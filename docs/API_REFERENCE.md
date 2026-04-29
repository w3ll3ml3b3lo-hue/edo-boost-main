# API Reference

**EduBoost SA Backend API — v1**

Base URL: `http://localhost:8000/api/v1` (local dev)  
Interactive docs: `http://localhost:8000/docs` (Swagger UI)  
Alternative docs: `http://localhost:8000/redoc`

---

## Authentication

All endpoints (except `/auth/login` and `/health`) require a **Bearer JWT token**.

```http
Authorization: Bearer <token>
```

Tokens are issued at login and expire after **24 hours** (`JWT_EXPIRY_HOURS`). Signed with HS256 using `JWT_SECRET`.

### Token Claims

```json
{
  "sub": "learner_pseudoid or guardian_id",
  "role": "learner | guardian | admin",
  "exp": 1234567890
}
```

---

## Rate Limits

| Endpoint Group | Limit |
|----------------|-------|
| General API | 100 requests/minute |
| LLM-backed endpoints (`/lessons`, `/diagnostic`) | 20 requests/minute |

Rate limit headers are returned on every response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1234567890
```

On limit exceeded: `429 Too Many Requests`

---

## Error Format

All errors follow a consistent envelope:

```json
{
  "detail": "Human-readable error message",
  "code": "MACHINE_READABLE_CODE",
  "field": "optional_field_name"
}
```

Common HTTP status codes:

| Code | Meaning |
|------|---------|
| `400` | Invalid request body or parameters |
| `401` | Missing or invalid JWT |
| `403` | Valid JWT but insufficient permissions (also: Judiciary policy failure) |
| `404` | Resource not found |
| `422` | Pydantic validation error |
| `429` | Rate limit exceeded |
| `500` | Internal server error (check Sentry) |
| `503` | LLM provider unavailable, fallback exhausted |

---

## Endpoints

---

### Health

#### `GET /health`

No authentication required.

**Response `200`:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "db": "connected",
  "redis": "connected"
}
```

---

### Authentication — `/api/v1/auth`

#### `POST /api/v1/auth/login`

Authenticates a guardian or admin. Returns a JWT.

