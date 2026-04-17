# Pre-Build Discovery Questions for ComplyEdge

Use this checklist to collect stakeholder decisions before implementation.

---

## 1) Scope & Coverage
1. Codes in MVP: all 4 labour codes at once, or start with 1–2 (for example, Code on Wages + Code on Social Security) and stage the rest?
2. Central vs. state rules: should MVP cover only central obligations, or include state-level rules from day one?
3. If state-level is included, which states are priority first (for example, Karnataka, Maharashtra, Tamil Nadu)?
4. Sector focus: which sectors are in scope first (manufacturing, IT/ITES, logistics, retail, BFSI, gig/platform)?
5. Establishment types: which are in scope (factory, shop & establishment, mine, plantation, beedi/cigar, motor transport)?
6. Worker categories: regular employees only, or also contract workers, inter-state migrants, gig/platform workers, apprentices in MVP?

## 2) Multi-Tenancy & Personas
7. Consultant/agency mode: is multi-client consultant mode a Day-1 requirement or Phase 2?
8. Tenant size targeting: SME, mid-market, or large enterprise first?
9. Personas in MVP: which personas need full workflows in MVP vs read-only?
10. Org hierarchy depth: is Tenant → Legal Entity → Establishment → Department enough, or are cost-centers/projects/sites also required?

## 3) Rule / Applicability Engine
11. Rule sourcing: authored manually by compliance team, ingested from legal data provider, or extracted from reference PDFs with human review?
12. Rule update cadence and ownership: who maintains changes when notifications/amendments are issued?
13. Explainability format: plain-language “why this applies” with citations, or structured machine-readable trace of evaluated conditions?
14. Effective dating: should MVP support back-dated audits (for example, “what applied on 1-Jan-2024”) or only current-state evaluation?

## 4) Integrations
15. HRMS/payroll priority integrations: which systems first (for example, SAP SuccessFactors, Darwinbox, Keka, Zoho People, GreytHR, Razorpay Payroll, Workday)?
16. Government portals: direct submission integrations (Shram Suvidha, EPFO, ESIC, state portals) or form generation for manual upload in MVP?
17. SSO providers: which IdPs to support first (Azure AD, Okta, Google Workspace)?

## 5) AI Co-pilot
18. AI co-pilot in MVP or Phase 2?
19. Grounding strategy: legal references only, or legal references + tenant data (with strict tenant isolation)?
20. LLM provider and residency constraints: OpenAI, Anthropic, self-hosted, and India residency requirements?
21. Allowed actions: read-only Q&A, or draft notices/responses with mandatory human approval?

## 6) Localization & Regional
22. Language support in first release: English-only, or include Hindi/regional languages (for example, Tamil, Marathi, Bengali, Kannada)?
23. Reporting format requirements: Indian numbering style (lakhs/crores) and localized date/time formats?

## 7) Deployment, Security, and Data Residency
24. Deployment model at launch: shared SaaS only, or also VPC-isolated and/or on-prem options?
25. Data residency: India-only hosting required? Any DPDP Act 2023-specific workflows needed in MVP?
26. Tenant isolation: row-level security for all, or schema/DB isolation options for enterprise tiers?
27. Target certifications/compliance posture: SOC 2, ISO 27001, CERT-In, others?

## 8) Workflow & Process
28. Approval chains: fixed maker-checker-approver or tenant-configurable by task type?
29. SLA/escalation: tenant-configurable SLAs or platform defaults?
30. Notification channels in MVP: email + in-app only, or include WhatsApp/SMS?
31. Evidence bundle export format: PDF only, or encrypted ZIP with manifest and chain-of-custody metadata?

## 9) Tech Stack Confirmation
32. Backend framework choice: NestJS or FastAPI?
33. Repository strategy: monorepo or polyrepo?
34. ORM choice: Prisma, TypeORM, Drizzle, SQLAlchemy, or other?
35. Async architecture: BullMQ/Redis, RabbitMQ, SQS, or hybrid?
36. Object storage strategy: AWS S3, MinIO (self-hosted), or both?
37. Search strategy: OpenSearch from MVP, or PostgreSQL full-text search first and OpenSearch later?

