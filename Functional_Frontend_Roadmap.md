# EduBoost SA — Functional Frontend Roadmap (V2)

**Last Updated:** April 27, 2026  
**Status:** 🟠 Amber (Moving from Mock to Mission-Critical)

## 🎯 Primary Objective
Transition the frontend from a "stub-heavy" React mockup to a production-grade Next.js application that is fully wired to the stateful backend Orchestrator, with a strict "No Mock" testing policy for integration.

---

## 🏗️ Phase 1: Architectural Integrity (Immediate)
*Goal: Fix the "plumbing" so links work and identity is consistent.*

- [x] **Fix Routing Mismatches**:
    - ✅ Updated `LearnerLayout` and all `router.push` calls to use standardized paths
    - ✅ Removed hardcoded `/learner/` prefixes from all internal navigation
- [x] **Establish Session Persistence**:
    - ✅ Implemented `useEffect` in `LearnerContext` to sync with `localStorage`
- [ ] **API Layer Consolidation**:
    - Deprecate `src/components/eduboost/api.js`.
    - Migrated all calls to `src/lib/api/services.js`.
    - Ensure all calls use the identity stored in `LearnerContext`.

## 🎨 Phase 2: Feature Decomposition (The "Anti-JSP" Move)
*Goal: Destroy the monolithic FeaturePanels.jsx and build real pages.*

- [ ] **Decompose Panels**:
    - Move `LessonPanel` logic to `app/(learner)/lesson/page.jsx`.
    - Move `DiagnosticPanel` logic to `app/(learner)/diagnostic/page.jsx`.
    - Move `StudyPlanPanel` logic to `app/(learner)/plan/page.jsx`.
- [ ] **Eliminate `PlaceholderPanel`**:
    - Replace the generic wrapper with specialized, high-fidelity UI components using the established design system (Tailwind + Framer Motion).
- [ ] **Interactive IRT UI**:
    - Build a real step-by-step diagnostic flow that renders questions one by one from the backend, instead of a "Run Diagnostic" stub button.

## 🔗 Phase 3: Real-Time Backend Sync
*Goal: Ensure the UI state matches the DB state at all times.*

- [ ] **Context-Driven Mastery**:
    - Move mastery data into a global state (Zustand or optimized Context) that updates automatically after lessons/diagnostics.
- [ ] **Gamification Wiring**:
    - Wire the `Sidebar` XP bar to the real gamification profile service.
    - Implement real-time "Level Up" and "Badge Awarded" notifications via a global Toast/Popup system.

## 🧪 Phase 4: Strict Functional Testing
*Goal: Stop the "Green Test / Broken App" delusion.*

- [ ] **Contract Testing**:
    - Introduce Vitest tests that validate the `Service` layer against the real Pydantic schemas (using mock data that matches the schema exactly).
- [ ] **Integration-Heavy Component Tests**:
    - Rework `__tests__` to test components wrapped in `LearnerProvider`.
    - Stop mocking the `Service` layer; instead, mock the network layer (MSW) to ensure the component is actually sending the right HTTP requests.
- [ ] **E2E Smoke Tests**:
    - Implement basic Playwright/Cypress flows for:
        1. Login -> Dashboard.
        2. Dashboard -> Lesson -> XP Awarded.
        3. Dashboard -> Diagnostic -> Mastery Update.

---

## 🚦 Success Metrics
1. **Zero 404s** on internal links.
2. **Zero `PlaceholderPanel`** usages in the `(learner)` group.
3. **Tests Fail** if the backend API endpoint changes its signature.
4. **Persistent Session** after a browser refresh. ✅
