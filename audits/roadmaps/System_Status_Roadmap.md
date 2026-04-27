# EduBoost SA — System Status Roadmap

**Last Updated:** April 27, 2026  
**Status:** 🟢 Active  

This roadmap outlines the core functionalities and capabilities of the EduBoost SA system. Each entry below has a corresponding detail block in the [System Status Report](../reports/System_Status_Report.md) for current implementation details and status checks.

## System Capabilities

### 1. Authentication & Security
- [ ] Implement JWT-based authentication for Learners and Guardians.
- [ ] Enforce POPIA-compliant data deletion mechanisms.
- [ ] Secure password hashing and token lifecycle management.

### 2. Constitutional AI & Judiciary Pipeline
- [ ] Validate and sanitize all LLM responses against educational guidelines.
- [ ] Implement PII scrubbing to prevent data leakage.
- [ ] Apply Subject-specific pedagogical rules (Maths vs Language).

### 3. Adaptive Diagnostics (IRT Engine)
- [ ] Deploy stateful Item Response Theory assessment sessions.
- [ ] Generate baseline capability reports from initial evaluations.
- [ ] Real-time gap detection and reporting.

### 4. Personalised Study Plan Generation
- [ ] Orchestrate weekly plan generation using OpenAI/Anthropic APIs.
- [ ] Map diagnostic gaps to specific learning objectives.
- [ ] Celery-driven background processing for automated plan renewal.

### 5. Interactive Learning & Execution
- [ ] Deliver dynamic lesson content with interactive components.
- [ ] Track Time-on-Task and granular mastery progress.
- [ ] Implement robust offline caching and Service Worker synchronization.

### 6. Gamification Engine
- [ ] Calculate and award XP for lesson completion.
- [ ] Track consecutive daily activity streaks.
- [ ] Unlock level progression and distribute achievement badges.

### 7. Parent Portal & Guardian Reporting
- [ ] Provide high-level progress dashboards for guardians.
- [ ] Support granular consent management and data requests.
- [ ] Generate comprehensive parent-friendly performance reports.

### 8. Auditing & Logging (Fourth Estate)
- [ ] Immutable event tracking for PII, Consent, and System mutations.
- [ ] Centralized Redis-backed event bus.
- [ ] Circuit-breaker fallbacks and structured local logging.

### 9. Infrastructure & Tooling
- [ ] Post-startup Dummy Data Generator for demo/dev environments.
- [ ] Alembic-driven database migrations and schema drift detection.
- [ ] Prometheus metrics and Grafana observability stack.
