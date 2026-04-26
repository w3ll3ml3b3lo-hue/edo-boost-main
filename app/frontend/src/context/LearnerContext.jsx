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

  // Optional: Add local storage persistence here later

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
