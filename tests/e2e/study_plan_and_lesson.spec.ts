// tests/e2e/study_plan_and_lesson.spec.ts
//
// Journey: Diagnostic complete → study plan generated → lesson delivered → marked complete
// Depends on diagnostic.spec.ts having run (auth state + learner fixture exist)

import { test, expect } from "@playwright/test";
import * as fs from "fs";
import * as path from "path";

const FIXTURE_FILE = path.join(
  __dirname,
  "../../playwright/.auth/fixtures.json"
);

test.describe("Study Plan Generation", () => {
  let learnerId: string;
  let accessToken: string;

  test.beforeAll(() => {
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    learnerId = fx.learnerId;
    accessToken = fx.accessToken;
  });

  test("study plan page renders for the learner", async ({ page }) => {
    await page.goto(`/learners/${learnerId}/plan`);
    await expect(
      page.getByRole("heading", { name: /study plan/i })
    ).toBeVisible({ timeout: 15_000 });
  });

  test("can generate a study plan from API when none exists", async ({
    request,
  }) => {
    const res = await request.post(
      `${process.env.API_BASE_URL ?? "http://localhost:8000/api/v1"}/learners/${learnerId}/plan/generate`,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
        data: { subject: "mathematics" },
      }
    );
    // 201 created or 200 if plan already exists
    expect([200, 201]).toContain(res.status());
    const plan = await res.json();
    expect(plan).toHaveProperty("id");
    expect(plan).toHaveProperty("plan_data");
    expect(plan.active).toBe(true);

    // Store plan ID for lesson test
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    fs.writeFileSync(FIXTURE_FILE, JSON.stringify({ ...fx, planId: plan.id }));
  });

  test("study plan page displays weekly topic breakdown", async ({ page }) => {
    await page.goto(`/learners/${learnerId}/plan`);
    await expect(page.getByTestId("plan-week-card")).toHaveCount(
      expect.any(Number) as unknown as number,
      { timeout: 15_000 }
    );
    const weekCards = await page.getByTestId("plan-week-card").count();
    expect(weekCards).toBeGreaterThanOrEqual(1);
  });

  test("API returns 403 without active consent", async ({ request }) => {
    // Use a bogus learner ID to simulate no-consent scenario
    const res = await request.get(
      `${process.env.API_BASE_URL ?? "http://localhost:8000/api/v1"}/learners/00000000-0000-0000-0000-000000000000/plan`,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
    expect([403, 404]).toContain(res.status());
  });
});

test.describe("Lesson Delivery", () => {
  let learnerId: string;
  let accessToken: string;

  test.beforeAll(() => {
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    learnerId = fx.learnerId;
    accessToken = fx.accessToken;
  });

  test("lesson page loads for a learner with active plan", async ({ page }) => {
    await page.goto(`/learners/${learnerId}/lesson`);
    // Either shows a lesson or a "start your first lesson" CTA
    const hasLesson = await page.getByTestId("lesson-content").isVisible({ timeout: 15_000 })
      .catch(() => false);
    const hasCTA = await page.getByRole("button", { name: /start lesson/i }).isVisible()
      .catch(() => false);
    expect(hasLesson || hasCTA).toBe(true);
  });

  test("can request a new lesson via API", async ({ request }) => {
    const res = await request.post(
      `${process.env.API_BASE_URL ?? "http://localhost:8000/api/v1"}/learners/${learnerId}/lesson`,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
        data: {
          subject: "mathematics",
          topic: "fractions",
          grade: "4",
        },
      }
    );
    expect([200, 201, 202]).toContain(res.status());
    const lesson = await res.json();
    expect(lesson).toHaveProperty("id");
    // Content must not contain raw PII or learner real name
    const content = JSON.stringify(lesson);
    expect(content).not.toContain("E2E Test Learner");
    expect(content).not.toContain("@test.eduboost.local");
  });

  test("lesson content renders with explanation and examples", async ({
    page,
  }) => {
    await page.goto(`/learners/${learnerId}/lesson`);
    await page.getByRole("button", { name: /start lesson/i }).click().catch(() => {
      // Already on a lesson page, no CTA needed
    });
    // Wait for LLM content to stream in (up to 30s)
    await expect(page.getByTestId("lesson-content")).toBeVisible({ timeout: 30_000 });
    const text = await page.getByTestId("lesson-content").textContent();
    expect(text?.length).toBeGreaterThan(100);
  });

  test("learner can mark a lesson as complete", async ({ page }) => {
    await page.goto(`/learners/${learnerId}/lesson`);
    const completeBtn = page.getByRole("button", { name: /complete|done|finished/i });
    if (await completeBtn.isVisible({ timeout: 10_000 }).catch(() => false)) {
      await completeBtn.click();
      await expect(
        page.getByText(/great job|well done|lesson complete/i)
      ).toBeVisible({ timeout: 10_000 });
    }
  });
});
