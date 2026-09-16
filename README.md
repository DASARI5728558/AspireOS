# AspireOS Capability & Knowledge Hub

Production-oriented full-stack reference implementation for trusted daily, weekly and monthly stakeholder updates, public learning-resource discovery, skill diagnostics, adaptive learning paths and measurable capability improvement.

## What is included

- Role-aware feeds and digest generation (learner, faculty, employer, institution, government, mentor and admin)
- Curated national/global institutional source registry with provenance, licence and canonical-link metadata
- RSS/Atom ingestion, deduplication, topic tagging and a human approval gate
- Skill catalogue, self/verified assessments, gap analysis, learning plans and evidence portfolios
- Notifications, bookmarks, feedback, recommendations, dashboards and audit events
- JWT authentication, RBAC, tenant isolation hooks, consent/preferences, rate limiting and safe URL validation
- English plus eight Indian-language locale scaffolds
- FastAPI, PostgreSQL, Redis, Celery/APScheduler-compatible jobs, React/TypeScript, Docker Compose
- OpenAPI docs, tests, seed data and architecture/operations documentation

## Quick start

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Open the web app at `http://localhost:5173` and API docs at `http://localhost:8000/docs`.
4. Seeded demo login: `learner@aspireos.example.com` / `ChangeMe123!` (change immediately outside local development).

Without Docker:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

## Responsible content model

AspireOS stores source metadata, abstracts, licensing status and canonical links. It does not copy full books/PDFs unless the licence and organisational policy explicitly permit it. Automated items enter `pending_review`; only approved content appears in stakeholder feeds. Source inclusion is not an endorsement.

## Repository map

- `backend/` API, models, services, ingestion and tests
- `frontend/` responsive stakeholder experience
- `infra/` source seed catalogue
- `docs/` architecture, API and operating controls
- `docker-compose.yml` local integrated runtime

## Production hardening checklist

Replace demo secrets; connect SSO/OIDC; run Alembic migrations; enable managed PostgreSQL/Redis; configure an email/push provider; put API behind TLS/WAF; configure malware scanning for uploads; enable backups, SIEM export and data-retention jobs; validate accessibility (WCAG 2.2 AA); and complete DPIA/security review before processing real learner data.
