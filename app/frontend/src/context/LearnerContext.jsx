"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

const LearnerContext = createContext();

export function LearnerProvider({ children }) {
  const [learner, setLearner] = useState(null);
  const [masteryData, setMasteryData] = useState({
    MATH: 38,
    ENG: 62,
    LIFE: 75,
    NS: 55,
    SS: 48,
  });
  const [badge, setBadge] = useState(null);

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
  }, []);

  // Save learner to localStorage whenever it changes
  useEffect(() => {
    if (learner) {
      localStorage.setItem("eb_active_learner", JSON.stringify(learner));
    } else {
      localStorage.removeItem("eb_active_learner");
    }
  }, [learner]);

  return (
    <LearnerContext.Provider
      value={{
        learner,
        setLearner,
        masteryData,
        setMasteryData,
        badge,
        setBadge,
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
