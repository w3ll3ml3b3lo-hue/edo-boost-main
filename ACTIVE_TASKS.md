## Active Tasks (Agent Execution)

This file is the **authoritative checklist** for the work currently being executed in this repository.  
Each item should be closed only when implemented, verified (tests or runtime validation), and committed.

### Scope: Backend functional verification + dummy data generator

- [ ] **Docs scaffolding**
  - [ ] Add/maintain this task list (`ACTIVE_TASKS.md`)
  - [ ] Add/maintain an implementation log (`audits/recommendations/Implementation_Report.md`)

- [ ] **Backend: functional verification**
  - [ ] Ensure `pytest` runs in a local venv without Docker and without external LLM keys
  - [ ] Make integration tests deterministic by stubbing inference in `APP_ENV=test`
  - [ ] Fix any failing routers/services uncovered by tests until suite is green

- [ ] **Dummy data generation (post-startup, silent)**
  - [ ] Implement generator modules (DB writers) capable of creating up to **10,000** dummy records
  - [ ] Ensure generation begins **only after** the API is up (post-startup background task)
  - [ ] Make generation **silent** (no noisy logs; only errors should surface)
  - [ ] Add idempotency/locking so multiple workers don’t double-generate

- [ ] **Persistence floor**
  - [ ] Keep **1/3 to 1/2** of generated dummy data persisted at all times
  - [ ] Implement cleanup/rotation that never drops below the persistence floor
  - [ ] Add configuration knobs (target size, floor ratio, cadence)

- [ ] **Commits**
  - [ ] Commit in small batches after each milestone (docs → backend green → generator → persistence floor)

