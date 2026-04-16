# ComplyEdge Discovery for Indian Labour Code SaaS (Multi-tenant)

## 1) Repository Review Summary

Current repository status:
- Minimal codebase (no application source code yet).
- `README.md` is a placeholder.
- Repository mainly contains policy/legal reference PDFs related to India’s labour law reforms under the four labour codes.

This means the current task is primarily **product discovery + architecture definition + build prompt design** rather than code refactoring.

---

## 2) Document Set Reviewed (by file inventory)

The repository includes the following documents:

### Primary Code / Rule references
1. `Code on Wages 2019.pdf`
2. `Code On Wages.pdf`
3. `Rules_Draft Code on Wages.pdf`
4. `Code on Social Security 2020.pdf`
5. `Rules_Social Security Code.pdf`
6. `Industrial Relations Code.pdf`
7. `Rules_Draft Industrial Relations Code.pdf`
8. `Occupational Safety Health and Working Conditions Code 2020.pdf`
9. `Rules_Draft Occupational Safety Health and Working Conditions Code 2020.pdf`

### Secondary explainers / practitioner references
10. `Key Provisions under Social Security.pdf`
11. `Booklet New Labour Code India.pdf`
12. `Compliance Handbook for Employers.pdf`

## 3) Product Vision (Problem and Opportunity)

### Problem
Indian companies face fragmented labour compliance requirements across:
- Central and state notifications.
- Multiple periodic returns/registers.
- Varying thresholds by headcount, wages, sector, establishment type.
- Different obligations for contractors, gig/platform workers, inter-state migrant workers, women night shifts, standing orders, retrenchment, PF/ESI/social security, and welfare provisions.

### Opportunity
Create a **multi-tenant compliance operating system** for India-based employers that:
- Continuously tracks obligations under all 4 labour codes.
- Converts legal text into actionable tasks/checklists.
- Provides auditable evidence trails.
- Supports role-based operations across corporate HQ + plants + branches + contractors.

---

## 4) Target Users and Jobs-to-be-Done

### Tenant types
- SME employers (single state)
- Mid-market multi-state employers
- Large enterprises with factory + offices + contractors
- Compliance consultants/law firms managing multiple client tenants

### User personas
- Compliance Head / CHRO
- Plant HR Manager
- Payroll Lead
- Legal Counsel
- EHS/Safety Officer
- Contractor Compliance Coordinator
- Auditor / Inspector-response team
- Consultant Admin (cross-tenant)

### Core jobs
- Know what applies to my establishment(s) now.
- Get a calendar of filing/renewal/notice obligations.
- Ensure labour records/registers are complete.
- Track non-compliance risk and remediation.
- Respond quickly to inspections/notices with evidence.
- Produce leadership dashboards and audit packs.

---

## 5) Functional Scope for a Contemporary SaaS Portal

## A) Multi-tenant Foundation
- Tenant onboarding wizard (legal entity, CIN/PAN/GST, states, sectors, establishment types, employee counts, contractor footprint).
- Workspace hierarchy: Tenant -> Legal Entity -> Establishment -> Department/Cost Center.
- Data partitioning by tenant with strict isolation.
- Optional consultant “agency mode” to manage multiple tenants.

## B) Regulatory Applicability Engine
- Rule matrix engine to determine applicability by:
  - State/UT
  - Employee thresholds
  - Wage bands
  - Industry type/factory status
  - Gender/shift patterns
  - Contractor presence
  - Gig/platform worker categories
- Effective-dated logic (support amendments and upcoming effective dates).
- “Why this applies” explanation layer for trust and audit.

## C) Compliance Task & Calendar Engine
- Auto-generated obligations from applicability engine.
- Configurable recurrence: monthly/quarterly/annual/event-based.
- SLA tracking and escalation matrix.
- Submission workflow with maker-checker-approver.
- Evidence attachment + immutable activity logs.

## D) Registers, Returns, and Notice Management
- Smart templates for statutory registers/forms.
- API/import from HRMS/payroll to prefill data.
- Validation rules before submission.
- Version history and regenerated filings on corrections.

