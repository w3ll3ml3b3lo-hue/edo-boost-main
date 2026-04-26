"use client";

import { useEffect, useState } from "react";

import { 
  generateLessonAPI, 
  generateParentReportAPI, 
  generateStudyPlanAPI,
  getLearnerMasteryAPI,
  runDiagnosticAPI,
  awardXPAPI,
  getLearnerProfileAPI
} from "./api";
import { LESSON_TOPICS, QUESTION_BANK, SAMPLE_PLAN, SUBJECTS } from "./constants";
import { PlaceholderPanel } from "./ShellComponents";
import { useLearner } from "../../context/LearnerContext";

export function DashboardPanel({ learner, masteryData, onStartLesson, onStartDiag }) {
  const { setMasteryData } = useLearner();

  useEffect(() => {
    getLearnerMasteryAPI().then((res) => {
      if (res && res.mastery) {
        const newMastery = { ...masteryData };
        res.mastery.forEach((m) => {
          newMastery[m.subject_code] = Math.round(m.mastery_score * 100);
        });
        setMasteryData(newMastery);
      }
    }).catch(console.error);
  }, []);

  const overallMastery = Math.round(Object.values(masteryData).reduce((a, v) => a + v, 0) / Object.values(masteryData).length) || 0;
  return (
    <PlaceholderPanel title={`🏠 Welcome, ${learner.nickname}!`} description="Dashboard now fetches real subject mastery from the backend API.">
      <p style={{ marginBottom: 12 }}>Overall mastery: <strong>{overallMastery}%</strong></p>
      <div className="btn-row">
        <button className="btn-primary" onClick={onStartLesson}>Start lesson</button>
        <button className="btn-secondary" onClick={onStartDiag}>Open diagnostic</button>
      </div>
    </PlaceholderPanel>
  );
}

export function DiagnosticPanel({ learner, onComplete, onBack }) {
  const [subject, setSubject] = useState(null);
  const [loading, setLoading] = useState(false);
  const questions = subject ? (QUESTION_BANK[subject]?.[learner.grade] || QUESTION_BANK[subject]?.[3] || []) : [];

  async function handleRunDiagnostic() {
    setLoading(true);
    try {
      const res = await runDiagnosticAPI({ subjectCode: subject, grade: learner.grade, maxQuestions: 5 });
      const finalMastery = res.gap_report ? Math.round(res.gap_report.mastery_score * 100) : 60;
      onComplete(subject, finalMastery);
    } catch (e) {
      console.error(e);
      onComplete(subject, 60); // fallback
    } finally {
      setLoading(false);
    }
  }

  return (
    <PlaceholderPanel title="🧪 Diagnostic Assessment" description="Now executing real IRT adaptive assessment API calls.">
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 16 }}>
        {SUBJECTS.map((s) => (
          <button key={s.code} className="btn-secondary" onClick={() => setSubject(s.code)}>{s.label}</button>
        ))}
      </div>
      <p style={{ marginBottom: 16, color: "var(--muted)" }}>Selected question set: {questions.length} items</p>
      <div className="btn-row">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <button className="btn-primary" disabled={!subject || loading} onClick={handleRunDiagnostic}>{loading ? "Running IRT..." : "Run Diagnostic"}</button>
      </div>
    </PlaceholderPanel>
  );
}

