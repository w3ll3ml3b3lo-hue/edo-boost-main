"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { LearnerService } from "../lib/api/services";

const LearnerContext = createContext();

export function LearnerProvider({ children }) {
  const [learner, setLearner] = useState(null);
  const [masteryData, setMasteryData] = useState({});
  const [gamification, setGamification] = useState(null);
  const [badge, setBadge] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load learner from localStorage on initial mount
  useEffect(() => {
    const saved = localStorage.getItem("eb_active_learner");
    if (saved) {
      try {
        setLearner(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to parse saved learner", e);
      }
    }
    setLoading(false);
  }, []);

  // Save learner to localStorage whenever it changes
  useEffect(() => {
    if (learner) {
      localStorage.setItem("eb_active_learner", JSON.stringify(learner));
      refreshState();
    } else {
      localStorage.removeItem("eb_active_learner");
      setMasteryData({});
      setGamification(null);
    }
  }, [learner]);

  const refreshState = async () => {
    if (!learner?.learner_id) return;
    try {
      const [masteryRes, gamificationRes] = await Promise.all([
        LearnerService.getMastery(learner.learner_id),
        LearnerService.getGamificationProfile(learner.learner_id),
      ]);

      if (masteryRes && masteryRes.mastery) {
        const newMastery = {};
        masteryRes.mastery.forEach((m) => {
          newMastery[m.subject_code] = Math.round(m.mastery_score * 100);
        });
        setMasteryData(newMastery);
      }
      setGamification(gamificationRes);
    } catch (err) {
      console.error("Failed to refresh learner state:", err);
    }
  };

  return (
    <LearnerContext.Provider
      value={{
        learner,
        setLearner,
        masteryData,
        setMasteryData,
        gamification,
        setGamification,
        refreshState,
        badge,
        setBadge,
        loading,
      }}
    >
      {children}
    </LearnerContext.Provider>
  );
}

export function useLearner() {
  const context = useContext(LearnerContext);
  if (!context) {
    throw new Error("useLearner must be used within a LearnerProvider");
  }
  return context;
}
