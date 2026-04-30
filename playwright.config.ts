// playwright.config.ts
//
// EduBoost SA — Playwright E2E Test Configuration
//
// Covers the four critical user journeys identified in the technical report:
//   1. Guardian consent flow
//   2. Diagnostic assessment
//   3. Study plan generation
//   4. Lesson delivery
//   5. Parent portal / report view
//
// Run locally:
//   npx playwright test
//
// Run in CI:
//   npx playwright test --project=chromium

import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,   // Sequential: flows depend on shared DB state
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 2,

  reporter: [
    ["list"],
    ["html", { outputFolder: "playwright-report", open: "never" }],
    ["junit", { outputFile: "playwright-results.xml" }],
  ],

  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    // API base URL for direct API assertions
    extraHTTPHeaders: {
      "Accept": "application/json",
    },
  },

  projects: [
    // Setup: create guardian + learner accounts once, store auth state
    {
      name: "setup",
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        storageState: "playwright/.auth/guardian.json",
      },
      dependencies: ["setup"],
    },
    {
      name: "mobile",
      use: {
        ...devices["Pixel 7"],
        storageState: "playwright/.auth/guardian.json",
      },
      dependencies: ["setup"],
    },
  ],

  // Start the dev stack before running tests locally
  webServer: process.env.CI
    ? undefined
    : {
        command: "docker-compose up -d && sleep 15",
        url: "http://localhost:3000",
        reuseExistingServer: true,
        timeout: 120_000,
      },
});
