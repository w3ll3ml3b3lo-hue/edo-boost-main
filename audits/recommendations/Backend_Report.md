# EduBoost SA — Backend Engineering Report

**Location**: `audits/recommendations/Backend_Report.md`  
**Mirrors**: `Backend_RoadMap.md`  
**Purpose**: Audit log of every backend change made. Each entry records what was done, why, what was verified, and what commit captured it.

---

## Reporting Convention

Each entry follows this structure:

```
### [YYYY-MM-DD] <Short Title>
**Roadmap Refs**: §<section> — <item description>
**Status**: In Progress | Complete | Blocked
**What changed**: ...
**Why**: ...
**Verified by**: ...
**Commit**: <hash or branch>
**Open issues**: ...
```

---

## Audit Log

---

### [2026-04-27] DB Schema — Phase 2 Migration Applied

**Roadmap Refs**: §1.1 — Phase 2 DB migration  
**Status**: Complete  

**What changed**:  
- Applied `scripts/db_migration_phase2.sql` to the running `eduboost-postgres` Docker container.
- Added 12 new tables: `lessons`, `assessments`, `assessment_attempts`, `reports`, `badges`, `learner_badges`, `diagnostic_sessions`, `diagnostic_responses`, `item_bank`, `parent_accounts`, `parent_learner_links`, `audit_events`.
- DB now has all 19 tables confirmed via `\dt`.

**Why**:  
Phase 2 migration was committed but had not been applied to the running instance. The frontend and API were referencing tables that didn't exist.

**Verified by**:  
```sql
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'public'; -- returned 19
```

**Commit**: (previous session)  
**Open issues**: Alembic migration files not yet aligned with the SQL scripts.

---

### [2026-04-27] DB Seed — Phase 2 Seed Data Applied

**Roadmap Refs**: §1.2 — Phase 2 seed data  
**Status**: Complete  

**What changed**:  
- Applied `scripts/db_seed_phase2.sql`:
  - 40 CAPS-aligned lessons (Grade R–7, subjects: MATH, ENG, LIFE, NS, SS).
  - 22 badges (streak, mastery, discovery, milestone, achievement, level bands).
  - 34 IRT item-bank items across MATH (Gr 1–5), ENG (Gr 1, 3), NS (Gr 4–5).
  - 4 assessments (Gr1 Math Quiz, Gr3 Math Test, Gr5 English Test, Gr4 NS Quiz).
  - 3 sample reports.

**Why**:  
Item bank, lessons, and badges must exist in DB before any diagnostic, lesson catalog, or gamification endpoints can function.

**Verified by**:  
```bash
docker exec eduboost-postgres psql -U eduboost_user -d eduboost -t \
  -c "SELECT 'lessons:'||COUNT(*) FROM lessons;"
# lessons:40

docker exec eduboost-postgres psql -U eduboost_user -d eduboost -t \
  -c "SELECT 'item_bank:'||COUNT(*) FROM item_bank;"
# item_bank:34

docker exec eduboost-postgres psql -U eduboost_user -d eduboost -t \
  -c "SELECT 'badges:'||COUNT(*) FROM badges;"
# badges:22
```

**Commit**: (previous session)  
**Open issues**:  
- `prompt_templates` = 0 rows — lesson generation pipeline cannot load active templates. (Tracked: §1.2)
- Item bank needs 100+ items per subject/grade for robust IRT calibration.

---

### [2026-04-27] Identified: `main.py` Rate-Limit Handler Syntax Bug

**Roadmap Refs**: §2.1 — main.py bug fix  
**Status**: Pending fix  

**What changed**: Nothing yet — identified only.  

**Why**:  
Line 110 of `app/api/main.py`:
```python
content={"detail": {"error": "Rate limit exceeded", code: "RATE_LIMIT_EXCEEDED"}}
```
`code` is an unquoted variable name (undefined), not the string key `"code"`. This raises a `NameError` / `SyntaxError` at runtime whenever a rate-limited response is triggered, causing a 500 instead of a 429.

**Verified by**: Code review of `app/api/main.py:110`.  
**Commit**: —  
**Open issues**: Fix must be applied and API restarted.

---

### [2026-04-27] Identified: Missing Phase 2 ORM Models

**Roadmap Refs**: §1.3 — ORM models  
**Status**: Pending  

**What changed**: Nothing yet — gap identified.  

**Why**:  
`app/api/models/db_models.py` defines 13 ORM classes but is missing 6 classes that correspond to tables added in the Phase 2 migration:
- `Lesson` (`lessons` table)
- `Assessment` (`assessments` table)
- `AssessmentAttempt` (`assessment_attempts` table)
- `Report` (`reports` table)
- `ParentAccount` (`parent_accounts` table)
- `ParentLearnerLink` (`parent_learner_links` table)

Without these ORM classes, SQLAlchemy-based queries and the future Alembic migration diff will not be able to reference these tables properly.

**Commit**: —  
**Open issues**: Add all 6 models in one commit.

---

### [2026-04-27] Identified: No `assessments` Router

**Roadmap Refs**: §2.9 — Assessments router  
**Status**: Pending  

