"use client";

import { useRouter } from "next/navigation";
import { useLearner } from "../../../../context/LearnerContext";
import { LessonPanel } from "../../../../components/eduboost/FeaturePanels";

export default function LessonPage() {
  const { learner, setLearner, setBadge } = useLearner();
  const router = useRouter();

  return (
    <LessonPanel
      learner={learner}
      onComplete={(xp) => {
        setLearner((prev) => ({ ...prev, xp: (prev.xp || 0) + xp }));
        setBadge("Lesson Complete! 🌟");
        router.push("/learner/dashboard");
      }}
      onBack={() => router.push("/learner/dashboard")}
    />
  );
}