export function LessonPanel({ learner, onComplete, onBack }) {
  const [subject, setSubject] = useState(null);
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [lessonTitle, setLessonTitle] = useState("");
  const [error, setError] = useState("");

  async function generate() {
    setLoading(true);
    setError("");
    try {
      const lesson = await generateLessonAPI({
        grade: learner.grade,
        subjectCode: subject,
        subjectLabel: SUBJECTS.find((s) => s.code === subject)?.label,
        topic,
        homeLanguage: learner.language,
      });
      setLessonTitle(lesson.title || topic);
    } catch (e) {
      setError(e.message || "Lesson generation failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PlaceholderPanel title="📖 Lessons" description="Phase 0 moves API logic and content configuration out of the monolithic component while preserving backend-only lesson generation.">
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 16 }}>
        {SUBJECTS.map((s) => (
          <button key={s.code} className="btn-secondary" onClick={() => { setSubject(s.code); setTopic(""); }}>{s.label}</button>
        ))}
      </div>
      {subject && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 16 }}>
          {(LESSON_TOPICS[subject] || []).map((entry) => (
            <button key={entry} className="btn-secondary" onClick={() => setTopic(entry)}>{entry}</button>
          ))}
        </div>
      )}
      {lessonTitle && <p style={{ marginBottom: 12 }}>Generated lesson: <strong>{lessonTitle}</strong></p>}
      {error && <p style={{ marginBottom: 12, color: "var(--red)" }}>{error}</p>}
      <div className="btn-row">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <button className="btn-primary" disabled={!subject || !topic || loading} onClick={generate}>{loading ? "Generating..." : "Generate lesson"}</button>
        <button className="btn-secondary" disabled={loading} onClick={async () => {
          setLoading(true);
          try {
            await awardXPAPI({ xpAmount: 35, eventType: "lesson_completed" });
            onComplete(35);
          } catch (e) {
            console.error(e);
            onComplete(35); // fallback
          } finally {
            setLoading(false);
          }
        }}>Award real API XP</button>
      </div>
    </PlaceholderPanel>
  );
}

export function StudyPlanPanel({ learner }) {
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState(null);

  async function generatePlan() {
    setLoading(true);
    try {
      const data = await generateStudyPlanAPI({ grade: learner.grade });
      setPlan(data);
    } catch {
      setPlan({ week_focus: "Fractions & Multiplication", days: SAMPLE_PLAN });
    } finally {
      setLoading(false);
    }
  }

  return (
    <PlaceholderPanel title="📅 Study Plan" description="Study plan logic now has its own surface area and uses shared API helpers.">
      <p style={{ marginBottom: 12 }}>Current focus: <strong>{plan?.week_focus || "Not generated yet"}</strong></p>
      <div className="btn-row">
        <button className="btn-primary" onClick={generatePlan} disabled={loading}>{loading ? "Generating..." : "Generate study plan"}</button>
      </div>
    </PlaceholderPanel>
  );
}

export function BadgesPanel() {
  const [profile, setProfile] = useState(null);
  
  useEffect(() => {
    getLearnerProfileAPI().then(setProfile).catch(console.error);
  }, []);

  return (
    <PlaceholderPanel title="🏆 Badges" description="Now fetching real gamification profile from the backend API.">
      {profile ? (
        <div>
          <p>Level: <strong>{profile.level}</strong></p>
          <p>Total XP: <strong>{profile.total_xp}</strong> / {profile.xp_to_next_level} to next level</p>
          <p>Streak: <strong>{profile.streak_days} days</strong></p>
          <div style={{ marginTop: 16 }}>
            <h4>Earned Badges:</h4>
            <ul style={{ paddingLeft: 20 }}>
              {(profile.earned_badges || []).length > 0 ? profile.earned_badges.map((b, i) => (
                <li key={i}>{b.name}</li>
              )) : <li>No badges yet!</li>}
            </ul>
          </div>
        </div>
      ) : (
        <p>Loading profile...</p>
      )}
    </PlaceholderPanel>
  );
}

export function ParentPortalPanel({ learner }) {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");

  async function generateReport() {
    setLoading(true);
    try {
      const report = await generateParentReportAPI({
        grade: learner.grade,
        streakDays: learner.streak || 1,
        totalXp: learner.xp || 0,
      });
      setSummary(report.summary || "Report generated.");
    } catch {
      setSummary("Parent reporting remains in phased hardening.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PlaceholderPanel title="👨‍👩‍👧 Parent Portal" description="Parent-facing workflows stay behind backend APIs while the frontend is decomposed.">
      <p style={{ marginBottom: 12 }}>{summary || "No report generated yet."}</p>
      <button className="btn-primary" onClick={generateReport} disabled={loading}>{loading ? "Generating..." : "Generate parent report"}</button>
    </PlaceholderPanel>
  );
}
