# Dealix Legal / Trust / Security

This layer covers PDPL, DPA, incident response, retention, and the
operational trust contract with customers and regulators.

## PDPL (Personal Data Protection Law — KSA)

Dealix processes personal data as a **data processor** acting on behalf
of the customer (data controller). Every engagement carries a DPA.

Controls:
- PII redaction middleware at the request boundary (`api/middleware/`).
- Source passport gates what data Dealix may ingest.
- Access logged with `governance_decision` field.
- Right-to-erasure exercise documented in `docs/SECURITY_RUNBOOK.md`.

## DPA (Data Processing Addendum)

Template: `docs/legal/DPA_TEMPLATE.md` (boilerplate to be reviewed by
counsel before first enterprise signing).

Required clauses:
- Roles (controller / processor)
- Purpose of processing
- Categories of data + data subjects
- Sub-processors (must be approved by controller)
- Security measures (see SECURITY_RUNBOOK)
- Incident notification (within 72h)
- Data retention (see below)
- Data deletion / return on contract end

## Incident response

Playbook: `docs/SECURITY_RUNBOOK.md`. Summary:

1. Detect (alerting, customer report, audit anomaly).
2. Triage (severity 1 = data loss; 2 = service down; 3 = degraded).
3. Contain (revoke keys, isolate services).
4. Notify (founder + impacted customers within SLA).
5. Postmortem within 72h published to `docs/postmortems/`.

## Data retention

| Data class | Retention |
|---|---|
| Audit logs | 365 days local, optional S3 longer with founder approval |
| Customer data ingested | Per Source Passport (default 90 days post-engagement) |
| Proof Packs | Indefinite (Capital Asset) |
| PII redaction logs | 30 days |
| Approval decisions | 365 days |

## Trust artifacts published

- Status page (`docs/SLO.md`)
- Security overview (`docs/SECURITY_RUNBOOK.md`)
- On-call coverage (`docs/ON_CALL.md`)
- Subprocessor list (`docs/legal/SUBPROCESSORS.md` — to be created)

## Verifier

`make legal-trust-security` runs `scripts/verifiers/verify_legal_trust_security.py`.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
