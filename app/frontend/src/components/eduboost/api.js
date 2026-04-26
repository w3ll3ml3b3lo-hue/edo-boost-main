function uuidv4() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) return crypto.randomUUID();
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function getLearnerPseudonymId() {
  if (typeof window === "undefined") return uuidv4();
  let id = window.localStorage.getItem("eb_learner_pseudonym_id");
  if (!id) {
    id = uuidv4();
    window.localStorage.setItem("eb_learner_pseudonym_id", id);
  }
  return id;
}

export async function createLearnerAPI(payload) {
  const data = await callAPI("/learners/", payload);
  if (data && data.learner_id) {
    if (typeof window !== "undefined") {
      window.localStorage.setItem("eb_learner_pseudonym_id", data.learner_id);
    }
  }
  return data;
}

export async function getLearnerMasteryAPI() {
  const data = await callAPI(`/learners/${getLearnerPseudonymId()}/mastery`, null, "GET");
  return data;
}

async function callAPI(endpoint, body, method = "POST") {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body && method !== "GET") {
    options.body = JSON.stringify(body);
  }
  
  const res = await fetch(`${apiUrl}${endpoint}`, options);

  if (!res.ok) {
    let detail = `API error: ${res.status}`;
    try {
      const err = await res.json();
      detail = err.detail?.reason || err.detail?.error || err.detail || detail;
    } catch {
      // ignore JSON parsing errors
    }
    throw new Error(detail);
  }

  return res.json();
}

export async function generateLessonAPI({ grade, subjectCode, subjectLabel, topic, homeLanguage, masteryPrior }) {
  const data = await callAPI("/lessons/generate", {
    learner_id: getLearnerPseudonymId(),
    subject_code: subjectCode,
    subject_label: subjectLabel,
    topic,
    grade,
    home_language: homeLanguage || "English",
    learning_style_primary: "visual",
    mastery_prior: typeof masteryPrior === "number" ? masteryPrior : 0.5,
    has_gap: false,
  });
  return data.lesson;
}

export async function runDiagnosticAPI({ subjectCode, grade, maxQuestions = 10 }) {
  const data = await callAPI("/diagnostic/run", {
    learner_id: getLearnerPseudonymId(),
    subject_code: subjectCode,
    grade,
    max_questions: maxQuestions,
  });
  return data;
}

export async function generateStudyPlanAPI({ grade, knowledgeGaps = [], subjectsMastery = {} }) {
  const data = await callAPI("/study-plans/generate", {
    learner_id: getLearnerPseudonymId(),
    grade,
    knowledge_gaps: knowledgeGaps,
    subjects_mastery: subjectsMastery,
    gap_ratio: 0.4,
  });
  return data.plan;
}

export async function generateParentReportAPI() {
  // Use a dummy guardian ID until guardian login flow is fully attached
  const guardianId = "00000000-0000-4000-8000-000000000000";
  const data = await callAPI("/parent/report/generate", {
    learner_id: getLearnerPseudonymId(),
    guardian_id: guardianId,
  });
  return data.report;
}

// --------------------------------------------------------
// Auth & Identity APIs
// --------------------------------------------------------

export async function guardianLoginAPI({ email, learnerPseudonymId }) {
  const data = await callAPI("/auth/guardian/login", {
    email,
    learner_pseudonym_id: learnerPseudonymId,
  });
  return data;
}

export async function learnerSessionAPI() {
  const data = await callAPI("/auth/learner/session", {
    learner_id: getLearnerPseudonymId(),
  });
  return data;
}

// --------------------------------------------------------
// Gamification APIs
// --------------------------------------------------------

export async function getLearnerProfileAPI() {
  const data = await callAPI(`/gamification/${getLearnerPseudonymId()}/profile`, null, "GET");
  return data;
}

export async function awardXPAPI({ xpAmount, eventType, lessonId = null }) {
  const data = await callAPI("/gamification/award-xp", {
    learner_id: getLearnerPseudonymId(),
    xp_amount: xpAmount,
    event_type: eventType,
    lesson_id: lessonId,
  });
  return data;
}

// --------------------------------------------------------
// POPIA Privacy & Deletion APIs (Parent Portal)
// --------------------------------------------------------

export async function requestDeletionAPI({ guardianId, reason = "" }) {
  const data = await callAPI("/parent/deletion/request", {
    learner_id: getLearnerPseudonymId(),
    guardian_id: guardianId,
    reason,
  });
  return data;
}

export async function getDeletionStatusAPI({ guardianId }) {
  const data = await callAPI(`/parent/deletion/status/${getLearnerPseudonymId()}/${guardianId}`, null, "GET");
  return data;
}

export async function exportDataAPI({ guardianId }) {
  const data = await callAPI(`/parent/export/${getLearnerPseudonymId()}/${guardianId}`, null, "GET");
  return data;
}
