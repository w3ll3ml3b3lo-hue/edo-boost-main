"use client";

import React, { useEffect, useState } from "react";
import { useLearner } from "../../../context/LearnerContext";
import { LearnerService } from "../../../lib/api/services";
import { Card } from "../../../components/ui/Card";
import { LoadingSpinner } from "../../../components/ui/LoadingSpinner";
import { ErrorMessage } from "../../../components/ui/ErrorMessage";

export default function StudyPlanPage() {
  const { learner } = useLearner();
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!learner?.learner_id) return;

    const fetchPlan = async () => {
      setLoading(true);
      setError("");
      try {
        const res = await LearnerService.getStudyPlan(learner.learner_id);
        setPlan(res.plan || res);
      } catch (err) {
        console.error("Study plan fetch error:", err);
        setError("Failed to load your study plan. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchPlan();
  }, [learner?.learner_id]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <LoadingSpinner />
        <p className="mt-4 text-[var(--muted)] font-medium">Preparing your custom plan...</p>
      </div>
    );
  }

  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const schedule = plan?.days || plan?.schedule || {};
  const currentDay = new Intl.DateTimeFormat('en-US', { weekday: 'short' }).format(new Date());

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <header className="mb-12">
        <h1 className="text-4xl font-['Baloo_2'] font-bold text-[var(--text)] mb-2">
          📅 Your Study Plan
        </h1>
        <p className="text-[var(--muted)] font-medium">
          A personalized schedule built just for you based on your goals and progress.
        </p>
      </header>

      {error && <ErrorMessage message={error} className="mb-8" />}

      <Card className="p-8 border-none bg-gradient-to-br from-indigo-500 to-purple-600 text-white mb-12 shadow-xl">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div>
            <h2 className="text-2xl font-bold mb-2">Weekly Focus</h2>
            <p className="text-indigo-100 text-lg">
              {plan?.week_focus || "General Grade Review & Mastery Boost"}
            </p>
          </div>
          <div className="bg-white/20 backdrop-blur-md px-6 py-3 rounded-2xl border border-white/30 text-center">
            <div className="text-xs font-bold uppercase tracking-widest opacity-80 mb-1">Target Grade</div>
            <div className="text-2xl font-black">Grade {learner.grade}</div>
          </div>
        </div>
      </Card>

      <div className="space-y-6">
        {days.map((day) => {
          const items = schedule?.[day] || [];
          const isToday = day === currentDay;

          return (
            <div key={day} className={`flex flex-col md:flex-row gap-4 md:gap-8 ${isToday ? "relative" : ""}`}>
              <div className="md:w-32 flex flex-row md:flex-col items-center justify-center md:pt-4">
                <span className={`text-xl font-black uppercase tracking-tighter ${isToday ? "text-blue-600" : "text-gray-300"}`}>
                  {day}
                </span>
                {isToday && (
                  <span className="ml-2 md:ml-0 md:mt-1 bg-blue-100 text-blue-600 text-[10px] px-2 py-0.5 rounded-full font-bold">
                    TODAY
                  </span>
                )}
              </div>

              <div className="flex-1 space-y-4">
                {items.length === 0 ? (
                  <div className="p-6 rounded-2xl border-2 border-dashed border-gray-100 text-gray-400 italic text-sm">
                    Rest day! Take some time to play and recharge. 🌴
                  </div>
                ) : (
                  items.map((item, idx) => (
                    <Card 
                      key={idx} 
                      className={`p-6 border-none flex flex-col sm:flex-row items-center gap-6 transition-all shadow-md hover:shadow-lg ${
                        isToday ? "bg-white ring-2 ring-blue-500/20" : "bg-white/60"
                      }`}
                    >
                      <div className="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center text-3xl shadow-inner">
                        {item.emoji || "📚"}
                      </div>
                      <div className="flex-1 text-center sm:text-left">
                        <div className="flex flex-wrap justify-center sm:justify-start items-center gap-2 mb-1">
                          <h4 className="font-bold text-lg text-gray-800">{item.label}</h4>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-widest ${
                            item.type === "gap-fill" 
                              ? "bg-orange-100 text-orange-600" 
                              : item.type === "completed"
                              ? "bg-green-100 text-green-600"
                              : "bg-blue-100 text-blue-600"
                          }`}>
                            {item.type?.replace("-", " ") || "curriculum"}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500 font-medium">
                          {item.type === "gap-fill" 
                            ? "Focusing on a concept from a previous level." 
                            : "Standard curriculum goal for your grade."}
                        </p>
                      </div>
                      <button className={`px-6 py-2 rounded-xl font-bold transition-all ${
                        item.type === "completed"
                          ? "bg-green-50 text-green-600 cursor-default"
                          : "bg-gray-100 text-gray-600 hover:bg-blue-600 hover:text-white"
                      }`}>
                        {item.type === "completed" ? "✓ Done" : "Start →"}
                      </button>
                    </Card>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