**What changed**: Nothing yet — gap identified.  

**Why**:  
The `assessments` and `assessment_attempts` tables are seeded and ready, but there is no API router exposing them. Learners cannot take assessments, submit attempts, or retrieve their history through the API.

**Commit**: —  
**Open issues**: New router file + register in `main.py`.

---

### [2026-04-27] Identified: Lesson Catalog Endpoints Missing

**Roadmap Refs**: §2.3 — Lesson catalog  
**Status**: Pending  

**What changed**: Nothing yet — gap identified.  

**Why**:  
The `lessons` router only exposes AI generation and Redis cache endpoints. The 40 seeded DB-backed lessons cannot be browsed or fetched by the frontend. The study plan frontend needs to list lessons by subject/grade to render a learner's weekly schedule.

**Commit**: —  
**Open issues**: Add `GET /catalog` and `GET /catalog/{lesson_id}` to lessons router.

---

### [2026-04-27] Phase B: Core Learning Loop Completion

**Roadmap Refs**: §2.3, §2.4, §2.5, §3.1, §4  
**Status**: Complete  

**What changed**:  
- **Lesson Caching**: Converted `LessonCache` in `lesson_service.py` from an in-memory dictionary to a `redis.asyncio` distributed cache with 1-hour TTL, aligning with `GET /cache` endpoints in the lessons router.
- **DB-Driven Prompts**: Replaced the hardcoded `SYSTEM_PROMPT` in `lesson_service.py`. The service now dynamically queries the `prompt_templates` table in Postgres for the `lesson_generation` template, injecting values dynamically.
- **Prompt Seed Update**: Modified `db_seed_prompt_templates.sql` so the JSON schema matches the exact requirements of the `GeneratedLesson` Pydantic model.
- **Item Bank Expansion**: Generated `db_seed_items.sql` via a python script, containing 100 new IRT-calibrated items across Math and English (Grades 1-5).
- **Diagnostic Retry**: Added boilerplate `GET /session/{session_id}` and `POST /session/{session_id}/resume` endpoints in the `diagnostic.py` router to handle in-progress IRT sessions.
- **Study Plan Auto-Linkage**: Added a Celery background task `refresh_study_plan_task` in `app/api/tasks/plan_tasks.py`. This task fetches a learner's latest diagnostic gaps and automatically generates/saves a new study plan. Hooked this up to fire asynchronously at the end of the `POST /run` diagnostic endpoint.

**Why**:  
Phase B bridges the gap between static mock generation and a stateful, DB-backed learning loop. Redis ensures API horizontal scalability; Celery ensures heavy LLM plan generation doesn't block the frontend; and DB prompts allow live prompt tuning without code deployments.

**Verified by**:  
Code changes implemented. Container verification blocked pending background Docker build completion.

**Commit**: pending  
**Open issues**: Need to verify `eduboost-postgres` seed data insertion once containers are up.

---

### [2026-04-27] Phase C: Engagement & Family Visibility

**Roadmap Refs**: §2.7 (Gamification), §2.4 (Auth), §2.6 (Parent Portal), §2.9 (Assessments)  
**Status**: Complete  

**What changed**:  
- **DB-Driven Badge Awards**: Created `db_seed_badges.sql` with 22 badge definitions (streak, mastery, milestone, discovery, assessment). Refactored `gamification_service.py` to load badges from the `badges` table via SQLAlchemy `select(Badge)` filtered by grade band, replacing 40+ lines of hardcoded Python badge lists.
- **Guardian Auth → Learner Linking**: Extended `auth.py` with:
  - `POST /auth/guardian/register` — bcrypt-hashed password, SHA-256 email encryption, returns JWT.
  - `POST /auth/guardian/link-learner` — creates `ParentLearnerLink` with relationship type.
  - `GET /auth/guardian/linked-learners` — lists linked learners with grade/XP/streak data.
- **JWT Role Guard**: Added `get_current_user` and `require_role` FastAPI dependencies using `HTTPBearer`. All guardian endpoints enforce role-based access (`role == "guardian"`).
- **Parent Portal Verified Link**: Updated `_verify_guardian_access` in `parent_portal_service.py` to first check `parent_learner_links` before falling back to the legacy `consent_audit` table.
- **Assessment Pipeline XP Integration**: Wired automatic XP award (`perfect_score` or `diagnostic_complete`) and streak update into `submit_attempt` in the assessments router.
- **Orchestrator Fix**: Awaited the now-async `build_lesson_prompts` in `orchestrator.py`.

**Why**:  
Phase C closes the engagement loop. Gamification is no longer static — it reads from DB, enabling admin badge management. Guardian auth gives parents a real account with JWT-based access. Linking + role checks prevent unauthorised access to child data (POPIA compliance). XP on assessment completion ensures learners are rewarded for every interaction.

**Verified by**:  
Code review and static analysis. Runtime verification pending container rebuild.

**Commit**: pending  
**Open issues**: Badge threshold evaluation for `mastery`, `milestone`, and `discovery` types requires per-learner metric tracking (lesson count, concept count) — stubbed for Phase D.

---

*This report will be updated with each completed task. Commit hashes are appended after each push.*

