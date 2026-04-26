"use client";

import { useRouter } from "next/navigation";
import { Onboarding } from "../../components/eduboost/EntryScreens";
import { useLearner } from "../../context/LearnerContext";
import { createLearnerAPI } from "../../components/eduboost/api";

export default function OnboardingPage() {
  const router = useRouter();
  const { setLearner } = useLearner();

  return (
    <div className="app">
      <div className="flag-bar" />
      <Onboarding
        onComplete={async (data) => {
          try {
            await createLearnerAPI({
              grade: data.grade,
              home_language: data.language,
              avatar_id: data.avatar,
              learning_style: { visual: 0.6, auditory: 0.2, kinesthetic: 0.2 },
            });
          } catch (e) {
            console.error("Failed to create learner profile API call, proceeding with local context:", e);
          }
          setLearner({ ...data, xp: 0, streak: 1 });
          router.push("/learner/dashboard");
        }}
      />
    </div>
  );
}
