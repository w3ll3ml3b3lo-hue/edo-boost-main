"use client";

import { useRouter } from "next/navigation";
import { useLearner } from "../../../../context/LearnerContext";
import { DiagnosticPanel } from "../../../../components/eduboost/FeaturePanels";

export default function DiagnosticPage() {
  const { learner, setMasteryData } = useLearner();
  const router = useRouter();

  return (
    <DiagnosticPanel
      learner={learner}
      onComplete={(subject, mastery) => {
        setMasteryData((prev) => ({ ...prev, [subject]: mastery }));
        router.push("/learner/plan");
      }}
      onBack={() => router.push("/learner/dashboard")}
    />
  );
}
