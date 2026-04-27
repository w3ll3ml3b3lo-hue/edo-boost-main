"use client";

import { useRouter } from "next/navigation";
import { useLearner } from "../../../context/LearnerContext";
import { InteractiveDiagnostic } from "../../../components/eduboost/InteractiveDiagnostic";

export default function DiagnosticPage() {
  const { learner, setMasteryData } = useLearner();
  const router = useRouter();

  return (
    <InteractiveDiagnostic
      learner={learner}
      onComplete={(subject, mastery) => {
        setMasteryData((prev) => ({ ...prev, [subject]: mastery }));
        router.push("/plan");
      }}
      onBack={() => router.push("/dashboard")}
    />
  );
}
