"use client";

import { useLearner } from "../../../../context/LearnerContext";
import { ParentPortalPanel } from "../../../../components/eduboost/FeaturePanels";

export default function ParentPortalPage() {
  const { learner } = useLearner();

  return <ParentPortalPanel learner={learner} />;
}
