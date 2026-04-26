import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { DashboardPanel, DiagnosticPanel } from "../src/components/eduboost/FeaturePanels";
import { LearnerProvider } from "../src/context/LearnerContext";

// Mock the API calls so we don't try to fetch during tests
vi.mock("../src/components/eduboost/api", () => ({
  getLearnerMasteryAPI: vi.fn().mockResolvedValue({ mastery: [] }),
  runDiagnosticAPI: vi.fn().mockResolvedValue({ gap_report: { mastery_score: 0.85 } }),
  awardXPAPI: vi.fn().mockResolvedValue({ success: true }),
  getLearnerProfileAPI: vi.fn().mockResolvedValue({ level: 2, total_xp: 150 }),
}));

describe("DashboardPanel", () => {
  it("renders the welcome message and overall mastery", () => {
    const mockLearner = { nickname: "TestUser", grade: 4 };
    const mockMastery = { MATH: 50, ENG: 70 };

    render(
      <LearnerProvider>
        <DashboardPanel
          learner={mockLearner}
          masteryData={mockMastery}
          onStartLesson={vi.fn()}
          onStartDiag={vi.fn()}
        />
      </LearnerProvider>
    );

    expect(screen.getByText(/Welcome, TestUser!/i)).toBeInTheDocument();
    expect(screen.getByText(/Overall mastery:/i)).toBeInTheDocument();
    expect(screen.getByText("60%")).toBeInTheDocument(); // (50+70)/2
  });
});

describe("DiagnosticPanel", () => {
  it("allows selecting a subject and submitting", async () => {
    const mockLearner = { nickname: "TestUser", grade: 4 };
    const mockOnComplete = vi.fn();

    render(
      <LearnerProvider>
        <DiagnosticPanel
          learner={mockLearner}
          onComplete={mockOnComplete}
          onBack={vi.fn()}
        />
      </LearnerProvider>
    );

    // Click Math subject
    const mathButton = screen.getByText("Mathematics");
    fireEvent.click(mathButton);

    // Verify it allows running diagnostic
    const runButton = screen.getByText("Run Diagnostic");
    expect(runButton).not.toBeDisabled();
    
    // Simulate clicking
    fireEvent.click(runButton);
    expect(screen.getByText("Running IRT...")).toBeInTheDocument();
  });
});
