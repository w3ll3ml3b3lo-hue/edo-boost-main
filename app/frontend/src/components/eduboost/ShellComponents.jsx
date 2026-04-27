"use client";

import { useLearner } from "../../context/LearnerContext";
import { AVATARS, GRADES } from "./constants";

export function Sidebar({ learner, activeTab, onTab, onLogout }) {
  const { gamification } = useLearner();
  const nav = [
    { id: "dashboard", icon: "🏠", label: "Home" },
    { id: "diagnostic", icon: "🧪", label: "Assessment" },
    { id: "lesson", icon: "📖", label: "Learn" },
    { id: "plan", icon: "📅", label: "Study Plan" },
    { id: "badges", icon: "🏆", label: "Badges" },
    { id: "parent", icon: "👨‍👩‍👧", label: "Parent Portal" },
  ];

  const level = gamification?.level || 1;
  const xp = gamification?.total_xp || 0;
  const xpProgress = (xp % 100);

  return (
    <div className="sidebar">
      <div style={{ padding: "0 20px 24px", borderBottom: "1px solid var(--border)", marginBottom: 8 }}>
        <strong>EduBoost SA</strong>
      </div>
      <div style={{ margin: "8px 12px 16px", background: "var(--surface2)", borderRadius: "var(--radius)", padding: 14 }}>
        <div style={{ fontSize: "2rem", textAlign: "center", marginBottom: 6 }}>{AVATARS[learner.avatar] || "🦁"}</div>
        <div style={{ fontWeight: 800, textAlign: "center" }}>{learner.nickname}</div>
        <div style={{ fontSize: "0.75rem", color: "var(--muted)", textAlign: "center", marginBottom: 12 }}>{GRADES[learner.grade]?.label}</div>
        
        {/* Gamification Bar */}
        <div style={{ background: "rgba(0,0,0,0.2)", height: 6, borderRadius: 3, overflow: "hidden", marginBottom: 4 }}>
          <div style={{ background: "var(--gold)", height: "100%", width: `${xpProgress}%`, transition: "width 0.5s ease-out" }} />
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: "10px", fontWeight: "bold" }}>
          <span style={{ color: "var(--gold)" }}>LVL {level}</span>
          <span style={{ color: "var(--muted)" }}>{xp} XP</span>
        </div>
      </div>
      {nav.map((item) => (
        <div
          key={item.id}
          onClick={() => onTab(item.id)}
          style={{
            padding: "12px 20px",
            cursor: "pointer",
            color: activeTab === item.id ? "var(--gold)" : "var(--muted)",
            borderLeft: activeTab === item.id ? "3px solid var(--gold)" : "3px solid transparent",
          }}
        >
          {item.icon} {item.label}
        </div>
      ))}
      <div style={{ marginTop: "auto", padding: 16 }}>
        <button className="btn-secondary" onClick={onLogout} style={{ width: "100%" }}>Logout</button>
      </div>
    </div>
  );
}

export function BadgePopup({ badge, onDismiss }) {
  return (
    <div className="badge-popup" onClick={onDismiss}>
      <span style={{ fontSize: "2rem" }}>🏅</span>
      <div>
        <div style={{ fontSize: "0.75rem", opacity: 0.8 }}>Badge Earned!</div>
        <div>{badge}</div>
      </div>
    </div>
  );
}

export function PlaceholderPanel({ title, description, children }) {
  return (
    <div style={{ maxWidth: 860, margin: "0 auto" }}>
      <h2 style={{ fontFamily: "'Baloo 2',cursive", fontSize: "1.6rem", marginBottom: 8 }}>{title}</h2>
      <p style={{ color: "var(--muted)", marginBottom: 24 }}>{description}</p>
      <div className="consent-form">{children}</div>
    </div>
  );
}
