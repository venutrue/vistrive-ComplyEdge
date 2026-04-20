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
## Current Status
This repository now includes an initial **FastAPI backend scaffold** with:
- API server bootstrapping
- Health endpoint
- Tenant onboarding stub endpoint
- PostgreSQL + Redis local runtime via Docker Compose

## Quick Start
1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
2. Start local stack:
   ```bash
   docker compose up --build
   ```
3. Open API docs:
   - Swagger UI: http://localhost:8000/docs
   - Health: http://localhost:8000/api/v1/health

## API Endpoints (initial)
- `GET /api/v1/health`
- `POST /api/v1/tenants`

Example tenant payload:
```json
{
  "legal_name": "Acme Manufacturing India Pvt Ltd",
  "primary_contact_email": "compliance@acme.example"
}
```

## Next Implementation Milestones
- Database models and migrations (tenant/legal entity/establishment)
- RBAC and auth (SSO + MFA hooks)
- Rule catalog ingestion and applicability engine
- Task/calendar orchestration and audit trail
