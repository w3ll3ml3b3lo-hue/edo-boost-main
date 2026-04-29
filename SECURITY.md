# Security Policy 🔒

EduBoost SA processes data belonging to children aged 5–13. We take security and privacy extremely seriously. This document covers our security policy, how to report vulnerabilities, and what data we protect.

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main` branch | ✅ Actively maintained |
| Any tagged release | ✅ Until superseded |
| Older branches | ❌ No security patches |

Always run the latest commit on `main` for security fixes.

---

## Reporting a Vulnerability

**Do not open a public GitHub Issue for security vulnerabilities.** Public disclosure of vulnerabilities affecting a children's education platform puts real learners at risk.

### How to report

1. **Email:** Send details to the project maintainer via the email listed on the [GitHub profile](https://github.com/NkgoloL).
2. **Subject line:** `[SECURITY] EduBoost SA — <brief description>`
3. **Include:**
   - Affected component (e.g., `app/api/routers/auth.py`, frontend consent page)
   - Steps to reproduce
   - Potential impact (data exposure, authentication bypass, POPIA violation, etc.)
   - Your suggested fix (optional but appreciated)
4. **Encrypt sensitive details** if possible using PGP (key available on request).

### What to expect

| Timeline | Action |
|----------|--------|
| Within 48 hours | Acknowledgement of your report |
| Within 7 days | Triage and severity assessment |
| Within 30 days | Fix or formal risk acceptance for low-severity issues |
| After fix | Credit in CHANGELOG (with your permission) |

We follow responsible disclosure: we ask that you give us 30 days before any public disclosure.

---

## Scope — What We Care About Most

Given that EduBoost SA handles **children's learning data**, we prioritise the following vulnerability classes:

### Critical (P0) — Fix within 24 hours
- Any authentication bypass
- Unauthenticated access to learner data
- SQL injection or mass data exposure
- JWT secret exposure or algorithm downgrade (HS256 → none)
- Leakage of learner data to LLM providers without pseudonymisation
- Parental consent enforcement bypass
- Plaintext storage of encryption keys or JWT secrets

### High (P1) — Fix within 7 days
- IDOR (Insecure Direct Object Reference) on learner or guardian records
- Missing HTTPS enforcement in production
- CSRF on state-changing endpoints
- Broken access control between learner / guardian / admin roles
- Audit log tampering or deletion
- Secrets in source code or container images
- Redis cache poisoning affecting learner responses

### Medium (P2) — Fix within 30 days
- Rate limiting bypass on LLM endpoints (financial impact)
- Missing input sanitisation (XSS in lesson content)
- Insecure CORS configuration
- Session fixation or inadequate token expiry

### Low (P3) — Track in backlog
- Informational disclosure (version headers, stack traces)
- Missing security headers (CSP, X-Frame-Options, etc.)
- Dependency vulnerabilities without known exploits

### Out of Scope
- Social engineering of maintainers
- Physical attacks
- DoS via resource exhaustion (report unless trivially exploitable)
- Bugs in third-party services (Groq, Anthropic, Supabase) — report directly to them

---

## Security Architecture

### Authentication

- JWT tokens signed with HS256 using a 64-character random secret (`JWT_SECRET`)
- Tokens expire after 24 hours (`JWT_EXPIRY_HOURS=24`)
- Refresh token flow: planned but not yet implemented
- Rate limiting on auth endpoints via `slowapi`

### Data Encryption

- Sensitive fields encrypted at rest using the `cryptography` library (Fernet)
- Encryption key (`ENCRYPTION_KEY`) must be exactly 32 characters
- Key derivation uses `ENCRYPTION_SALT`
- Keys are **never logged** and must be rotated if compromised

### Learner Data Pseudonymisation

- Learner identities are pseudonymised before being passed to any LLM provider
- The `judiciary.py` layer enforces this as a policy gate — PII cannot reach the LLM services without going through this layer
- Phone numbers and names are processed via `bleach` and `phonenumbers` for PII scrubbing

### Audit Trail

- The `fourth_estate.py` module writes all sensitive operations to a Redis stream (`eduboost:audit_stream`)
- Stream max length: 100,000 entries
- Audit records are immutable once written (append-only stream)
- Events include: login, consent grant/revocation, data access, erasure requests, LLM prompts

### LLM Security

- All lesson generation is **backend-mediated** — learners never call LLM APIs directly
- Groq is the primary provider (rate-limited to 20 req/min, 14,400/day)
- Anthropic Claude is the secondary/fallback provider
- HuggingFace Zephyr-7B is the offline fallback
- Provider API keys are environment-scoped and never exposed to frontend

### CORS

- Allowed origins are explicitly whitelisted (`ALLOWED_ORIGINS`)
- Default: `http://localhost:3000, https://eduboost.co.za`
- Wildcard origins (`*`) are never permitted

### Dependency Security

- Dependencies are pinned to exact versions in `requirements.txt`
- `pre-commit` hooks run before every commit
- **TODO:** Automated dependency vulnerability scanning (Dependabot or `pip-audit`) is not yet configured — this is a known gap

---

## POPIA (South African Privacy Law) Notes

EduBoost SA is designed for South African learners and is subject to the **Protection of Personal Information Act (POPIA), No. 4 of 2013**.

Key obligations relevant to security reporters:

- **Section 19** — responsible party must secure personal information
- **Section 22** — data breaches must be reported to the Information Regulator and affected data subjects
- Any vulnerability that could result in exposure of learner personal information is treated as a **potential POPIA breach** and escalated accordingly

If you discover a vulnerability that has already resulted in data exposure, please note this explicitly in your report. We are legally required to notify the Information Regulator within a reasonable time.

---

## Known Gaps (Honest Disclosure)

As of the current codebase state, the following security items are **incomplete** and are tracked for resolution:

| Gap | Status |
|-----|--------|
| Right-to-erasure (POPIA Section 24) not end-to-end verified | In progress |
| Consent audit trail incomplete across all workflows | In progress |
| No automated dependency vulnerability scanning | Planned |
| HTTPS not enforced in local dev stack | By design; enforced in production config |
| Refresh token rotation not implemented | Planned |
| CI/CD secrets scanning not configured | Planned |

We include this transparency so contributors can help address these gaps.

---

## Security Hall of Fame

We gratefully acknowledge researchers who responsibly disclose vulnerabilities. With your permission, your name will be listed here after the fix is released.

_(No entries yet — be the first!)_
