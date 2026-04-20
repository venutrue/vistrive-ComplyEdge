# ComplyEdge

ComplyEdge is a multi-tenant compliance SaaS platform for Indian labour code obligations.

## Current Backend Coverage
- Tenant, legal-entity, establishment hierarchy
- Roles/users (RBAC baseline)
- Regulations, rules, obligation templates
- Applicability-driven compliance task generation
- Filings/evidence APIs
- Notices and incidents APIs
- Notification queue/send/list APIs
- Inspection packet summary API
- Payroll validation API
- Dashboard summary API
- AI copilot (citations + mandatory human review signal)
- Auth login + MFA verify endpoints (baseline)
- Tenant isolation guardrails via `X-Tenant-ID` + bearer token validation for protected paths
- CORS middleware and token TTL configuration

## Quick Start
1. `cp .env.example .env`
2. `docker compose up --build`
3. Open `http://localhost:8000/docs`

## Tenant-Safe API Access Pattern
For protected APIs, include:
- `Authorization: Bearer <token>`
- `X-Tenant-ID: <tenant_id>`

Get a bootstrap token:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@acme.test", "tenant_id":"<tenant_id>"}'
```

## Run Tests
```bash
cd backend
python -m pytest -q
```

## Migration Artifact
- `backend/migrations/0001_initial_schema.sql` contains an explicit starter DDL script for controlled deployment environments.

## Notes
This branch resolves merge-sensitive files by consolidating tenant-guardrail + auth + dashboard + config updates into one coherent baseline.
