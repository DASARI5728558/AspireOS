# API and operations guide

Interactive documentation is exposed at `/docs`; the OpenAPI document is `/openapi.json`.

## Main endpoints

| Method and path | Purpose | Access |
|---|---|---|
| `POST /api/v1/auth/login` | Issue access token | Public |
| `GET /api/v1/me` | Current identity and role | Authenticated |
| `GET /api/v1/feed` | Ranked, approved stakeholder feed | Authenticated |
| `GET /api/v1/skills` | Capability taxonomy | Authenticated |
| `PUT /api/v1/assessments` | Create/update a skill assessment | Authenticated |
| `GET /api/v1/skill-gaps` | Explainable gap result | Authenticated |
| `GET /api/v1/learning-plans` | Adaptive pathway state | Authenticated |
| `GET /api/v1/digests/{daily\|weekly\|monthly}` | On-demand stakeholder digest | Authenticated |
| `POST /api/v1/feedback` | Relevance/outcome feedback | Authenticated |
| `POST /api/v1/admin/sources/{id}/ingest` | Controlled source ingestion | Admin |
| `PATCH /api/v1/admin/content/{id}/approve` | Human publication gate | Admin |

## Scheduled jobs

Deploy scheduler/worker processes separately in production. Recommended cadence in `Asia/Kolkata`: source health every 30 minutes, approved-feed refresh hourly, daily digest at 06:30, weekly digest Monday 07:00, monthly impact report on day 1 at 08:00. Use per-user timezone and quiet hours for notifications.

## Quality gates

- Source is official/authoritative, reachable and policy-approved.
- Canonical URL is unique; title/date/issuer are present.
- Licence is recorded; link-only is the safe default.
- Summary faithfully distinguishes source facts from AspireOS synthesis.
- Stakeholder and skill mappings have reviewer confidence.
- Accessibility and translation checks pass before publication.
- Corrections propagate to digests and cached views.

## KPIs

Track freshness SLA, source success rate, review turnaround, duplicate rate, feed relevance feedback, weekly active stakeholders, action conversion, learning completion, verified proficiency gain, time-to-proficiency, coverage by region/language, accessibility failures, correction rate and privacy/security incidents. Avoid vanity metrics and do not equate engagement with competence.
