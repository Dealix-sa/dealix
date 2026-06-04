# Lead Intake & CRM OS

Schema and **manual** tracking only. No CRM send/push integration is included.
Source of truth: `config/crm_pipeline_schema.json`.

## Lead schema
`lead_id, company_name, website, country, city, vertical_hint, language_hint,
buyer_title_hint, source, source_url, public_contact_type, consent_status,
notes, research_status, risk_notes`

Example data: `data/commercial_seed_leads.example.jsonl` (synthetic, no personal
contact fields). Validate with:
```bash
python scripts/commercial_seed_leads_validate.py
```

## CRM stages
`new → researched → draft_generated → founder_review → manually_contacted →
replied_positive | replied_negative → diagnostic_booked → diagnostic_sold →
pilot_proposed → pilot_sold → retainer` (plus `disqualified`, `suppressed`).

## Rules
- Only **public business** contact points; never scrape individuals.
- `consent_status` tracked; `suppressed` is honored permanently.
- No automated CRM push or send — the founder updates stages manually.
- Privacy-first verticals (legal) require consent-aware handling end to end.
