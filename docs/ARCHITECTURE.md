# System Architecture

**EduBoost SA** — AI-Powered Adaptive Learning Platform for South African Learners

---

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Component Map](#component-map)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [AI / LLM Layer](#ai--llm-layer)
- [Adaptive Diagnostic Engine](#adaptive-diagnostic-engine)
- [Background Task System](#background-task-system)
- [Database Design](#database-design)
- [Governance Layers](#governance-layers)
- [Observability Stack](#observability-stack)
- [Infrastructure](#infrastructure)
- [Data Flow: Lesson Request](#data-flow-lesson-request)
- [Data Flow: Diagnostic Assessment](#data-flow-diagnostic-assessment)
- [Security Boundaries](#security-boundaries)
- [Architectural Decisions](#architectural-decisions)

---

## High-Level Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        Learner / Guardian                      │
└─────────────────────────────┬────────────────────────────────┘
                              │ HTTPS
┌─────────────────────────────▼────────────────────────────────┐
│                  Next.js 14 Frontend (App Router)              │
│  Dashboard │ Diagnostic │ Lesson │ Study Plan │ Parent Portal  │
│                    src/lib/api/ (service layer)                │
└─────────────────────────────┬────────────────────────────────┘
                              │ REST API (JSON)
┌─────────────────────────────▼────────────────────────────────┐
│                  FastAPI Backend (Python 3.11)                  │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │  Routers │ │Services │ │   ML     │ │  Constitutional   │  │
│  │ (auth,   │ │(Lesson, │ │  (IRT    │ │  Schema +        │  │
│  │ learner, │ │StudyPlan│ │  Engine) │ │  Orchestrator)   │  │
│  │ lesson,  │ │ Parent  │ │          │ │                  │  │
│  │ parent)  │ │ Portal) │ │          │ │                  │  │
│  └──────────┘ └─────────┘ └──────────┘ └──────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Judiciary (Policy Layer)  │  Fourth Estate (Audit)       │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────┬─────────────┬──────────────┬──────────────┬────────────┘
       │             │              │              │
  ┌────▼───┐   ┌─────▼──┐    ┌─────▼──┐    ┌──────▼─────┐
  │Postgres│   │ Redis   │    │ Groq / │    │  Celery     │
  │  16    │   │ 7       │    │Anthropic│   │  Workers    │
  │(SQLAlch│   │(Cache + │    │/HuggFace│   │  + Beat     │
  │emy 2)  │   │ Broker) │    └─────────┘   └────────────┘
  └────────┘   └─────────┘
```

---

## Component Map

### Repository Structure

```
edo-boost-main/
├── app/
│   ├── api/                          # FastAPI application root
│   │   ├── constitutional_schema/    # Schema, typing, domain contracts
│   │   ├── core/                     # Config, DB session, Celery app
│   │   │   ├── config.py             # Pydantic Settings (reads .env)
│   │   │   ├── database.py           # Async SQLAlchemy engine + session
│   │   │   └── celery_app.py         # Celery app + Beat schedule
│   │   ├── ml/                       # Adaptive Engine
│   │   │   └── irt_engine.py         # 2PL/3PL IRT scoring & item selection
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   ├── routers/                  # FastAPI route handlers
│   │   │   ├── auth.py               # Login, JWT token issuance
│   │   │   ├── learner.py            # Learner CRUD, profile
│   │   │   ├── lesson.py             # Lesson generation & retrieval
│   │   │   ├── diagnostic.py         # IRT diagnostic sessions
│   │   │   ├── study_plan.py         # CAPS-aligned study plans
│   │   │   └── parent.py             # Parent portal, reports
│   │   ├── services/                 # Business logic
│   │   │   ├── lesson_service.py     # LLM lesson generation
│   │   │   ├── study_plan_service.py # CAPS scheduling + gap remediation
│   │   │   └── parent_portal_service.py # AI progress reports
│   │   ├── main.py                   # FastAPI app factory, middleware
│   │   ├── orchestrator.py           # Workflow composition
│   │   ├── judiciary.py              # Policy / POPIA validation gate
│   │   ├── fourth_estate.py          # Append-only audit event stream
│   │   └── profiler.py               # Request profiling helpers
│   └── frontend/                     # Next.js 14 App Router
│       ├── src/app/                  # Route segments
│       │   ├── dashboard/            # Learner home
│       │   ├── diagnostic/           # Assessment flow
│       │   ├── lesson/               # Lesson viewer
│       │   ├── study-plan/           # Weekly schedule
│       │   └── parent/               # Guardian dashboard
│       ├── src/components/eduboost/  # Shared UI components
│       └── src/lib/api/              # Type-safe API client layer
├── alembic/                          # Database migrations
├── tests/
│   ├── unit/                         # Isolated unit tests
│   └── integration/                  # API + DB integration tests
├── docker/                           # Dockerfiles
│   ├── Dockerfile.api
│   └── Dockerfile.frontend
├── k8s/                              # Kubernetes manifests (WIP)
├── bicep/                            # Azure IaC experiments (WIP)
├── grafana/                          # Grafana dashboard provisioning
├── scripts/                          # DB init/seed SQL scripts
├── docker-compose.yml                # Local dev stack (8 services)
└── docker-compose.prod.yml           # Production compose (WIP)
```

---

## Backend Architecture

### FastAPI Application

The backend is a **fully async FastAPI application** using Python 3.11. All I/O operations (database, Redis, HTTP to LLM providers) are async.

**Startup sequence (`main.py`):**
1. Load `Settings` from environment via `pydantic-settings`
2. Create async SQLAlchemy engine
3. Mount Prometheus metrics middleware (`prometheus-fastapi-instrumentator`)
4. Register Sentry SDK
5. Configure CORS (explicit origin whitelist)
6. Register rate limiters (`slowapi`)
7. Include all routers with `/api/v1/` prefix
8. Mount health check at `/health`

**Request lifecycle:**
```
HTTP Request
    → CORS middleware
    → Rate limiter (SlowAPI: 100 req/min default, 20 req/min LLM endpoints)
    → JWT auth dependency (where required)
    → Judiciary policy gate (for learner-data operations)
    → Router handler
    → Service layer
    → SQLAlchemy async session / Redis / LLM client
    → Fourth Estate audit event (for sensitive ops)
    → Response
```

### Service Layer

Services contain all business logic and are injected into routers via FastAPI's dependency injection system.

| Service | Responsibility |
|---------|---------------|
| `LessonService` | Calls LLM provider chain, injects SA context, caches result in Redis |
| `StudyPlanService` | CAPS-aligned scheduling, accepts knowledge gaps as strings or dicts |
| `ParentPortalService` | Generates AI progress reports; returns both `report` and legacy-compatible `data` keys |

### Database Session Management

```python
# All sessions are async and scoped to a single request
async with AsyncSessionLocal() as session:
    async with session.begin():
        # all operations in this block are transactional
```

Sessions are **never shared across requests**. Connection pooling is managed by SQLAlchemy's async pool.

---

## Frontend Architecture

### Next.js 14 App Router

The frontend uses the **App Router** (introduced in Next.js 13+) with **React Server Components** as the default. Client components are explicitly marked `"use client"`.

**Page segments:**

| Route | Component | Rendering |
|-------|-----------|-----------|
| `/` | Landing / redirect | Server |
| `/dashboard` | Learner home with XP & streaks | Client |
| `/diagnostic` | IRT assessment flow | Client |
| `/lesson/[id]` | Lesson viewer | Server + Client |
| `/study-plan` | Weekly schedule grid | Client |
| `/parent` | Guardian dashboard | Server |

### API Service Layer (`src/lib/api/`)

All API calls are centralised in `src/lib/api/`. Components never call `fetch()` directly.

```typescript
// Example pattern
import { lessonApi } from '@/lib/api/lesson'

const lesson = await lessonApi.getLesson(lessonId)
```

Benefits: single point for auth headers, error handling, retry logic, and type safety.

---

## AI / LLM Layer

### Provider Chain

LLM requests use a **fallback chain with retry logic** (via `tenacity`):

```
Groq (llama3-70b-8192)        ← Primary
    ↓ on timeout/rate-limit/error
Anthropic (claude-sonnet-4-20250514) ← Secondary
    ↓ on timeout/error
HuggingFace (zephyr-7b-beta)  ← Offline fallback
```

**Rate limits enforced:**

| Provider | Limit | Configured by |
|----------|-------|---------------|
| Groq | 20 req/min, 14,400 req/day | `GROQ_DAILY_REQUEST_LIMIT`, `RATE_LIMIT_LLM_PER_MINUTE` |
| Anthropic | 20 req/min (shared with Groq gate) | Same SlowAPI rule |
| HuggingFace | No external rate limit (local inference option) | N/A |

### South African Localisation

Every LLM prompt injects SA-specific context:
- Rand (ZAR) as currency
- Local wildlife (springbok, rhino, weaver bird)
- Ubuntu philosophy
- Braai, kwaito, and other cultural references appropriate to grade level
- CAPS topic alignment (Mathematics, Home Language, Life Skills, etc.)

### Lesson Caching

Generated lessons are cached in Redis with a TTL derived from lesson parameters. Subsequent requests for the same learner-grade-topic combination return the cached version without calling the LLM.

---

## Adaptive Diagnostic Engine

### Item Response Theory (IRT)

The diagnostic engine in `app/api/ml/irt_engine.py` implements **2-Parameter Logistic (2PL) IRT**, with architecture to extend to 3PL for Grade 4–7 learners (where guessing is a factor).

**Key concepts:**

| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| Discrimination | `a` | How sharply the item distinguishes ability levels |
| Difficulty | `b` | The ability level at which P(correct) = 0.5 |
| Learner ability | `θ` (theta) | Estimated on a standard normal scale |

**2PL model:**
```
P(correct | θ) = 1 / (1 + exp(-a * (θ - b)))
```

**Adaptive item selection:**
- Items are selected to maximise **Fisher Information** at the current θ estimate
- After each response, θ is updated using **Maximum Likelihood Estimation (MLE)**
- Termination: fixed number of items (configurable) or standard error threshold

**Grade mapping:**
```
θ < -2.0  → Grade R–1 remediation needed
θ -2.0–-1.0 → Grade 2–3 foundation
θ -1.0–0.0  → Grade 4–5 on track
θ  0.0–1.0  → Grade 6–7 grade level
θ > 1.0     → Advanced / extension content
```

---

## Background Task System

### Celery + Redis

Background tasks are handled by **Celery 5.4** with **Redis 7** as the broker and result backend.

**Worker configuration:**
```yaml
celery-worker: concurrency=2 (local dev)
celery-beat:  scheduled tasks (cron-like)
```

**Registered tasks:**

| Task | Trigger | Description |
|------|---------|-------------|
| `generate_parent_report` | On demand / weekly | AI progress report via `ParentPortalService` |
| `send_report_email` | After report generation | SendGrid email via Jinja2 template |
| `rlhf_batch_collection` | Celery Beat (weekly) | Collect lesson feedback for model improvement |
| `regenerate_study_plan` | Celery Beat / on demand | Re-schedule when learner completes a milestone |

**Monitoring:** Flower dashboard at `:5555` shows real-time task queue depth, worker status, and task history.

---

## Database Design

### Key Tables

| Table | Purpose |
|-------|---------|
| `learners` | Pseudonymous learner profile (no direct PII) |
| `guardians` | Parent/guardian accounts with consent records |
| `consent_records` | Timestamped POPIA consent grants and revocations |
| `diagnostic_sessions` | IRT session metadata |
| `diagnostic_responses` | Per-item responses with timestamps |
| `lessons` | Generated lesson cache with LLM provider metadata |
| `study_plans` | CAPS-aligned weekly schedule records |
| `study_plan_items` | Individual session slots within a plan |
| `knowledge_gaps` | Identified gaps from diagnostic (concept + severity) |
| `badges` | Gamification badge definitions |
| `learner_badges` | Earned badges with timestamp |
| `xp_events` | XP transaction log (append-only) |
| `audit_log` | Mirror of critical Fourth Estate events in SQL |

### Migration Strategy

All schema changes go through **Alembic**. Runtime `create_all()` is disabled.

```bash
# Apply pending migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "add_index_to_knowledge_gaps_learner_id"

# Roll back one migration
alembic downgrade -1
```

Migration files live in `alembic/versions/`. Every `upgrade()` must have a matching `downgrade()`.

---

## Governance Layers

### Judiciary (`judiciary.py`)

The Judiciary is a **policy validation gate** that every service call touching learner data must pass through. It enforces:

1. **Consent check** — has the guardian granted POPIA consent for this operation?
2. **Pseudonymisation** — strips direct identity fields before passing to LLM services
3. **Data minimisation** — validates that only required fields are included in payloads
4. **Age-appropriate check** — applies stricter rules for Grade R–3 learners

If a policy check fails, the Judiciary raises an exception that FastAPI converts to a `403 Forbidden` with a structured error body.

### Fourth Estate (`fourth_estate.py`)

The Fourth Estate is an **append-only audit trail** implemented as a Redis stream.

```python
# Stream key
FOURTH_ESTATE_STREAM_KEY = "eduboost:audit_stream"
FOURTH_ESTATE_MAX_LEN = 100_000   # MAXLEN trimming

# Event schema (simplified)
{
    "event_type": "lesson_generated",
    "learner_pseudoid": "abc123",
    "provider": "groq",
    "grade": 4,
    "subject": "Mathematics",
    "timestamp": "2025-04-01T10:00:00Z",
    "session_id": "sess_xyz"
}
```

Events are consumed by a background reader that mirrors critical events to the SQL `audit_log` table for POPIA compliance reporting.

### Constitutional Schema (`constitutional_schema/`)

Defines the **domain contracts** (Pydantic models) shared between layers. Named after constitutional governance — it is the highest-level law of data shape in the system.

### Orchestrator (`orchestrator.py`)

Composes multi-step workflows (e.g., "run diagnostic → identify gaps → generate study plan → notify guardian"). The orchestrator coordinates services without coupling them directly to each other.

---

## Observability Stack

### Metrics (Prometheus + Grafana)

Prometheus scrapes the FastAPI metrics endpoint at `:8000/metrics` (exposed by `prometheus-fastapi-instrumentator`).

**Key metrics:**
- `http_request_duration_seconds` — latency histogram per endpoint
- `http_requests_total` — request count with status labels
- `celery_tasks_total` — task count by name and state
- `llm_request_duration_seconds` — LLM provider latency (custom)
- `learner_sessions_active` — concurrent learner sessions (custom)

Grafana dashboards are provisioned from `grafana/dashboards/` on startup.

### Error Tracking (Sentry)

Sentry SDK is integrated with the FastAPI app. All unhandled exceptions are captured with:
- Request context
- User ID (pseudonymised)
- Environment tag (`APP_ENV`)

Configure via `SENTRY_DSN` environment variable.

### Structured Logging (`structlog`)

All backend logs are structured JSON via `structlog`. Log level is configurable via `LOG_LEVEL`.

```json
{
  "event": "lesson_generated",
  "provider": "groq",
  "grade": 4,
  "latency_ms": 1240,
  "level": "info",
  "timestamp": "2025-04-01T10:00:01Z"
}
```

### Request Profiling (`profiler.py`)

The profiler middleware captures slow request traces. Configurable threshold (default: flag requests > 500ms).

---

## Infrastructure

### Local Development (Docker Compose)

```yaml
Services:
  frontend:  localhost:3002   (Next.js dev server, hot reload)
  api:       localhost:8000   (FastAPI with uvicorn --reload)
  postgres:  localhost:5432   (PostgreSQL 16-alpine)
  redis:     localhost:6379   (Redis 7-alpine, 256MB max)
  prometheus: localhost:9090
  grafana:   localhost:3001
  flower:    localhost:5555
  celery-worker: (no exposed port)
  celery-beat:   (no exposed port)
```

### Kubernetes (Work in Progress)

Manifests in `k8s/` provide a skeleton for deployment to any Kubernetes cluster (GKE, AKS, EKS). **Not yet production-validated.**

### Azure (Bicep, Experimental)

`bicep/` contains infrastructure-as-code for Azure deployment. **Experimental — not used in any active environment.**

---

## Data Flow: Lesson Request

```
Learner clicks "Start Lesson"
    ↓
Next.js page calls lessonApi.createLesson({ grade, subject, topic })
    ↓
POST /api/v1/lessons   (JWT required)
    ↓
auth dependency: validate JWT, extract learner_pseudoid
    ↓
rate_limit check: 20 req/min for LLM endpoints
    ↓
Judiciary.validate_lesson_request(learner_pseudoid, grade, topic)
    ├─ Check consent is active
    └─ Pseudonymise learner context
    ↓
Redis cache check: key = hash(grade, subject, topic, sa_context_seed)
    ├─ Cache HIT → return cached lesson JSON
    └─ Cache MISS → proceed to LLM
    ↓
LessonService.generate(grade, subject, topic, sa_context)
    ├─ Build CAPS-aligned prompt with SA localisation
    ├─ Call Groq (primary) via httpx with tenacity retry
    │   └─ On failure → Anthropic → HuggingFace
    └─ Parse + validate lesson schema
    ↓
Store in Redis (TTL: 3600s)
Store lesson record in PostgreSQL
Fourth Estate: emit "lesson_generated" event
    ↓
Return lesson JSON to frontend
```

---

## Data Flow: Diagnostic Assessment

```
Learner starts diagnostic
    ↓
POST /api/v1/diagnostic/sessions  (JWT required)
    ↓
IRT Engine: initialise θ = 0.0 (prior), SE = ∞
    ↓
LOOP (until termination condition):
    IRT Engine: select_item(θ, administered_items)
        └─ Maximise Fisher Information at current θ estimate
    ↓
    Frontend renders item
    Learner responds
    ↓
    POST /api/v1/diagnostic/sessions/{id}/responses
    ↓
    IRT Engine: update_theta(responses, item_bank)
        └─ MLE over response vector
    IRT Engine: compute_se(θ, items)
    ↓
    If SE < threshold OR max_items reached → terminate
    ↓ (continue loop)
    ↓
POST /api/v1/diagnostic/sessions/{id}/complete
    ↓
IRT Engine: score_to_grade(θ) → grade_estimate, knowledge_gaps[]
    ↓
StudyPlanService: generate_plan(grade_estimate, knowledge_gaps)
    ↓
Fourth Estate: emit "diagnostic_completed" + "study_plan_generated"
    ↓
Return results to frontend
```

---

## Security Boundaries

```
┌─────────────────────────────────────────────────────┐
│              PUBLIC INTERNET                         │
│    (Learners, Guardians, Unauthenticated requests)   │
└────────────────────┬────────────────────────────────┘
                     │ HTTPS only
┌────────────────────▼────────────────────────────────┐
│           Next.js Frontend (CDN edge)                │
│   Only NEXT_PUBLIC_ env vars exposed to browser      │
└────────────────────┬────────────────────────────────┘
                     │ REST over HTTPS, CORS enforced
┌────────────────────▼────────────────────────────────┐
│       FastAPI Backend (private network/VPC)          │
│   JWT auth → Judiciary → Services → DB               │
│   LLM calls go OUTBOUND only (no inbound webhook)    │
└────┬──────────────┬──────────────┬──────────────────┘
     │              │              │
  ┌──▼──┐       ┌───▼───┐     ┌───▼────────────────┐
  │ DB  │       │ Redis │     │ LLM Providers       │
  │(VPC)│       │ (VPC) │     │ (OUTBOUND TLS only) │
  └─────┘       └───────┘     └────────────────────┘
```

**Key principles:**
- Database and Redis are never exposed to the internet
- LLM API keys are environment secrets, never in source code
- Learner PII never leaves the backend unredacted
- All frontend-to-backend communication requires a valid JWT

---

## Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Async framework** | FastAPI | Best-in-class Python async, auto OpenAPI docs |
| **ORM** | SQLAlchemy 2.0 async | Production-grade, native async support |
| **Frontend** | Next.js 14 App Router | React Server Components reduce client JS bundle |
| **LLM strategy** | Multi-provider fallback | Resilience + cost control; Groq free tier for dev |
| **IRT model** | 2PL (extending to 3PL) | Industry standard for adaptive assessments |
| **Audit trail** | Redis stream | Append-only, high-throughput, TTL-safe |
| **Background tasks** | Celery + Redis | Mature, well-understood; same Redis as cache |
| **Pseudonymisation gate** | `judiciary.py` | Single enforcement point prevents drift |
| **Migration tool** | Alembic | De-facto standard for SQLAlchemy projects |
| **Monitoring** | Prometheus + Grafana | Open-source, no vendor lock-in |
