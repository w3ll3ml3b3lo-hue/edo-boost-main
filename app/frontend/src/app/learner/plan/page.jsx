"use client";

import { useLearner } from "../../../../context/LearnerContext";
import { StudyPlanPanel } from "../../../../components/eduboost/FeaturePanels";

export default function StudyPlanPage() {
  const { learner } = useLearner();

  return <StudyPlanPanel learner={learner} />;
}
