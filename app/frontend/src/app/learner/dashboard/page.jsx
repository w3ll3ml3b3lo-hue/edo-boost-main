"use client";

import { useRouter } from "next/navigation";
import { useLearner } from "../../../../context/LearnerContext";
import { DashboardPanel } from "../../../../components/eduboost/FeaturePanels";

export default function DashboardPage() {
  const { learner, masteryData } = useLearner();
  const router = useRouter();

  return (
    <DashboardPanel
      learner={learner}
      masteryData={masteryData}
      onStartLesson={() => router.push("/learner/lesson")}
      onStartDiag={() => router.push("/learner/diagnostic")}
    />
  );
}
