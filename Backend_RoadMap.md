# EduBoost SA — Backend Implementation Roadmap

This roadmap tracks all backend-specific tasks: API layer, database, ORM models, services, auth, privacy, background jobs, observability, and model-serving infrastructure.

It is a living document. Update status as each item is implemented, tested, and committed. Cross-reference with `Functional_Implementation_Roadmap.md` for full-stack context.

## How to Use This Roadmap

- Mark each checkbox as work is completed and verified.
- Do not mark an item complete without tests and a commit.
- Treat "Done" as: implemented, tested, observable, and committed.
- Parallel changes must be reflected in `audits/recommendations/Backend_Report.md`.

## Implementation Status Legend

- `[ ]` Not started
- `[~]` In progress
- `[x]` Implemented and verified

---

## 1) Database Foundation

### 1.1 Schema Management

- [x] `db_init.sql` — base schema (learners, learner_identities, subject_mastery, session_events, study_plans, prompt_templates, consent_audit).
- [x] `db_migration_phase2.sql` — phase 2 tables (lessons, assessments, assessment_attempts, reports, badges, learner_badges, diagnostic_sessions, diagnostic_responses, item_bank, parent_accounts, parent_learner_links, audit_events).
- [x] All 19 tables applied to running Docker Postgres instance.
- [x] Row Level Security enabled on `learner_identities`, `learners`, `subject_mastery`.
- [ ] Alembic migration files aligned with SQL scripts (no drift between ORM and schema).
- [ ] CI check: fail pipeline when Alembic migrations drift from ORM models.
- [ ] Migration rollback paths documented and tested for critical schema changes.

### 1.2 Seed Data

- [x] `db_seed.sql` — base seed (3 learners, subject_mastery rows).
- [x] `db_seed_phase2.sql` — phase 2 seed (40 lessons, 22 badges, 34 item_bank items, 4 assessments, 3 reports).
- [ ] `prompt_templates` — seed active templates (lesson_generation, gap_remediation, diagnostic_intro, parent_report).
- [ ] Item bank depth: 100+ calibrated items per subject/grade (currently ~34 items total).
- [ ] Separate dev / staging / production seed strategies.

### 1.3 ORM Models (`db_models.py`)

- [x] `Learner`, `LearnerIdentity`, `SubjectMastery`, `SessionEvent`, `StudyPlan`.
- [x] `PromptTemplate`, `ConsentAudit`.
- [x] `DiagnosticSession`, `DiagnosticResponse`.
- [x] `Badge`, `LearnerBadge`, `ItemBank`, `AuditEvent`.
- [ ] `Lesson` ORM model (phase 2 table exists; ORM class missing).
- [ ] `Assessment` + `AssessmentAttempt` ORM models.
- [ ] `Report` ORM model.
- [ ] `ParentAccount` + `ParentLearnerLink` ORM models.

---

## 2) API Layer — Routers & Contracts

### 2.1 Application Entrypoint (`main.py`)

- [x] FastAPI app with CORS, GZip, rate limiting, Prometheus, Sentry integration.
- [x] All routers registered with versioned prefixes (`/api/v1/...`).
- [ ] **BUG FIX**: Line 110 — `code:` (unquoted) must be `"code":` in rate-limit exception handler.
- [ ] SlowAPI integration: confirm distributed rate limiting is consistent with in-memory middleware (potential double-counting).
- [ ] Standardise error envelope across all routers using `ErrorResponse` schema.

### 2.2 Learners Router (`/api/v1/learners`)

- [x] `POST /` — create pseudonymous learner.
- [x] `GET /{learner_id}` — fetch learner profile.
- [x] `PATCH /{learner_id}` — update learner fields.
- [x] `DELETE /{learner_id}` — POPIA right-to-erasure flag.
- [x] `GET /{learner_id}/mastery` — subject mastery summary.
- [ ] `POST /{learner_id}/mastery` — upsert/update a subject mastery entry.
- [ ] `GET /{learner_id}/progress` — session event summary (lessons done, time on task, XP history).
- [ ] Input validation: enforce grade-band consistency with home_language enum.

### 2.3 Lessons Router (`/api/v1/lessons`)

- [x] `POST /generate` — AI lesson generation pipeline.
- [x] `GET /{lesson_id}` — fetch cached Redis lesson.
- [x] `POST /{lesson_id}/feedback` — submit learner feedback (async).
- [x] `GET /cache/stats` — cache statistics.
- [x] `DELETE /cache` — clear lesson cache.
- [ ] `GET /catalog` — list DB-backed lesson catalog (filter: subject_code, grade_level, topic).
- [ ] `GET /catalog/{lesson_id}` — fetch a single lesson from DB.
- [ ] Lesson caching: cache generated lessons in Redis after creation.

