# Development Guide

Everything you need to get EduBoost SA running locally, understand the codebase, and contribute effectively.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Running the Stack](#running-the-stack)
- [Environment Variables Reference](#environment-variables-reference)
- [Working with the Backend](#working-with-the-backend)
- [Working with the Frontend](#working-with-the-frontend)
- [Working with the Database](#working-with-the-database)
- [Working with Celery](#working-with-celery)
- [Accessing Local Services](#accessing-local-services)
- [Feature Flags](#feature-flags)
- [Common Development Tasks](#common-development-tasks)
- [Code Style](#code-style)

---

## Prerequisites

Install these before starting:

| Tool | Version | Install |
|------|---------|---------|
| Python | **3.11 exactly** | `pyenv install 3.11.9` |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) or `nvm` |
| Docker | 24+ | [docker.com/get-docker](https://docker.com/get-docker) |
| Docker Compose | v2 (plugin) | Included with Docker Desktop |
| Git | 2.40+ | OS package manager |

> **Python 3.11 is strictly required.** The `.python-version` file pins this. Using 3.12+ may cause issues with certain dependencies.

Verify your setup:
```bash
python --version    # Should say Python 3.11.x
node --version      # Should say v18.x.x or higher
docker --version    # Should say Docker version 24.x.x
docker compose version  # Should say Docker Compose version v2.x.x
```

---

## Initial Setup

### 1. Clone the repository

```bash
git clone https://github.com/NkgoloL/edo-boost-main.git
cd edo-boost-main
```

### 2. Configure environment variables

```bash
cp env.example .env
```

Open `.env` and fill in the required values. At minimum for local development:

```bash
# Required — generate random values for local dev
JWT_SECRET=<run: python3 -c "import secrets; print(secrets.token_hex(32))">
ENCRYPTION_KEY=<must be exactly 32 characters>
ENCRYPTION_SALT=any-random-string

# Required — at least one LLM key
GROQ_API_KEY=gsk_...       # Free: https://console.groq.com
# OR
ANTHROPIC_API_KEY=sk-ant-... # https://console.anthropic.com

# Docker Compose sets these automatically from the defaults below:
# DATABASE_URL, REDIS_URL — leave as-is for Docker dev
```

### 3. Install pre-commit hooks

```bash
pip install pre-commit
pre-commit install
```

This installs hooks that run linting and formatting checks on every `git commit`.

---

## Running the Stack

### Option A: Full Docker stack (recommended)

Starts all 8 services (API, frontend, Postgres, Redis, Celery, Prometheus, Grafana, Flower):

```bash
docker compose up --build
```

First run takes ~3–5 minutes to pull images and build containers. Subsequent runs are faster.

To run in the background:
```bash
docker compose up --build -d
docker compose logs -f api   # tail API logs
```

To stop:
```bash
docker compose down           # stop containers
docker compose down -v        # stop + delete volumes (wipes DB data)
```

### Option B: Backend only (faster iteration)

Use this when making backend-only changes and you don't need the full frontend:

```bash
# Terminal 1: Postgres + Redis
docker compose up postgres redis -d

# Terminal 2: Backend
cd app/api
python -m venv ../../.venv
source ../../.venv/bin/activate
pip install -r ../../requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000
```

### Option C: Frontend only (with remote or mocked API)

```bash
cd app/frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 npm run dev
```

---

## Accessing Local Services

| Service | URL | Notes |
|---------|-----|-------|
| **Frontend** | http://localhost:3002 | Next.js dev server |
| **API** | http://localhost:8000 | FastAPI |
| **Swagger UI** | http://localhost:8000/docs | Interactive API explorer |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |
| **Grafana** | http://localhost:3001 | Default login: `admin` / `admin` |
| **Prometheus** | http://localhost:9090 | Metrics explorer |
| **Flower** | http://localhost:5555 | Celery task monitor |
| **Postgres** | localhost:5432 | DB: `eduboost`, User: `eduboost_user` |
| **Redis** | localhost:6379 | No auth in dev |

---

## Environment Variables Reference

All variables are documented in `env.example`. Key groupings:

### Application

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` or `production` |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `DEBUG` | `false` | Never set `true` in production |

### Security (generate fresh values for every environment)

| Variable | Description |
|----------|-------------|
| `JWT_SECRET` | 64-char hex — sign with `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `ENCRYPTION_KEY` | Exactly 32 characters |
| `ENCRYPTION_SALT` | Any random string |
| `SECRET_KEY` | General app secret |

### AI Providers

| Variable | Default | Notes |
|----------|---------|-------|
| `GROQ_MODEL` | `llama3-70b-8192` | Free tier: 14,400 req/day |
| `GROQ_MAX_TOKENS` | `1800` | Per lesson generation |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` | Secondary/fallback |
| `HUGGINGFACE_MODEL` | `HuggingFaceH4/zephyr-7b-beta` | Offline fallback |

### Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `FEATURE_VOICE_INPUT` | `true` | Enable voice recording on mobile |
| `FEATURE_OFFLINE_MODE` | `true` | Cache lessons for offline use |
| `FEATURE_PARENT_REPORTS` | `true` | AI progress reports for guardians |
| `FEATURE_RLHF_COLLECTION` | `true` | Collect lesson feedback for model training |
| `FEATURE_LEARNING_STYLE_ML` | `true` | Personalise based on detected learning style |

### Audit / Governance

| Variable | Default | Description |
|----------|---------|-------------|
| `FOURTH_ESTATE_STREAM_KEY` | `eduboost:audit_stream` | Redis stream key for audit events |
| `FOURTH_ESTATE_MAX_LEN` | `100000` | Max events before MAXLEN trim |
| `ETHER_PROFILE_TTL` | `86400` | Cache TTL for profiler data (seconds) |

---

## Working with the Backend

### Project layout

```
app/api/
├── main.py               # App factory, middleware, router registration
├── orchestrator.py       # Multi-step workflow composition
├── judiciary.py          # POPIA policy gate (all learner data must pass here)
├── fourth_estate.py      # Audit event stream writer
├── profiler.py           # Slow-request profiling middleware
├── core/
│   ├── config.py         # Pydantic Settings (reads .env)
│   ├── database.py       # Async SQLAlchemy engine + session factory
│   └── celery_app.py     # Celery app definition + Beat schedule
├── models/               # SQLAlchemy ORM models
├── routers/              # FastAPI route handlers (thin — logic in services)
├── services/             # Business logic
│   ├── lesson_service.py
│   ├── study_plan_service.py
│   └── parent_portal_service.py
├── ml/
│   └── irt_engine.py     # Adaptive diagnostic engine (IRT)
└── constitutional_schema/ # Domain contracts (Pydantic models)
```

### Adding a new API endpoint

1. Add a route to the appropriate file in `routers/` or create a new router file
2. Add business logic to the matching service in `services/`
3. Register a new router in `main.py` if you created a new router file
4. Write an integration test in `tests/integration/`
5. Update `docs/API_REFERENCE.md`

### Dependency injection pattern

```python
# routers/lesson.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.core.database import get_db
from app.api.services.lesson_service import LessonService

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.post("/", status_code=201)
async def create_lesson(
    request: LessonRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    service = LessonService(db)
    return await service.generate(request, current_user.learner_id)
```

### Adding a Celery task

```python
# core/celery_app.py
from celery import Celery

celery_app = Celery("eduboost", broker=settings.REDIS_URL)

@celery_app.task(name="generate_parent_report")
def generate_parent_report(learner_id: str, period_weeks: int):
    ...
```

Register periodic tasks in the `beat_schedule` in `celery_app.py`.

---

## Working with the Frontend

### Project layout

```
app/frontend/
├── src/
│   ├── app/                  # Next.js App Router pages
│   │   ├── dashboard/
│   │   ├── diagnostic/
│   │   ├── lesson/[id]/
│   │   ├── study-plan/
│   │   └── parent/
│   ├── components/
│   │   └── eduboost/         # Domain-specific components
│   └── lib/
│       └── api/              # API client (all fetch calls live here)
│           ├── auth.ts
│           ├── learner.ts
│           ├── lesson.ts
│           ├── diagnostic.ts
│           ├── study-plan.ts
│           └── parent.ts
```

### Adding a new page

```
1. Create src/app/<route>/page.tsx
2. If it needs client-side state, add "use client" at the top
3. Add API calls in src/lib/api/<resource>.ts
4. Import the API function in the page component
```

### API client conventions

```typescript
// src/lib/api/lesson.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL

export const lessonApi = {
  async generate(payload: LessonRequest): Promise<Lesson> {
    const res = await fetch(`${API_BASE}/lessons`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getStoredToken()}`,
      },
      body: JSON.stringify(payload),
    })
    if (!res.ok) throw new ApiError(await res.json())
    return res.json()
  }
}
```

Never call `fetch()` directly in a page or component — always go through `src/lib/api/`.

---

## Working with the Database

### Running migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Roll back the last migration
alembic downgrade -1

# Check current migration state
alembic current

# Show migration history
alembic history --verbose
```

### Creating a new migration

```bash
# After changing a SQLAlchemy model:
alembic revision --autogenerate -m "add_learning_style_to_learners"
```

Review the generated file in `alembic/versions/` before applying — autogenerate is not always perfect.

### Connecting to Postgres directly

```bash
# Via Docker
docker exec -it eduboost-postgres psql -U eduboost_user -d eduboost

# Via psql locally
psql postgresql://eduboost_user:devpassword@localhost:5432/eduboost
```

### Seeding development data

```bash
# The Docker Compose setup auto-runs these on first start:
scripts/db_init.sql    # Schema (if not using Alembic)
scripts/db_seed.sql    # Sample learners, guardians, lessons
scripts/db_audit_migration.sql  # Audit table setup
```

To re-seed:
```bash
docker exec -i eduboost-postgres psql -U eduboost_user -d eduboost < scripts/db_seed.sql
```

---

## Working with Celery

### Running workers manually (outside Docker)

```bash
# Worker
celery -A app.api.core.celery_app worker --loglevel=info --concurrency=2

# Beat scheduler
celery -A app.api.core.celery_app beat --loglevel=info

# Flower monitor
celery -A app.api.core.celery_app flower --port=5555
```

### Triggering a task manually

```python
# In a Python shell or test:
from app.api.core.celery_app import celery_app
result = celery_app.send_task("generate_parent_report", args=["lrn_abc123", 4])
print(result.get(timeout=60))
```

### Inspecting the queue

```bash
celery -A app.api.core.celery_app inspect active
celery -A app.api.core.celery_app inspect reserved
```

---

## Feature Flags

Feature flags are read from environment variables at startup:

```python
# In code
from app.api.core.config import settings

if settings.FEATURE_VOICE_INPUT:
    # enable voice recording endpoint
```

To toggle a flag locally, update `.env` and restart the API container:
```bash
docker compose restart api
```

---

## Common Development Tasks

### Rebuild a single service

```bash
docker compose up --build api      # rebuild only the API
docker compose up --build frontend # rebuild only the frontend
```

### View logs

```bash
docker compose logs -f api          # API logs
docker compose logs -f celery-worker  # Celery logs
docker compose logs -f postgres     # Database logs
```

### Reset everything

```bash
docker compose down -v              # removes all volumes (data wiped)
docker compose up --build           # fresh start
```

### Check environment variable resolution

```bash
bash scripts/check_env.sh           # validates Python runtime and key vars
```

### Generate a secure secret

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Code Style

### Python

- All code formatted with `black` (via pre-commit)
- Import ordering managed by `isort` (via pre-commit)
- Linting via `ruff`
- Type hints required on all public functions
- Docstrings required on all classes and public methods (Google style)

### TypeScript (Frontend)

- Strict TypeScript mode enabled
- ESLint configured (root `package.json` includes `eslint`)
- No `any` types without explicit comments

### Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat(api): add voice input endpoint
fix(ml): correct IRT theta update for empty response vectors
test(services): add coverage for StudyPlanService gap normalisation
docs(api): update lesson endpoint request schema
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide.