## E) Payroll & Social Security Controls
- Wage component mapping to legal definitions.
- Min wage/floor wage checks by location/category.
- Overtime/rest-day logic checks.
- PF/ESI/social security eligibility and deduction checks.
- Exception reports for underpayment/computation anomalies.

## F) Industrial Relations Workflow
- Standing order applicability and policy governance.
- Grievance workflow and disciplinary lifecycle tracking.
- Event workflows: closure/layoff/retrenchment/strike-related compliance logs.
- Notice tracker with statutory timelines.

## G) OSHWC / EHS Compliance Layer
- Safety committee requirements and membership tracker.
- Working conditions checklist by establishment type.
- Health/safety records + incident reporting.
- Contractor welfare and facility obligations.

## H) Inspection & Litigation Readiness
- One-click “inspection room” packet:
  - Applicable law map
  - Registers
  - Returns filed status
  - Licenses/renewals
  - Past notices and closure actions
- Notice-response workflow with legal owner assignment.

## I) Reporting, Risk, and Executive Dashboards
- Compliance health score by entity/state/code.
- Critical overdue obligations.
- Penalty exposure estimator (configurable assumptions).
- Trend analytics (open issues, repeat violations, closure cycle time).

## J) AI Co-pilot (with guardrails)
- Ask: “What applies to Bangalore office with 78 employees?”
- Ask: “What changed this month for Karnataka?”
- Draft response suggestions for notices.
- Natural language explanation of obligations with citations to source documents.
- Hallucination controls: always cite source + confidence + human review required.

---

## 6) Data Model (High-level)

Core entities:
- Tenant
- User, Role, Permission
- LegalEntity
- Establishment
- WorkforceSnapshot (effective dated)
- Contractor, ContractWorkforceSnapshot
- Regulation, Rule, ApplicabilityCondition
- ObligationTemplate
- ComplianceTask
- Filing/Return
- RegisterRecord
- EvidenceDocument
- Notice/Inspection
- Incident (OSHWC)
- AuditLog

Design principles:
- Effective-dated records everywhere.
- Immutable audit events.
- State-specific overlays on central rule objects.
- Explainable rule evaluation trace.

---

## 7) Architecture Recommendation (Modern SaaS)

- Frontend: Next.js + TypeScript + component design system.
- Backend: Modular monolith (initially) with domain modules:
  - Identity & RBAC
  - Tenant & Org hierarchy
  - Rule engine
  - Task engine
  - Documents & evidence
  - Notification service
- Database: PostgreSQL (tenant-aware schema strategy).
- Search: OpenSearch/Elastic for document and notice retrieval.
- Queue: Redis + worker (for reminders, async ingestion).
- Storage: S3-compatible object storage for evidence.
- Auth: SSO (SAML/OIDC) + MFA.
- Observability: OpenTelemetry + audit event pipeline.

Multi-tenant strategy:
- Start with shared DB + tenant_id row-level isolation + strong policies.
- Add enterprise option for isolated DB deployment.

---

## 8) Security, Compliance, and Governance Requirements

- Encryption at rest and in transit.
- Fine-grained RBAC + scoped data access.
- Immutable audit log and legal hold for documents.
- Configurable retention policies.
- India data residency deployment option.
- DLP controls for sensitive workforce data.

---

## 9) MVP vs Phase 2

### MVP (90-120 days)
- Tenant onboarding and org hierarchy.
- Applicability engine for top-priority obligations.
- Compliance calendar + task workflow.
- Basic returns/register templates.
- Evidence management + audit log.
- Executive dashboard and alerts.

### Phase 2
- Deep payroll validations.
- Advanced IR/OSH workflows.
- AI copilot with grounded retrieval.
- Consultant multi-client cockpit.
- API marketplace integrations.

---

## 10) Detailed Prompt for LLM (Use as Master Build Prompt)

Copy the following into your coding LLM:

---

You are a principal product architect + staff engineer. Design and implement a production-oriented **multi-tenant SaaS web portal** called **ComplyEdge** for Indian labour law compliance under the four labour codes:
1) Code on Wages
2) Code on Social Security
3) Industrial Relations Code
4) Occupational Safety, Health and Working Conditions Code