### 2.4 Diagnostic Router (`/api/v1/diagnostic`)

- [x] Diagnostic session start, item fetch, response submission, session completion.
- [x] IRT 2PL theta estimation, SEM, Fisher information.
- [x] Gap probe logic and concept-level gap detection.
- [x] Persistence to `diagnostic_sessions` and `diagnostic_responses`.
- [ ] Retry/re-entry support for partially completed sessions.
- [ ] Item bank depth check before session start (fail gracefully if < N items available).
- [ ] `GET /{session_id}/history` — fetch full session history for a learner.
- [ ] Benchmark check: response-time SLA < 500ms p99.

### 2.5 Study Plans Router (`/api/v1/study-plans`)

- [x] Plan generation, save, fetch, refresh endpoints.
- [x] Gap-ratio scheduling and week-focus generation.
- [x] Rationale endpoint for parent/educator visibility.
- [ ] `GET /{learner_id}/history` — list all historical plans for a learner.
- [ ] Tighter linkage: auto-trigger plan refresh when diagnostic completes.
- [ ] Audit event emission on plan generation and refresh.

### 2.6 Gamification Router (`/api/v1/gamification`)

- [x] XP, level, streak, badge issuance, leaderboard endpoints.
- [ ] Badge award from DB `badges` table (currently hardcoded list vs. DB-driven).
- [ ] Daily XP cap enforcement.
- [ ] Anti-abuse validation tests.
- [ ] Frontend-visible endpoint: `GET /learner/{learner_id}/profile` — full XP + badge + level summary.

### 2.7 Parent Portal Router (`/api/v1/parent`)

- [x] Progress summaries, diagnostic trends, study-plan adherence, report generation.
- [x] Export (right-to-access), deletion request endpoints.
- [ ] Guardian auth flow: link `parent_accounts` → `parent_learner_links` → `learners`.
- [ ] Role/permission model: only linked guardian can access learner data.
- [ ] Integration tests: guardian login, learner linking, report retrieval, cross-tenant rejection.

### 2.8 Auth Router (`/api/v1/auth`)

- [x] JWT guardian login/signup, session creation, token refresh.
- [x] Pseudonymous learner session tokens.
- [x] Basic rate limiting on auth endpoints.
- [ ] Session invalidation on logout (token blacklist / short TTL enforcement).
- [ ] Deletion path: verify session tokens are purged on erasure.
- [ ] Negative tests: invalid token, privilege escalation, expired token.

### 2.9 Assessments Router (`/api/v1/assessments`) ❌ NEW

- [ ] `GET /` — list assessments (filter: subject_code, grade_level, assessment_type).
- [ ] `GET /{assessment_id}` — fetch assessment with questions.
- [ ] `POST /{assessment_id}/attempt` — submit learner attempt, compute score, persist to `assessment_attempts`.
- [ ] `GET /learner/{learner_id}/attempts` — list learner's past attempts.
- [ ] Register in `main.py` under `/api/v1/assessments`.

### 2.10 Audit Router (`/api/v1/audit`)

- [x] Audit event query/search service and routes.
- [ ] Audit emission on all protected mutations (consent, deletion, plan refresh, lesson generation).
- [ ] Signed/append-only guarantee (tamper-resistance checks).

### 2.11 System Router (`/api/v1/system`)

- [x] System info, config, health detail endpoints.
- [ ] Expose migration version and DB schema drift status.

---

## 3) Services Layer

### 3.1 Lesson Service (`lesson_service.py`)

- [x] Lesson generation orchestration (RLHF, prompt templating, output validation).
- [x] SA-context adaptation, CAPS alignment enforcement.
- [x] Output guardrails (age-appropriateness, toxicity filter, curriculum adherence).
- [ ] Lesson caching (Redis write-through after generation).
- [ ] `prompt_templates` DB read: load active templates instead of hardcoded strings.
- [ ] Lesson efficacy score pipeline connected to `session_events`.

### 3.2 Gamification Service (`gamification_service.py`)

- [x] XP computation, streak logic, badge eligibility checks.
- [x] Level progression and leaderboard ranking.
- [ ] DB-driven badge catalogue (read from `badges` table).
- [ ] Grade 4-7 discovery mechanics (richer challenge sets).

### 3.3 Study Plan Service (`study_plan_service.py`)

- [x] Gap-ratio scheduling, topic allocation, week-focus generation.
- [ ] Auto-integrate diagnostic output directly into plan generation.
- [ ] Plan change history audit.

### 3.4 Parent Portal Service (`parent_portal_service.py`)

