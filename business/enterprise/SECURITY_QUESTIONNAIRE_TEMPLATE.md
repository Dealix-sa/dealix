# Enterprise Security Questionnaire — Dealix Standard Response Template

Use this when a buyer sends their security/IT questionnaire. Founder edits before sending.

## 1. Company

- Legal entity: Dealix SA
- HQ: Riyadh, Saudi Arabia
- Primary contact: founder
- Data center region: customer-chosen (default KSA)

## 2. Application architecture

- Frontend: Next.js 15 (Node 22), deployed on managed PaaS.
- Backend: FastAPI + Python 3.12, deployed on Railway or customer-chosen IaaS.
- Data store: PostgreSQL (managed) + object storage for proof artifacts.
- Secrets: environment-managed; never committed; rotated quarterly.

## 3. Access control

- Production access restricted to the founder until the customer's IdP is wired.
- SAML 2.0 + OIDC ready (`api/security/saml.py`, `oidc.py`).
- SCIM provisioning ready (`api/security/scim.py`).
- MFA enforced on all admin accounts (`api/security/mfa.py`, `mfa_policy.py`).

## 4. Data handling

- Customer data stays in customer systems; Dealix processes copies under the agreed scope.
- Retention: per `business/governance/CLIENT_DATA_RETENTION_POLICY.md`.
- Deletion-on-request: documented in `docs/security/DATA_RETENTION_AND_DELETION.md`.
- Encryption at rest: managed by PaaS provider. Encryption in transit: TLS 1.2+.

## 5. AI usage

- Default mode: deterministic. No customer data sent to third-party LLM by default.
- LLM-assist mode: opt-in per customer; provider/model logged with every call.
- No automated outbound messaging. Human approves every outbound communication.

## 6. Logging and audit

- Privileged audit log: `api/middleware/privileged_audit.py`.
- Append-only event ledger: `business/_data/audit_log.json`.
- Approval matrix tracked per outbound action.

## 7. Incident response

- See `docs/ops/INCIDENT_RESPONSE_RUNBOOK.md`.
- Customer notification within 72 hours of confirmed incident affecting their data.

## 8. Sub-processors

- PaaS (Railway / Vercel) — published list available on request.
- LLM providers — only those the customer opts into.
- No marketing / analytics SDKs on customer-facing data flows by default.

## 9. Certifications

- Operational scaffolds ready for SOC 2 Type I / ISO 27001 Stage 1. Formal attestation is a roadmap item; no false claim is made today.

## 10. Out of scope

- Dealix does not sell customer data. Ever.
- Dealix does not scrape platforms in violation of their terms.
- Dealix does not send cold automated messages.
