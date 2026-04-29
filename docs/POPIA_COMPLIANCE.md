# POPIA Compliance Guide

**Protection of Personal Information Act (POPIA), No. 4 of 2013 — South Africa**

This document explains how EduBoost SA implements POPIA compliance, which controls and processes are in place, and what gaps remain. It is intended for developers, auditors, and legal reviewers.

---

## Overview

EduBoost SA processes personal information of children (defined as minors under 18 in terms of POPIA), which triggers heightened obligations under **Section 34 of POPIA** and the **Children's Act**. We treat every learner's data as subject to the most protective tier of POPIA requirements.

---

## Applicable POPIA Conditions

POPIA defines **8 Conditions for Lawful Processing** (Sections 8–25). Our implementation against each:

### Condition 1 — Accountability (Section 8)

**Requirement:** The responsible party must ensure compliance with POPIA.

**Implementation:**
- The project maintainer (NkgoloL) is the designated responsible party
- The `judiciary.py` layer is the code-level accountability mechanism — it is the single enforcement point for data processing rules
- Audit events in `fourth_estate.py` create the accountability record

**Status:** ✅ Architecture in place | ⚠️ Full end-to-end validation incomplete

---

### Condition 2 — Processing Limitation (Section 9–12)

**Requirement:** Processing must be lawful, adequate, relevant, and not excessive.

**Our legal basis:** Consent from the guardian (Section 11(1)(a)) — required before any learner data is created or processed.

**Implementation:**
- `POST /api/v1/consent` creates a timestamped consent record before any learner data is accepted
- The Judiciary checks consent status on every learner-data operation
- Consent version is stored — updates to our privacy policy may require re-consent

**Data collected per learner:**
- `display_name` — learner-chosen first name or nickname only (no surname)
- `grade` — numeric grade level
- `home_language` — from a controlled list
- `province` — from a controlled list
- Diagnostic responses (pseudonymous item IDs + correct/incorrect flag)
- XP and badge records (gamification)
- Lesson access records

**Data NOT collected:**
- Full legal name
- South African ID number
- School name or EMIS number
- Physical address
- Photo or biometric data
- Device identifiers

**Status:** ✅ Data minimisation designed | ⚠️ Audit of actual data collection completeness pending

---

### Condition 3 — Purpose Specification (Section 13–14)

**Requirement:** Processing must be for a specific, explicitly defined purpose communicated to the data subject.

**Our stated purpose:** To provide personalised, adaptive education content to the learner based on their assessed knowledge gaps.

**Implementation:**
- Purpose is declared in the consent form at `POST /api/v1/consent` (stored with `consent_version`)
- All data processing operations are tagged with purpose codes in the audit trail
- The Judiciary rejects any processing request that does not match a defined purpose

**Status:** ✅ Purpose defined | ⚠️ Purpose-code tagging not yet applied to all operations

---

### Condition 4 — Further Processing Limitation (Section 15)

**Requirement:** Further processing must be compatible with the original purpose.

**Implementation:**
- RLHF (Reinforcement Learning from Human Feedback) data uses **aggregated, de-identified** feedback only — never linked back to individual learner identities
- `FEATURE_RLHF_COLLECTION` flag disables this collection if required
- Lesson content logs stripped of learner identifiers before any model training pipeline

**Status:** ✅ Design compliant | ⚠️ Full pipeline audit pending

---

### Condition 5 — Information Quality (Section 16)

**Requirement:** Personal information must be complete, accurate, and not misleading.

**Implementation:**
- Learner grade is validated against a controlled range (Grade R = 0 through Grade 7 = 7)
- Province validated against official South African province list
- Home language validated against official SA language list

**Status:** ✅ Input validation in place

---

### Condition 6 — Openness (Section 17–18)

**Requirement:** Learners and guardians must be informed of processing activities.

**Implementation:**
- Privacy notice displayed before consent is collected
- `consent_version` field tracks which version of the privacy policy was accepted
- Guardians can request a copy of their learner's data via the Parent Portal

**Status:** ⚠️ Privacy notice content needs legal review | ⚠️ Data export (Subject Access Request) not yet implemented

---

### Condition 7 — Security Safeguards (Section 19–22)

**Requirement:** Appropriate technical and organisational measures must protect personal information.

**Technical measures in place:**

| Measure | Implementation |
|---------|---------------|
| Encryption in transit | HTTPS/TLS (production) |
| Encryption at rest | Fernet symmetric encryption via `cryptography` library |
| Authentication | JWT (HS256, 24hr expiry) |
| Authorisation | Role-based (learner / guardian / admin) via FastAPI dependencies |
| PII scrubbing | `bleach` and `phonenumbers` libraries |
| Pseudonymisation | Learner IDs are opaque random strings, not names or SA IDs |
| LLM firewall | All AI calls go through backend; raw learner data never reaches LLM provider |
| Audit trail | Redis stream (`eduboost:audit_stream`) — append-only |
| Rate limiting | `slowapi` on all endpoints |

**Breach notification (Section 22):**
- Security incidents must be reported to the **Information Regulator** and affected data subjects without unreasonable delay
- Refer to `SECURITY.md` for the vulnerability reporting process
- ⚠️ A formal breach response procedure does not yet exist — this is a gap

**Status:** ✅ Technical measures largely in place | ⚠️ Breach response procedure missing | ⚠️ Penetration test not yet performed

---

### Condition 8 — Data Subject Participation (Section 23–25)

