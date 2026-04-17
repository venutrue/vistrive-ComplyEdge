# ComplyEdge

ComplyEdge is a multi-tenant compliance SaaS platform for Indian labour code obligations.

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
