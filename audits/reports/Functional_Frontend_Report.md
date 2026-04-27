# EduBoost SA — Functional Frontend Report

**Generated:** April 27, 2026
**Purpose:** An uncompromising audit of the frontend state, acknowledging the gaps between the UI presentation and the actual backend capabilities.

---

## 1. The Disconnect: Why it feels like a "1-Page JSP"

Despite the backend having a fully functional Orchestrator, multi-step IRT diagnostics, and real DB persistence, the frontend is stranded in "Phase 0". 

### 1.1 The `FeaturePanels` Anti-Pattern
The entire application relies on `app/frontend/src/components/eduboost/FeaturePanels.jsx`. Inside this file, every major feature (Dashboard, Diagnostics, Study Plan, Parent Portal) is rendered using a `PlaceholderPanel`.
- **Impact:** The user experiences a title, a brief description, and a button. There is no real UI logic, no forms, no data visualization.
- **Resolution:** `FeaturePanels.jsx` must be deleted. Each App Router page (e.g., `app/(learner)/dashboard/page.jsx`) must build its own specific UI.

### 1.2 Dead Navigation
The `Sidebar` component assumes the learner routes are namespaced under `/learner/[tabId]`. However, the Next.js `(learner)` route group mounts them at the root level (e.g., `/dashboard`).
- **Impact:** Clicking on any sidebar link results in a 404 Error.
- **Resolution:** The routing paths in `Sidebar` must be updated to match the actual file structure.

### 1.3 State Loss and Login Bypassing
The `LearnerContext` handles global state, but the `LoginPage` attempts to bypass login by pushing directly to `/dashboard` without initializing the context.
- **Impact:** The `LearnerLayout` sees `learner === null` and immediately redirects the user back to the home page `/`, creating an infinite loop or a confusing boot-out.
- **Resolution:** The application needs a robust, testable mock state for development, or the frontend must be forced to use the real `/learners/` registration endpoint.

---

## 2. API Connectivity Chaos

### 2.1 The Two API Clients
The codebase currently contains:
1. `app/frontend/src/components/eduboost/api.js` — The legacy file containing `localStorage` mock logic and outdated endpoint assumptions.
2. `app/frontend/src/lib/api/services.js` — The new, production-grade service file that correctly uses JWTs and the `fetchApi` wrapper.

- **Impact:** The `FeaturePanels.jsx` is still importing from the legacy `api.js`. The frontend is literally ignoring the new backend endpoints.
- **Resolution:** Delete `api.js` and rewire every page to use `services.js`.

---

## 3. The Testing Delusion

### 3.1 Why Tests Pass When the App is Broken
The current test suite (Vitest/React Testing Library) is testing isolated component rendering with mocked dependencies. 
- Example: The test asserts that a `<DashboardPanel />` renders the text "Welcome". It does not test if the "Start Lesson" button routes to the correct page, or if the API call fetches real data.
- **Impact:** High test coverage provides false confidence. We are optimizing for green ticks instead of functional user journeys.

### 3.2 The Path to Strict Testing
We must implement a stricter testing philosophy:
1. **End-to-End Dominance:** Use Playwright to spin up the actual Next.js server and the FastAPI backend (in Test Mode), and simulate a user clicking through the flow.
2. **Integration Tests over Unit Tests:** Frontend tests should use MSW (Mock Service Worker) to mock HTTP requests at the network level, not at the React hook level. This ensures the components are generating correct request payloads.

---

## 4. Immediate Remediation Plan (Next Steps)

1. **Delete `api.js`** and refactor `FeaturePanels.jsx` to use `services.js`.
2. **Fix `Sidebar` routing** to eliminate 404s.
3. **Setup Playwright** for strict E2E validation.
4. **Build the real `DiagnosticPanel` UI** to replace the `PlaceholderPanel`.
