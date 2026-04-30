# Changelog

All notable changes to EduBoost SA are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Release cadence:
  - Patch (0.x.Y): bug fixes, documentation, dependency updates — no DB migration
  - Minor (0.X.0): new features, non-breaking API changes — may include migration
  - Major (X.0.0): breaking API changes, major schema changes — requires migration guide

---

## [Unreleased]

### Added
- `requirements-ml.txt` separates torch/transformers from base install (#4)
- `INCLUDE_ML` Docker build argument gates heavyweight ML deps (#4)
- `docker-compose.prod.yml` canonical production deployment stack (#3)
- Nginx reverse-proxy with SSL termination and security headers (#3)
- `.github/workflows/ci-cd.yml` canonical CI/CD pipeline with staging and production gates (#3)
- Playwright E2E test suite covering diagnostic → study plan → lesson → parent portal (#6)
- `scripts/popia_sweep.py` automated POPIA audit of LLM prompt paths and consent gates (#7)
- `tests/popia/test_consent_enforcement.py` integration tests for consent gating (#7)
- Grafana dashboard: Learner Journey SLOs (`grafana/dashboards/learner_journey.json`) (#9)
- Grafana dashboard: LLM Provider Health (`grafana/dashboards/llm_provider_health.json`) (#9)
- Consolidated `.env.example` (removed duplicate `env.example`) (#10)
- `CONTRIBUTING.md` developer onboarding and contribution guidelines (#10)
- `app/api/version.py` single source of truth for application version

### Changed
- `docker-compose.yml` frontend port corrected to `3000:3000` (was `3002:3050`) (#5)
- Alembic migration `0001` now sole source of truth for schema (SQL scripts removed from compose startup) (#1)
- `ConsentService.require_active_consent()` documented as mandatory gate at all learner endpoints (#2)

### Fixed
- `celery-beat` missing `db-migrate` dependency in compose file
- `db-migrate` service lacked `SEED_ON_BOOT` default in dev compose

---

## [0.1.0-beta] — 2026-04-30

First tagged beta release. Establishes foundational architecture.

### Added
- FastAPI backend with routers: auth, learners, consent, diagnostic, lessons, study-plans, parent-portal
- Next.js 14 App Router frontend: dashboard, lesson view, diagnostic, parent portal
- Alembic migration `0001`: guardians, learners, parental_consents, diagnostic_sessions, study_plans, audit_log
- `ConsentService` — POPIA parental consent service layer with grant/revoke/erasure
- `ParentalConsent` ORM model with `is_active` property and annual renewal logic
- IRT-based diagnostic engine (scikit-learn, numpy, scipy)
- LLM lesson generation via Anthropic Claude and Groq (with pseudonym_id isolation)
- Celery + Redis async task queue with Beat scheduler
- Prometheus + Grafana observability stack
- Docker Compose local development stack (9 services)
- GitHub Actions CI skeleton (lint + test)
- AGENT_INSTRUCTIONS.md TDD-loop paradigm for autonomous agents

### Security
- Emails stored as SHA-256 hash + pgcrypto-encrypted ciphertext (never plaintext)
- Learner real UUID never sent to LLM providers — pseudonym_id used exclusively
- Soft-delete pattern for right-to-erasure (POPIA Section 24)
- Annual consent renewal enforced via `expires_at` column

---

[Unreleased]: https://github.com/NkgoloL/edo-boost-main/compare/v0.1.0-beta...HEAD
[0.1.0-beta]: https://github.com/NkgoloL/edo-boost-main/releases/tag/v0.1.0-beta