## 10) Build Approach for This Repository
38. What should be built first?
   - (a) MVP skeleton repo and runnable scaffolding
   - (b) Rule catalog + applicability engine first
   - (c) State-wise compliance rule catalog template first
   - (d) PRD + ERD + OpenAPI package first, then code
39. Definition of done for this initial pass: runnable local stack with seeded dashboard, or architecture/spec artifacts only?

---

## Suggested Answer Template (for stakeholders)
Provide answers inline using this format:

- **Q1:** <answer>
- **Q2:** <answer>
- ...
- **Q39:** <answer>

---

## Captured Stakeholder Answers (2026-04-16)

> These answers were captured from stakeholder comments and should be treated as the current baseline until explicitly revised.

- **Q1:** All 4 labour codes in MVP.
- **Q2:** Include both Central and State obligations from Day 1.
- **Q3:** All sectors.
- **Q4:** All industries except plantation, beedi/cigar, mines, and transportation.
- **Q5:** All worker categories.
- **Q6:** Employer persona is primary; agency/consultancy is secondary.
- **Q7:** Pricing is not based on organization size; pricing drivers include number of Acts, reports, downloads, vendor portals, marketplace access/listing.
- **Q8:** All roles in scope; role permissions should be customizable by Platform Admin per tenant.
- **Q9:** Org hierarchy confirmed as Tenant → Legal Entity → Establishment → Department.
- **Q10:** Rules extracted via LLM from PDFs, with API support for external legal data providers.
- **Q11:** Platform Admin can update and push rules to tenants as the source of truth; tenant-level updates are also allowed.
- **Q12:** Default explainability should be plain-English; offer optional structured trace for customers who need it.
- **Q13:** Current-state applicability only; historical back-dated applicability not needed before customer signup date.
- **Q14:** API integration with HRMS/payroll systems is required.
- **Q15:** Direct submission integration with statutory/government portals is required.
- **Q16:** SSO is mandatory; MFA is also mandatory.
- **Q17:** AI co-pilot required in Phase 1.
- **Q18:** Clarification requested by stakeholder.
- **Q19:** Customers should have option to use any LLM provider.
- **Q20:** AI action scope should be read-only.
- **Q21:** Multi-language UI required, with user-level language preference persistence; translation should support Sarvam.ai and major Indian languages.
- **Q22:** Currency should be configurable in settings; default INR; exchange rates sourced from xe.com.
- **Q23:** Multi-tenant SaaS with dedicated database per client.
- **Q24:** Data residency in India.
- **Q25:** RLS mandatory at platform level, tenant level, and intra-tenant user-profile level.
- **Q26:** Target compliance posture includes ISO 27001, SOC 2, DPDP Act (India), and CERT-In.
- **Q27:** Approval chain configurable per tenant/task type.
- **Q28:** SLA/escalation should use platform-defined defaults.
- **Q29:** Notifications via email, in-app, WhatsApp, and SMS.
- **Q30:** Evidence export starts with PDF.
- **Q31:** Backend framework preference is FastAPI.
- **Q32:** Clarification requested by stakeholder.
- **Q33:** ORM preference is Prisma or Drizzle.
- **Q34:** Async architecture preference is full broker.
- **Q35:** Object storage preference is Azure Blob.
- **Q36:** Search preference is OpenSearch.
- **Q37:** Build sequence preference includes all four tracks: (a), (b), (c), and (d).

### Open Clarifications
- **Q18:** Grounding strategy (legal references only vs legal references + tenant data) needs explicit confirmation.
- **Q32:** Repository strategy (monorepo vs polyrepo) needs explicit confirmation.
- **Q38/Q39 equivalents:** Need explicit decision on execution order and definition of done for the initial milestone.
