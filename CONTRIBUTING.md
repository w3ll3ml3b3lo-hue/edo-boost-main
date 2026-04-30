# Contributing to EduBoost SA

Thank you for contributing to EduBoost SA. This document covers everything you
need to get the stack running locally, the development workflow, and the rules
that keep the codebase safe for the children who use this platform.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Running the Stack](#running-the-stack)
4. [Development Workflow (TDD Loop)](#development-workflow)
5. [Testing](#testing)
6. [POPIA Rules — Non-Negotiable](#popia-rules)
7. [Commit & Branch Conventions](#commit--branch-conventions)
8. [Releasing](#releasing)
9. [Architecture Quick Reference](#architecture-quick-reference)

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Docker Desktop | 4.x+ | Local stack |
| Docker Compose | v2.x+ | Bundled with Docker Desktop |
| Python | 3.11+ | Backend development |
| Node.js | 20 LTS | Frontend development |
| Git | 2.40+ | Version control |

Optional but recommended:
- `pgcli` — better PostgreSQL CLI
- `httpx` — for running `scripts/popia_sweep.py --live-check`

---

## Environment Setup

```bash
# 1. Clone the repo
git clone https://github.com/NkgoloL/edo-boost-main.git
cd edo-boost-main

# 2. Create your local environment file
cp .env.example .env
# Open .env and fill in required values (marked REQUIRED in the file)

# 3. Install Python dev dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 4. Install frontend dependencies
cd app/frontend && npm ci && cd ../..

# 5. Install Playwright browsers (for E2E tests)
npx playwright install chromium
```

**Note:** If you need local ML inference (torch/transformers), install separately:
```bash
pip install -r requirements-ml.txt --extra-index-url https://download.pytorch.org/whl/cpu
```
This is optional — the API uses Anthropic/Groq in development by default.

---

## Running the Stack

```bash
# Start all services (Postgres, Redis, API, Frontend, Celery, Prometheus, Grafana)
docker-compose up -d

# Watch API logs
docker-compose logs -f api

# Run database migrations manually (auto-runs on startup via db-migrate service)
alembic upgrade head

# URLs:
#   Frontend:   http://localhost:3000
#   API docs:   http://localhost:8000/docs
#   Grafana:    http://localhost:3001  (admin / value from GRAFANA_ADMIN_PASSWORD)
#   Prometheus: http://localhost:9090
#   Flower:     http://localhost:5555
```

---

## Development Workflow

EduBoost SA follows a **TDD-first loop**. For every new feature or bug fix:

```
1. Write a failing test  →  tests/unit/ or tests/integration/
2. Run it (confirm red)  →  pytest tests/ -k "your_test_name"
3. Implement the feature →  app/api/
4. Run it (confirm green) → pytest tests/
5. Run POPIA sweep       →  python scripts/popia_sweep.py
6. Commit                →  following conventions below
```

Agents must update `audits/roadmap.md` before starting a new session.

---

## Testing

```bash
# Full test suite (unit + integration, excluding E2E)
pytest tests/ -v --cov=app --cov-report=term-missing -m "not e2e"

# POPIA enforcement tests only (run before every PR)
pytest tests/popia/ -v

# E2E tests (requires running stack)
npx playwright test

# POPIA static sweep (run before every PR)
python scripts/popia_sweep.py --fail-on-issues

# Frontend lint and type checks
cd app/frontend && npm run lint && npm run type-check
```

Coverage target: **60% minimum** (CI enforces this). New features must not
lower coverage.

---

## POPIA Rules — Non-Negotiable

EduBoost SA processes personal data of children aged 5–13. POPIA compliance is
not optional and not negotiable. Every contributor must follow these rules:

### 1. Consent gate is mandatory
Every API endpoint that reads or writes learner personal data MUST call
`ConsentService.require_active_consent()` before any database access.

```python
# ✅ Correct
async def get_lesson(learner_id: UUID, db: AsyncSession = Depends(get_db)):
    await ConsentService.require_active_consent(db, learner_id)  # FIRST
    lesson = await LessonService.get_latest(db, learner_id)
    ...

# ❌ POPIA violation — never do this
async def get_lesson(learner_id: UUID, db: AsyncSession = Depends(get_db)):
    lesson = await LessonService.get_latest(db, learner_id)  # No consent check!
    ...
```

### 2. Never send real identifiers to LLM providers
Only `pseudonym_id` (not `learner_id`, not names, not emails) may appear in
prompts sent to Anthropic, Groq, or HuggingFace.

```python
# ✅ Correct
prompt = f"Generate a Grade 4 maths lesson for learner {learner.pseudonym_id}"

# ❌ POPIA violation
prompt = f"Generate a lesson for {learner.display_name} ({learner.id})"
```

### 3. Audit log every consent change
Calls to `grant()`, `revoke()`, and `execute_erasure()` must be followed by an
audit log entry. The `fourth_estate.py` component provides this — use it.

### 4. Run the POPIA sweep before every PR
```bash
python scripts/popia_sweep.py --fail-on-issues
```
If the sweep reports any critical or high issues, fix them before opening the PR.
PRs with unresolved POPIA issues will not be merged.

---

## Commit & Branch Conventions

Branch naming:
```
feature/short-description
fix/short-description
chore/short-description
docs/short-description
```

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add consent renewal reminder email
fix: correct expires_at calculation in mark_granted
chore: move torch to requirements-ml.txt
docs: update CONTRIBUTING.md with POPIA rules
test: add E2E lesson delivery test
```

**Do not** commit directly to `main`. Open a PR and get at least one review.

---

## Releasing

Releases are managed via GitHub Actions. To cut a release:

1. Ensure `main` is green (all CI checks pass).
2. Go to **Actions → Release → Run workflow**.
3. Select bump type: `patch` | `minor` | `major`.
4. The workflow will bump `app/api/version.py`, update `CHANGELOG.md`, tag,
   and trigger production deployment automatically.

**Never** manually edit `app/api/version.py` or create git tags by hand.

---

## Architecture Quick Reference

```
app/
  api/
    routers/        HTTP layer — thin, validates input, calls services
    services/       Business logic — consent_service, lesson_service, etc.
    models/         SQLAlchemy 2.0 ORM models
    core/           DB session, Celery config, security utils
    orchestrator.py Workflow orchestration (multi-step LLM flows)
    judiciary.py    Policy enforcement (content safety, rate limits)
    fourth_estate.py Audit logging component
  frontend/         Next.js 14 App Router
    src/app/        Page routes (dashboard, lesson, diagnostic, parent)
    src/components/ UI component library
    src/lib/api/    API service layer (typed fetch wrappers)

tests/
  unit/             Fast, no DB — mock everything external
  integration/      Real DB (test schema), no external APIs
  popia/            POPIA consent enforcement tests (must always pass)
  e2e/              Playwright — full stack, real browser

scripts/
  popia_sweep.py    POPIA static + dynamic audit
  db_seed.sql       Reference data (run once via SEED_ON_BOOT=true)

alembic/
  versions/         DB migrations — Alembic is the ONLY schema authority
```
