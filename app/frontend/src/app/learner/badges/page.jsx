"use client";

import { useLearner } from "../../../../context/LearnerContext";
import { BadgesPanel } from "../../../../components/eduboost/FeaturePanels";

export default function BadgesPage() {
  const { learner } = useLearner();

  return <BadgesPanel learner={learner} />;
}
