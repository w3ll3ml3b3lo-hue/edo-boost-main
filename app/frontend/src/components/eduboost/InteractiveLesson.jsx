"use client";

import React from "react";
import { Card } from "../ui/Card";
import { Button } from "../ui/Button";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { SUBJECTS } from "./constants";
import { useLearner } from "../../context/LearnerContext";

export default function InteractiveLesson({ lesson, subject, topic, onBack, onComplete, loading }) {
  const { learner } = useLearner();
  const subjectData = SUBJECTS.find(s => s.code === subject);

  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <Button variant="secondary" onClick={onBack} className="mb-6 hover:translate-x-[-4px] transition-transform">
        ← Choose Another Topic
      </Button>
      
      <Card className="p-8 md:p-12 border-none bg-white shadow-2xl overflow-hidden relative rounded-[32px]">
        {/* Decorative element */}
        <div 
          className="absolute top-0 right-0 p-8 opacity-10 text-9xl select-none"
          style={{ color: subjectData?.color }}
        >
          {subjectData?.icon || "📖"}
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-6">
            <span 
              className="px-4 py-1.5 rounded-full text-xs font-black text-white uppercase tracking-wider"
              style={{ backgroundColor: subjectData?.color }}
            >
              {subjectData?.label || subject}
            </span>
            <span className="text-[var(--muted)] text-sm font-bold bg-gray-50 px-3 py-1 rounded-lg">
              Grade {learner.grade} Adventure
            </span>
          </div>

          <h1 className="text-4xl md:text-5xl font-['Baloo_2'] font-extrabold text-gray-900 mb-8 leading-tight">
            {lesson.title}
          </h1>

          <div className="prose prose-xl prose-blue max-w-none mb-12">
            <div className="text-xl text-gray-600 leading-relaxed italic border-l-8 border-blue-500 pl-6 py-4 bg-blue-50/30 rounded-r-3xl mb-10">
              {lesson.summary || "Get ready to explore this exciting topic together! Let's dive in."}
            </div>
            
            <div className="mt-8 space-y-8 text-gray-800 text-lg md:text-xl leading-relaxed font-medium">
              {/* If content is an array of sections, render them, otherwise render as text */}
              {Array.isArray(lesson.content) ? (
                lesson.content.map((section, idx) => (
                  <div key={idx} className="space-y-4">
                    {section.heading && <h3 className="text-2xl font-bold text-gray-900">{section.heading}</h3>}
                    <p>{section.body || section}</p>
                  </div>
                ))
              ) : (
                <div className="whitespace-pre-wrap">{lesson.content}</div>
              )}

              {/* Real-world context footer */}
              <div className="bg-green-50/50 p-6 rounded-2xl border-2 border-green-100/50 mt-12">
                <h4 className="text-green-800 font-bold mb-2 flex items-center gap-2">
                  <span>🇿🇦</span> Why this matters in South Africa:
                </h4>
                <p className="text-green-700 text-base italic">
                  Learning about {topic} helps you understand the world around you, from the Kruger Park to the busy streets of Joburg!
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-orange-50 to-yellow-50 border-2 border-orange-100 p-10 rounded-[32px] text-center shadow-xl shadow-orange-500/5 relative overflow-hidden group">
            <div className="absolute -top-4 -right-4 text-6xl opacity-10 group-hover:scale-110 transition-transform">🌟</div>
            <h3 className="text-3xl font-black text-orange-700 mb-4 font-['Baloo_2']">Mission Accomplished?</h3>
            <p className="text-orange-600 mb-10 font-bold text-lg">Finish this lesson to claim your <span className="text-orange-800">35 XP</span> and level up!</p>
            
            <Button 
              onClick={onComplete} 
              disabled={loading} 
              className="px-16 py-5 text-2xl font-black shadow-2xl shadow-orange-500/40 hover:scale-105 active:scale-95 transition-all rounded-2xl bg-gradient-to-r from-orange-500 to-yellow-500 border-none"
            >
              {loading ? <LoadingSpinner size="sm" /> : "Claim My Stars! ✨"}
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
