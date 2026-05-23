# Partner Attack System

> Partners are the second highest-leverage channel after warm intros.
> This system makes partner motion *strategic* instead of opportunistic.

## Partner types we attack first

1. **Agencies** (marketing, digital transformation, ERP implementers)
   — they own the buyer relationship.
2. **ERP / CRM vendors** — they own the system of record.
3. **Cybersecurity / GRC firms** — they own the trust conversation.

## Source of truth

`<PRIVATE_OPS>/partners/partner_pipeline.csv`

```
partner_id,company,type,website,relationship_path,offer_fit,
referral_potential,white_label_potential,trust_risk,status,next_action
```

- `type` ∈ {`agency`, `erp_crm`, `cybersecurity_grc`, `consultancy`, `other`}.
- `referral_potential` ∈ {`high`, `medium`, `low`}.
- `white_label_potential` ∈ {`yes`, `no`, `governance_review`}.
- `status` ∈ {`prospect`, `intro_meeting`, `pilot_partner`,
  `active`, `paused`, `terminated`}.

## Doctrine

- No partner promises revenue share or referral fee outside the
  approved partner terms (see `PARTNER_REFERRAL_TERMS_GUARDRAILS.md`).
- No white-label deal without a governance review row.
- No partner sees customer data without an executed data-processing
  agreement.

## Run

```bash
make partner-pipeline PRIVATE_OPS=/opt/dealix-ops-private
```

Produces `<PRIVATE_OPS>/partners/partner_pipeline_report.md`.
