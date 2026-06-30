# 23 — Lead Ops Final QA

فحص نهائي لعمليات العملاء المحتملين. مطابق لـ `config/crm_pipeline_schema.json` ومُتحقّق آليًا.
Final QA for lead operations, aligned to `config/crm_pipeline_schema.json` and machine-verified by
`scripts/commercial_crm_schema_verify.py`.

## Checklist
- [ ] **Lead schema** — required fields present (`lead_id, company, vertical, contact_role, source, stage, priority_score, consent_basis, created_at`)
- [ ] **CRM stages** — only allowed stages used
- [ ] **Suppression** — unsubscribe / complaint / do-not-contact move lead to `suppressed` and block future drafts
- [ ] **Manual approval** — outreach only after founder approval
- [ ] **Reply classification** — interested / not_now / not_interested / wrong_contact / unsubscribe / spam_complaint
- [ ] **Diagnostic booked** — stage `discovery_booked`
- [ ] **Pilot proposed** — stage `pilot_proposed`
- [ ] **Retainer conversion** — stage `retainer`
- [ ] **Disqualification** — stage `disqualified` with reason
- [ ] **Source tracking** — every lead has a `source`
- [ ] **No sensitive personal data** — no national IDs / financial / health before agreement

## Verification
```bash
python scripts/commercial_crm_schema_verify.py
# -> outputs/final_launch_control/crm_schema_verification.json (pass: true)
```

## Forbidden fields (must never appear)
`send_now`, `auto_send`, `smtp_password`, `outbound_token`, `api_key`, `access_token`.

## Decision
- **GO** for manual, approved, consent-based lead operations.
- **NO-GO** for any automated sending or sensitive-data collection before agreement.