- [x] Progress, diagnostic, adherence, report generation, export, deletion.
- [ ] Consent check enforcement before all data reads.
- [ ] AI-generated plain-language summaries for parent reports.

### 3.5 POPIA Deletion Service (`popia_deletion_service.py`)

- [x] End-to-end deletion across relational, cache, and derived stores.
- [x] Deletion request/completion audit events and right-to-access export.
- [ ] Verified encryption-at-rest for PII columns.
- [ ] Deletion coverage: `assessment_attempts`, `learner_badges`, `reports` cascades confirmed.

### 3.6 Inference Gateway (`inference_gateway.py`)

- [x] Model adapter abstraction, fallback policy.
- [ ] Remove external-provider fallover — route only to EduBoost-hosted model endpoints.
- [ ] Model version routing (dev → staging → prod).
- [ ] Batch inference mode for plan-level lesson pre-generation.

### 3.7 Audit Query Service (`audit_query_service.py`)

- [x] Audit event search, filtering, export.
- [ ] Signed record support (HMAC/hash chain per event).

---

## 4) Background Jobs (Celery)

- [ ] Idempotent task patterns with retry + dead-letter handling.
- [ ] Priority queues: learner-critical ops (lesson generation, diagnostic scoring) vs. batch (reports, plan refresh).
- [ ] Celery Beat scheduled tasks: daily plan refresh, weekly report generation, XP decay (if applicable).
- [ ] Task success/failure + latency metrics exposed to Prometheus.
- [ ] Integration tests: retry/backoff, poison-message, Redis interruption.

---

## 5) Observability

- [ ] Structured logging (`structlog`) on all service entry/exit points.
- [ ] Prometheus metrics: learner journey outcomes, queue depth, lesson generation latency, error spike rates.
- [ ] Distributed tracing correlation: frontend request → API → Celery worker → DB → model inference.
- [ ] Alert rules: API latency > 1s, queue backlog > 100, error rate > 1%, model-serving timeout.
- [ ] Grafana dashboards: product view, reliability view, privacy/compliance view.
- [ ] Runbooks for top alerts.

---

## 6) In-House Model Training & Serving

- [ ] Nano model selection (≤ 7B, quantized) for lesson generation.
- [ ] Reproducible training pipeline: data versioning, experiment tracking, artifact registry.
- [ ] CAPS-aligned training corpus with provenance tracking and licensing checks.
- [ ] Data quality pipeline: deduplication, contamination checks, age-band tagging.
- [ ] LoRA/QLoRA parameter-efficient fine-tuning workflow.
- [ ] Internal model serving endpoint with autoscaling and health checks.
- [ ] Model routing layer: grade/language-aware template and model selection.
- [ ] Model promotion gates: dev → staging → production based on evaluation thresholds.
- [ ] Golden test set for lesson quality, CAPS mapping, SA-context correctness.
- [ ] Automated eval suite: accuracy, hallucination risk, readability by grade band, response latency.

---

## 7) Security & Privacy

- [ ] Encryption-at-rest for PII columns (full Supabase Vault integration).
- [ ] MFA/2FA for guardian accounts.
- [ ] Session invalidation guarantees on deletion.
- [ ] Security audit of model endpoint: authz, rate-limits, abuse prevention.
- [ ] No direct learner identifiers in any LLM prompt (enforce via judiciary rules).

---

## 8) CI/CD (Backend)

- [ ] Pipeline: lint (ruff/black), unit tests, integration tests, migration drift check, security scan.
- [ ] Docker build validation in CI.
- [ ] Artifact/version tagging on release.
- [ ] Deployment promotion: dev → staging → production gates.
- [ ] Rollback and hotfix runbook documented.

---

## Execution Phases

### Phase A: Foundation Hardening (Current Sprint)
- [~] Fix `main.py` syntax bug.
- [~] Add missing Phase 2 ORM models.
- [~] Seed `prompt_templates`.
- [~] Add lesson catalog REST endpoints.
- [~] Add `assessments` router.

### Phase B: Core Learning Loop Completion
- [ ] Lesson caching (Redis write-through).
- [ ] DB-driven prompt templates in lesson service.
- [x] Item bank expansion (100+ items/subject/grade).
- [x] Diagnostic retry/re-entry.
- [x] Study plan ↔ diagnostic auto-linkage.

### Phase C: Engagement & Family Visibility
- [x] DB-driven badge awards.
- [x] Guardian auth → learner linking.
- [x] Role/permission model for parent portal.
- [x] Assessment attempts pipeline.

### Phase D: Production Readiness
- [ ] Celery job hardening.
- [ ] Observability SLOs and alert rules.
- [ ] In-house model training baseline.
- [ ] CI/CD pipeline full implementation.
- [ ] Security/privacy audit.
