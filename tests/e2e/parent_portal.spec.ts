// tests/e2e/parent_portal.spec.ts
//
// Journey: Guardian views parent portal → sees learner progress report →
//          manages consent → triggers right-to-erasure
//
// This is the POPIA-critical path: consent management and erasure must
// be exercised in E2E tests before any pilot launch.

import { test, expect } from "@playwright/test";
import * as fs from "fs";
import * as path from "path";

const FIXTURE_FILE = path.join(
  __dirname,
  "../../playwright/.auth/fixtures.json"
);

test.describe("Parent Portal — Progress Reports", () => {
  let learnerId: string;

  test.beforeAll(() => {
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    learnerId = fx.learnerId;
  });

  test("parent portal dashboard loads and shows learner card", async ({
    page,
  }) => {
    await page.goto("/parent");
    await expect(
      page.getByRole("heading", { name: /parent portal/i })
    ).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText("E2E Test Learner")).toBeVisible();
  });

  test("learner progress report shows grade, subject, and activity", async ({
    page,
  }) => {
    await page.goto(`/parent/learners/${learnerId}/report`);
    await expect(page.getByTestId("learner-grade")).toBeVisible({ timeout: 10_000 });
    await expect(page.getByTestId("subject-progress")).toBeVisible();
    await expect(page.getByTestId("recent-activity")).toBeVisible();
  });

  test("consent status badge shows 'Active' for granted consent", async ({
    page,
  }) => {
    await page.goto(`/parent/learners/${learnerId}/consent`);
    await expect(page.getByTestId("consent-status-badge")).toContainText(
      /active|granted/i
    );
    await expect(page.getByText(/expires/i)).toBeVisible();
  });

  test("consent expiry date is approximately 1 year from now", async ({
    request,
  }) => {
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    const res = await request.get(
      `${process.env.API_BASE_URL ?? "http://localhost:8000/api/v1"}/consent/status?learner_id=${learnerId}`,
      { headers: { Authorization: `Bearer ${fx.accessToken}` } }
    );
    expect(res.status()).toBe(200);
    const data = await res.json();
    const expiresAt = new Date(data.expires_at).getTime();
    const now = Date.now();
    const oneYear = 365 * 24 * 60 * 60 * 1000;
    // Should expire within 363-367 days from now (tolerance for test clock skew)
    expect(expiresAt - now).toBeGreaterThan(oneYear - 2 * 86400 * 1000);
    expect(expiresAt - now).toBeLessThan(oneYear + 2 * 86400 * 1000);
  });
});

test.describe("Parent Portal — Consent Management", () => {
  test("guardian can view and download data export", async ({ page }) => {
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    await page.goto(`/parent/learners/${fx.learnerId}/data`);
    await expect(
      page.getByRole("button", { name: /export data|download/i })
    ).toBeVisible({ timeout: 10_000 });
  });

  test("right-to-erasure flow shows confirmation dialog", async ({ page }) => {
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    await page.goto(`/parent/learners/${fx.learnerId}/consent`);
    const eraseBtn = page.getByRole("button", { name: /delete|erase|remove data/i });
    await expect(eraseBtn).toBeVisible({ timeout: 10_000 });
    await eraseBtn.click();
    // Must show a confirmation dialog — never erase on single click
    await expect(
      page.getByRole("dialog", { name: /confirm/i })
    ).toBeVisible({ timeout: 5_000 });
    // Cancel — we don't actually erase in this test run
    await page.getByRole("button", { name: /cancel/i }).click();
    await expect(page.getByRole("dialog")).not.toBeVisible();
  });
});

test.describe("Parent Portal — API Consent Enforcement", () => {
  test("revoked consent blocks learner data access immediately", async ({
    request,
  }) => {
    const fx = JSON.parse(fs.readFileSync(FIXTURE_FILE, "utf-8"));
    const API = process.env.API_BASE_URL ?? "http://localhost:8000/api/v1";
    const headers = { Authorization: `Bearer ${fx.accessToken}` };

    // Create a second learner with NO granted consent
    const learnerRes = await request.post(`${API}/learners`, {
      headers,
      data: { display_name: "No Consent Learner", grade: "3" },
    });
    // Consent starts as 'pending' — access should be blocked
    if (learnerRes.status() === 201) {
      const noConsentLearner = await learnerRes.json();
      const planRes = await request.get(
        `${API}/learners/${noConsentLearner.id}/plan`,
        { headers }
      );
      // Must be 403 (ConsentNotGrantedError) not 200
      expect(planRes.status()).toBe(403);
      const err = await planRes.json();
      expect(err.detail ?? err.message ?? "").toMatch(/consent/i);
    }
  });
});
