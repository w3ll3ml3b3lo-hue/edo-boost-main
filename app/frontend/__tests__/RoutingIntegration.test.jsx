import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { LearnerProvider } from "../src/context/LearnerContext";
import DashboardPage from "../src/app/(learner)/dashboard/page";
import LessonPage from "../src/app/(learner)/lesson/page";
import DiagnosticPage from "../src/app/(learner)/diagnostic/page";

// Mock next/navigation
const mockPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
  usePathname: () => "/dashboard",
}));

// Mock the components used in pages to avoid massive dependency chain
vi.mock("../src/components/eduboost/FeaturePanels", () => ({
  DashboardPanel: ({ onStartLesson, onStartDiag }) => (
    <div>
      <button onClick={onStartLesson}>Start lesson</button>
      <button onClick={onStartDiag}>Open diagnostic</button>
    </div>
  ),
  LessonPanel: ({ onComplete, onBack }) => (
    <div>
      <button onClick={() => onComplete(10)}>Complete Lesson</button>
      <button onClick={onBack}>Back</button>
    </div>
  ),
}));

vi.mock("../src/components/eduboost/InteractiveDiagnostic", () => ({
  InteractiveDiagnostic: ({ onComplete, onBack }) => (
    <div>
      <button onClick={() => onComplete("MATH", 80)}>Complete Diagnostic</button>
      <button onClick={onBack}>Back</button>
    </div>
  ),
}));

describe("Routing Integration", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("Dashboard routes to /lesson and /diagnostic (NOT /learner/*)", () => {
    render(
      <LearnerProvider>
        <DashboardPage />
      </LearnerProvider>
    );

    fireEvent.click(screen.getByText("Start lesson"));
    expect(mockPush).toHaveBeenCalledWith("/lesson");

    fireEvent.click(screen.getByText("Open diagnostic"));
    expect(mockPush).toHaveBeenCalledWith("/diagnostic");
  });

  it("Lesson page routes back to /dashboard", () => {
    render(
      <LearnerProvider>
        <LessonPage />
      </LearnerProvider>
    );

    fireEvent.click(screen.getByText("Back"));
    expect(mockPush).toHaveBeenCalledWith("/dashboard");
    
    fireEvent.click(screen.getByText("Complete Lesson"));
    expect(mockPush).toHaveBeenCalledWith("/dashboard");
  });

  it("Diagnostic page routes to /plan and /dashboard", () => {
    render(
      <LearnerProvider>
        <DiagnosticPage />
      </LearnerProvider>
    );

    fireEvent.click(screen.getByText("Back"));
    expect(mockPush).toHaveBeenCalledWith("/dashboard");

    fireEvent.click(screen.getByText("Complete Diagnostic"));
    expect(mockPush).toHaveBeenCalledWith("/plan");
  });
});
