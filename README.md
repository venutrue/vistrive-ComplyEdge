# ComplyEdge

ComplyEdge is a multi-tenant compliance SaaS platform for Indian labour code obligations.

## Current Backend Coverage
- Tenant, legal-entity, establishment hierarchy
- Roles/users (RBAC baseline)
- Regulations, rules, obligation templates
- Applicability-driven compliance task generation
- Filings/evidence APIs
- Notices and incidents APIs
- Notification queue/send APIs
- Inspection packet summary API
- Payroll validation API
- Dashboard summary API
- AI copilot (citations + mandatory human review signal)
- Auth login + MFA verify endpoints (baseline)

## Quick Start
1. `cp .env.example .env`
2. `docker compose up --build`
3. Open `http://localhost:8000/docs`

## Run Tests
```bash
cd backend
python -m pytest -q
```

## Notes
This codebase is now significantly beyond scaffold and covers broad domain modules.
For production readiness, continue hardening with enterprise auth providers, migrations lifecycle, async worker orchestration, storage integrations, and frontend implementation.