## Objective
Build a contemporary, enterprise-grade compliance platform for Indian companies with role-based workflows, applicability intelligence, evidence-backed compliance tasks, and executive dashboards.

## Required output format
Provide output in this sequence:
1. Product requirements document (PRD)
2. Domain model and database schema (ERD + SQL)
3. Service architecture and module boundaries
4. API contract (OpenAPI-style)
5. UI information architecture and key screens
6. Implementation plan in milestones (MVP -> Phase 2)
7. Starter code scaffolding (frontend + backend)
8. Seed data examples
9. Test strategy (unit, integration, E2E)
10. Security and audit controls checklist

## Non-negotiable product requirements
- Multi-tenant isolation with strict data segregation.
- Hierarchy: Tenant -> Legal Entity -> Establishment.
- Effective-dated applicability engine based on state, thresholds, establishment type, and workforce facts.
- Auto-generated obligations calendar and compliance task workflows (maker-checker-approver).
- Evidence attachment and immutable audit trail for each compliance action.
- Role-based access control (Super Admin, Compliance Admin, HR Manager, Payroll Manager, Legal Reviewer, Auditor, Read-only).
- Dashboard with compliance score, overdue items, risk hotspots by state/entity/code.
- Notification engine for due dates, escalations, and unresolved violations.
- Document management for filings, registers, notices, licenses.
- API/import adapters for HRMS and payroll ingestion.
- Explainability: every obligation should show “why applicable” and source reference.

## Technical constraints
- Frontend: Next.js + TypeScript + modern accessible design system.
- Backend: Node.js (NestJS preferred) or Python (FastAPI) with clean architecture.
- DB: PostgreSQL.
- Async jobs: Redis queue.
- Storage: S3-compatible object store.
- Auth: OIDC/SAML-ready, JWT sessions, MFA hooks.
- Observability: structured logs, metrics, tracing.

## Data model expectations
Define entities and relations for:
- Tenant, User, Role, Permission
- LegalEntity, Establishment
- WorkforceSnapshot, ContractorSnapshot
- Regulation, Rule, ApplicabilityCondition
- ObligationTemplate, ComplianceTask, TaskRun
- Filing, RegisterRecord, EvidenceDocument
- Notice, Inspection, Incident
- AuditEvent

Include effective dates, state-specific overrides, and legal versioning.

## Workflow requirements
- Onboarding wizard to configure applicability facts.
- Generate obligations from rule engine.
- Compliance task lifecycle: Draft -> In Review -> Approved -> Filed -> Closed.
- Escalation path based on SLA breaches.
- Inspection mode that compiles evidence bundles instantly.

## AI assistant requirements (guardrailed)
- Natural language Q&A over regulations and tenant data.
- Answers must include source citations and confidence level.
- Human approval mandatory for suggested legal responses.
- Do not fabricate statutory references.

## Deliverable depth
- Provide realistic table schemas and indexed fields.
- Include representative API payloads.
- Include at least 10 core UI screens with key components.
- Include migration and seed strategy.
- Include CI/CD and environment configuration notes.

## Quality bar
- Enterprise-grade, secure-by-default, audit-friendly.
- Clear assumptions and explicit out-of-scope list.
- Implementation should be modular and extensible for state-level rule updates.

---

## 11) Discovery Questions to Finalize Before Build

1. Do you want to include **state-level rules** in MVP or only central code obligations first?
2. Which sectors are priority (manufacturing, IT/ITES, logistics, retail, etc.)?
3. Will you support consultants/law firms as first-class multi-client tenants from day one?
4. Which HRMS/payroll systems should be integrated first?
5. What legal workflow depth is needed for notice/litigation management in MVP?
6. Do you require Hindi/regional language support in first release?
7. What deployment model is expected: shared cloud SaaS, VPC, or on-prem enterprise?

---

## 12) Suggested Next Step

Use the “Master Build Prompt” above with your preferred coding LLM, then iterate with a second prompt asking it to:
- produce a **state-wise compliance rule catalog template**, and
- generate a **working MVP skeleton repo** with seed obligations, sample tenants, and dashboard mock data.
