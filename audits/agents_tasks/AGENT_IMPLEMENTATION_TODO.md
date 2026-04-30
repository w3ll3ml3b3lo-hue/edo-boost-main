# Agent Implementation TODO

## 🏁 Current Milestone: Production Hardening & Long-Term Roadmap (COMPLETED)
All recommendations from the Technical Assessment Report (#15) have been implemented.

- [x] **Alembic Baseline**: Consolidated all schema management.
- [x] **Consent Gating**: Backend-enforced POPIA checkpoints.
- [x] **Fourth Estate**: Migrated to durable RabbitMQ audit trail.
- [x] **CI/CD**: Semantic versioning and release automation.
- [x] **Observability**: Expanded Grafana dashboards.
- [x] **E2E Testing**: Playwright suite implemented.

## 🚀 Next Milestone: Pilot Readiness & Scaling
The following tasks are targeted for the next phase of development.

### 1. Production Deployment & Reliability
- [ ] Execute trial production deployment using `docker-compose.prod.yml`.
- [ ] Implement database backup and automated restore drills.
- [ ] Stress-test RabbitMQ and Celery under concurrent learner load.

### 2. Pedagogy & Content Hardening
- [ ] Formalize CAPS-alignment validation rules for Grade 4-7.
- [x] Implement multi-language lesson generation for Zulu, Xhosa and Afrikaans.
- [ ] Expand the IRT Item Bank with calibrated CAPS items.

### 3. Frontend UX & Accessibility
- [ ] Conduct WCAG 2.1 accessibility audit for the Learner Dashboard.
- [x] Implement "Offline First" lesson synchronization (PWA).
- [ ] Enhance Parent Portal with downloadable progress PDF reports.

### 4. AI Governance
- [x] Implement prompt versioning and A/B testing framework (PromptManager).
- [x] Add RLHF (Reinforcement Learning from Human Feedback) loop for lesson quality.
- [x] Integrate real-time content moderation for LLM outputs (Judiciary).