**Requirement:** Data subjects (or their guardians) have the right to access, correct, and delete their information.

#### Right of Access (Section 23)

Guardians may request all data held about their learner.

**Current implementation:** Partial — Parent Portal exposes learner profile, XP, and study plans. Full data export endpoint not yet built.

**Gap:** A formal Subject Access Request (SAR) process with a 30-day response SLA is not yet implemented.

#### Right to Correction (Section 24(a))

Guardians may update learner profile information (display name, grade).

**Implementation:** `PUT /api/v1/learners/{learner_id}` ✅

#### Right to Deletion / Erasure (Section 24(b))

Guardians may request complete deletion of a learner's data.

**Implementation:**
```
DELETE /api/v1/learners/{learner_id}
```

This operation:
1. Soft-deletes the learner record in PostgreSQL
2. Queues a background Celery task to cascade-delete all related records (diagnostic sessions, lessons, study plans, XP events)
3. Purges Redis cache keys associated with the learner
4. Emits a `"learner_erased"` event to the Fourth Estate audit stream

**Gap:** ⚠️ End-to-end verification of cascade deletion across ALL data stores (Postgres, Redis, S3/R2 if used) is not yet complete. This is a known, tracked gap.

#### Right to Object (Section 11(3))

Guardians may object to processing for any purpose other than the core education purpose.

**Implementation:** Revoking consent via `DELETE /api/v1/consent/{consent_id}` suspends all further processing. ✅ Architecture correct. ⚠️ Not end-to-end tested.

---

## Special Provisions — Children's Data

Because EduBoost SA specifically processes data of learners under 18:

1. **Parental/Guardian consent is always required** — a learner cannot self-consent, regardless of age
2. **The consent form uses plain language** — legal jargon is avoided
3. **Data is not shared with any third party** for marketing or profiling purposes
4. **Minimum data** is collected — Section 34 requires particular care with children's data

---

## LLM Provider POPIA Considerations

### What data is sent to LLM providers

The following is sent to Groq, Anthropic, or HuggingFace when generating a lesson:

```json
{
  "grade": 4,
  "subject": "Mathematics",
  "topic": "Long division",
  "sa_context": "wildlife, ubuntu, rands",
  "learning_style": "visual"
}
```

**What is NOT sent:**
- Learner display name
- Learner pseudonymous ID
- Any diagnostic response history
- Guardian information

The Judiciary layer enforces this by stripping any learner-identifying fields before constructing the LLM prompt.

### Third-party provider agreements

- **Groq:** Subject to Groq's Terms of Service and privacy policy. No data retention claimed for API usage.
- **Anthropic:** Subject to Anthropic's Terms of Service. API data is not used for model training.
- **HuggingFace:** Used only as an offline fallback — no data is sent externally when in offline mode.

⚠️ **Gap:** Formal Data Processing Agreements (DPAs) with each LLM provider should be reviewed by a legal professional before go-live with real learners.

---

## Audit Trail

All sensitive operations emit structured events to the Fourth Estate Redis stream.

**Stream key:** `eduboost:audit_stream`  
**Max entries:** 100,000 (MAXLEN trimming)  
**Persistent mirror:** Critical events are written to the SQL `audit_log` table

### Audited event types

| Event | Trigger |
|-------|---------|
| `consent_granted` | Guardian submits consent |
| `consent_revoked` | Guardian revokes consent |
| `learner_created` | New learner profile created |
| `learner_erased` | Right-to-erasure request processed |
| `diagnostic_started` | IRT session begins |
| `diagnostic_completed` | IRT session ends with results |
| `lesson_generated` | LLM lesson created |
| `lesson_accessed` | Learner views a lesson |
| `parent_report_generated` | AI progress report created |
| `data_export_requested` | Subject Access Request received |
| `auth_login` | Successful authentication |
| `auth_failed` | Failed authentication attempt |
| `policy_violation` | Judiciary blocked a request |

---

## Known Compliance Gaps

The following are acknowledged gaps with planned remediation:

| Gap | Priority | Status |
|-----|----------|--------|
| Right-to-erasure not end-to-end verified across all stores | P0 | In progress |
| Consent audit trail incomplete for all operations | P0 | In progress |
| Breach response procedure not documented | P1 | Planned |
| Subject Access Request (SAR) export endpoint missing | P1 | Planned |
| Data Processing Agreements (DPAs) with LLM providers not reviewed | P1 | Planned |
| Privacy notice not reviewed by legal professional | P1 | Planned |
| Penetration test not performed | P1 | Planned |
| Purpose-code tagging incomplete in audit events | P2 | Planned |

---

## Compliance Checklist for New Features

Before shipping any feature that processes learner data, the developer must verify:

- [ ] Does this feature require a new consent basis? If yes, update consent form and version
- [ ] Is the data collected proportionate to the purpose?
- [ ] Does the data pass through the Judiciary layer?
- [ ] Is an audit event emitted for this operation?
- [ ] If this feature sends data to an external service, has the LLM firewall rule been updated?
- [ ] Is the data included in the right-to-erasure cascade?
- [ ] Is this documented in the Privacy Notice?

---

## Information Regulator Contact

South African Information Regulator:  
Website: [justice.gov.za/inforeg/](https://justice.gov.za/inforeg/)  
Email: inforeg@justice.gov.za  
Tel: +27 12 406 4818

---

_This document must be reviewed and updated with each significant change to data processing practices. Last reviewed: April 2026._