**Request body:**
```json
{
  "email": "guardian@example.com",
  "password": "SecurePassword123!"
}
```

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "role": "guardian"
}
```

**Error `401`:** Invalid credentials.

---

#### `POST /api/v1/auth/learner-login`

Authenticates a learner using a PIN and their pseudonymous learner ID. No email required — designed for Grade R–7 usability.

**Request body:**
```json
{
  "learner_id": "lrn_abc123",
  "pin": "4321"
}
```

**Response `200`:** Same structure as guardian login, role = `"learner"`.

---

### Learners — `/api/v1/learners`

#### `POST /api/v1/learners`

Creates a new learner profile. **Requires guardian JWT.**

Guardian must have an active POPIA consent record before a learner can be created.

**Request body:**
```json
{
  "display_name": "Sipho",
  "grade": 4,
  "home_language": "isiZulu",
  "province": "KwaZulu-Natal"
}
```

> Note: No surname, full name, or school name is stored. `display_name` is a learner-chosen first name or nickname only.

**Response `201`:**
```json
{
  "learner_id": "lrn_abc123",
  "display_name": "Sipho",
  "grade": 4,
  "xp": 0,
  "streak_days": 0,
  "badges": [],
  "created_at": "2025-04-01T10:00:00Z"
}
```

---

#### `GET /api/v1/learners/{learner_id}`

Retrieves a learner profile. **Requires JWT of owning guardian or the learner.**

**Response `200`:**
```json
{
  "learner_id": "lrn_abc123",
  "display_name": "Sipho",
  "grade": 4,
  "xp": 1200,
  "streak_days": 5,
  "badges": [
    { "badge_id": "first_lesson", "earned_at": "2025-04-01T11:00:00Z" }
  ],
  "current_study_plan_id": "sp_xyz789"
}
```

---

#### `DELETE /api/v1/learners/{learner_id}`

**Right-to-erasure (POPIA Section 24).** Deletes all learner data across all stores.

**Requires guardian JWT.** Emits a `"learner_erased"` audit event.

**Response `204`:** No content.

> ⚠️ This operation is **irreversible**. All diagnostic data, lesson history, XP, and study plans are permanently deleted.

---

### Consent — `/api/v1/consent`

#### `POST /api/v1/consent`

Guardian grants POPIA consent for a learner. **Required before any learner data operations.**

**Request body:**
```json
{
  "learner_id": "lrn_abc123",
  "consent_version": "1.0",
  "granted": true,
  "ip_address": "196.x.x.x"
}
```

**Response `201`:**
```json
{
  "consent_id": "con_456",
  "learner_id": "lrn_abc123",
  "granted": true,
  "granted_at": "2025-04-01T10:00:00Z",
  "version": "1.0"
}
```

---

#### `DELETE /api/v1/consent/{consent_id}`

Revokes consent. All further data processing for the learner is suspended.

**Response `204`:** No content. Audit event emitted.

---

### Diagnostic — `/api/v1/diagnostic`

#### `POST /api/v1/diagnostic/sessions`

Starts a new IRT adaptive diagnostic session for a learner.

**Request body:**
```json
{
  "learner_id": "lrn_abc123",
  "subject": "Mathematics",
  "grade_target": 4
}
```

**Response `201`:**
```json
{
  "session_id": "diag_789",
  "learner_id": "lrn_abc123",
  "subject": "Mathematics",
  "status": "in_progress",
  "theta_estimate": 0.0,
  "standard_error": 999.0,
  "items_administered": 0,
  "current_item": {
    "item_id": "math_004_022",
    "question": "If you have 3 bags with 7 marbles each, how many marbles do you have?",
    "options": ["18", "21", "24", "28"],
    "grade_level": 3,
    "topic": "Multiplication"
  }
}
```

---

#### `POST /api/v1/diagnostic/sessions/{session_id}/responses`

Submits a learner's response to the current item. Returns the next item or signals completion.

**Request body:**
```json
{
  "item_id": "math_004_022",
  "response": "21",
  "response_time_ms": 12400
}
```

**Response `200` — more items:**
```json
{
  "session_id": "diag_789",
  "theta_estimate": 0.35,
  "standard_error": 1.1,
  "items_administered": 1,
  "status": "in_progress",
  "next_item": { ... }
}
```

**Response `200` — diagnostic complete:**
```json
{
  "session_id": "diag_789",
  "status": "complete",
  "theta_estimate": -0.4,
  "standard_error": 0.32,
  "items_administered": 12,
  "grade_estimate": 3,
  "knowledge_gaps": [
    { "concept": "Long division", "severity": "high" },
    { "concept": "Fractions: equivalence", "severity": "medium" }
  ]
}
```

---

#### `GET /api/v1/diagnostic/sessions/{session_id}`

Retrieves session status and results. **Guardian and learner can both access.**

---

### Lessons — `/api/v1/lessons`

> **Rate limited to 20 req/min (LLM endpoint)**

#### `POST /api/v1/lessons`

Generates (or retrieves cached) a CAPS-aligned lesson with South African context.

**Request body:**
```json
{
  "learner_id": "lrn_abc123",
  "grade": 4,
  "subject": "Mathematics",
  "topic": "Multiplication",
  "knowledge_gap": "3-digit multiplication",
  "learning_style": "visual"
}
```

**Response `201` or `200` (cached):**
```json
{
  "lesson_id": "les_321",
  "grade": 4,
  "subject": "Mathematics",
  "topic": "Multiplication",
  "provider": "groq",
  "cached": false,
  "content": {
    "title": "Multiplication at the Waterhole 🦏",
    "introduction": "At a waterhole in the Kruger, you spot 4 groups of 7 zebras...",
    "explanation": "...",
    "worked_example": "...",
    "practice_problems": [
      {
        "question": "There are 6 rhinos with 4 oxpecker birds each. How many birds?",
        "answer": "24",
        "hint": "Think of 6 groups of 4"
      }
    ],
    "summary": "...",
    "xp_reward": 50
  },
  "created_at": "2025-04-01T10:05:00Z"
}
```

**Error `503`:** All LLM providers failed. Retry after a short delay.

---

#### `GET /api/v1/lessons/{lesson_id}`

Retrieves a previously generated lesson by ID.

---

#### `POST /api/v1/lessons/{lesson_id}/feedback`

Submits learner feedback for RLHF (Reinforcement Learning from Human Feedback) collection.

**Request body:**
```json
{
  "rating": 4,
  "was_helpful": true,
  "was_too_easy": false,
  "was_too_hard": false,
  "free_text": "I liked the rhino example!"
}
```

**Response `201`:**
```json
{ "feedback_id": "fb_111", "recorded": true }
```

---

### Study Plans — `/api/v1/study-plans`

#### `POST /api/v1/study-plans`

Generates a CAPS-aligned weekly study plan based on diagnostic results.

**Request body:**
```json
{
  "learner_id": "lrn_abc123",
  "diagnostic_session_id": "diag_789",
  "weeks": 4,
  "sessions_per_week": 5,
  "session_duration_minutes": 30
}
```

**Response `201`:**
```json
{
  "plan_id": "sp_xyz789",
  "learner_id": "lrn_abc123",
  "grade": 4,
  "start_date": "2025-04-07",
  "end_date": "2025-05-02",
  "weeks": [
    {
      "week": 1,
      "sessions": [
        {
          "day": "Monday",
          "subject": "Mathematics",
          "topic": "Long division — foundational",
          "type": "remediation",
          "duration_minutes": 30,
          "lesson_id": null
        },
        { ... }
      ]
    }
  ]
}
```

---

#### `GET /api/v1/study-plans/{plan_id}`

Retrieves a study plan.

---

#### `PUT /api/v1/study-plans/{plan_id}/sessions/{session_index}/complete`

Marks a study session as complete and awards XP.

**Response `200`:**
```json
{
  "xp_awarded": 50,
  "new_total_xp": 1250,
  "streak_days": 6,
  "badge_earned": null
}
```

---

### Parent Portal — `/api/v1/parent`

#### `GET /api/v1/parent/learners`

Returns all learners linked to the authenticated guardian.

**Response `200`:**
```json
{
  "learners": [
    {
      "learner_id": "lrn_abc123",
      "display_name": "Sipho",
      "grade": 4,
      "xp": 1250,
      "streak_days": 6,
      "last_active": "2025-04-01T15:30:00Z"
    }
  ]
}
```

---

#### `POST /api/v1/parent/reports`

Generates an AI-powered progress report for a learner.

> Processed as a background Celery task. Returns a task ID immediately.

**Request body:**
```json
{
  "learner_id": "lrn_abc123",
  "period_weeks": 4
}
```

**Response `202`:**
```json
{
  "task_id": "celery_task_abc",
  "status": "pending",
  "estimated_seconds": 30
}
```

---

#### `GET /api/v1/parent/reports/{task_id}`

Polls for report completion.

**Response `200` (complete):**
```json
{
  "task_id": "celery_task_abc",
  "status": "complete",
  "report": {
    "learner_display_name": "Sipho",
    "grade": 4,
    "period": "2025-03-01 to 2025-04-01",
    "summary": "Sipho has shown excellent progress in Mathematics...",
    "strengths": ["Multiplication", "Place value"],
    "growth_areas": ["Long division", "Word problems"],
    "study_consistency_percent": 80,
    "xp_earned_this_period": 1250,
    "recommendation": "Focus on division with remainders next week...",
    "generated_at": "2025-04-01T10:10:00Z"
  }
}
```

**Response `202`:** Still processing. Poll again.

---

## Webhook Events (Planned)

> Not yet implemented. Documented here for design alignment.

| Event | Trigger |
|-------|---------|
| `learner.diagnostic.completed` | Diagnostic session finished |
| `learner.lesson.completed` | Learner marks lesson done |
| `learner.badge.earned` | New badge awarded |
| `guardian.report.ready` | Weekly progress report generated |

---

## Pagination

List endpoints that return multiple items support cursor-based pagination:

```http
GET /api/v1/diagnostic/sessions?learner_id=lrn_abc123&limit=20&cursor=sess_xyz
```

**Response envelope:**
```json
{
  "data": [...],
  "next_cursor": "sess_abc",
  "has_more": true
}
```

---

## Versioning

The API is versioned via URL path prefix (`/api/v1/`). Breaking changes will result in a new `/api/v2/` prefix with a deprecation notice period of at least 90 days.
