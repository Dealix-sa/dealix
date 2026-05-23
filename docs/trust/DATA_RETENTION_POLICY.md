# Data Retention Policy

> What data we collect, where it lives, how long, and how it gets deleted.
> Enforced by `dealix/trust/data_retention.py`.

## Data Categories

| Category | Examples | Storage | Retention |
|---|---|---|---|
| Public lead data | Company name, public role, public URLs | Public-safe metadata in pipeline | indefinite (audit trail) |
| Buyer contact | Email, LinkedIn URL, phone (if provided) | Private repo `pipeline/` | 24 months from last interaction |
| Client engagement data | Sprint deliverables, conversations, notes | Private repo `clients/{client}/` | Duration of engagement + 24 months |
| Client confidential data | Anything client labels confidential | Private repo, encrypted at rest | Duration of engagement + 6 months unless DPA specifies otherwise |
| Approval logs | Trust gate logs, decisions | Private repo `trust/` | 7 years (audit) |
| Financial records | Invoices, payments | Private repo `revenue/` | 10 years (Saudi tax) |
| Personal identifying info (PII) we don't need | — | Not collected | n/a |

## Storage Locations

- **Public repo** (`voxc2/dealix`): public-safe artifacts only. No buyer contacts, no client data.
- **Private repo** (`dealix-ops-private`): all operational data, client work, financial records, approval logs.
- **Third-party (Stripe, banking, etc.)**: covered by provider DPAs; never duplicated.
- **Local founder machine**: ephemeral working copies; must sync to private repo daily; never the source of truth.

## Sensitive Storage Tier

For Custom AI / Revenue Desk clients, data may include integration credentials, CRM data, or operational data. Tier:
- Encrypted at rest
- Access limited to founder (no agent access without explicit per-action approval)
- DPA-driven retention (typically 30 days post-engagement)
- Deletion proof generated on offboarding

## Collection Discipline

- Collect only what's needed for the engagement
- Never collect: credit card numbers, government IDs, employee PII, sensitive personal data (health, religion, etc.)
- Buyer-volunteered data is not implicit consent for broader use

## Deletion Triggers

- Client engagement ends + DPA retention period expires → automatic deletion (logged)
- Lead opt-out received → contact info purged, supression-list entry retained
- Suppression list addition (auto-flagged) → contact stored in suppression list only, full record purged
- Manual deletion request → 30-day fulfillment

## Deletion Mechanism

- `dealix/trust/data_retention.py` runs a scheduled review
- Generates a deletion report per cycle
- Founder approves the report → mass-delete
- Deletion log retained in `trust/deletion_log.csv`

## Backup Posture

- Public repo: GitHub default
- Private repo: GitHub default + local founder backup (encrypted)
- Financial records: cloud storage with provider redundancy
- No long-lived backups outside these (no "just in case" copies on USB drives, etc.)

## What This Policy Refuses

- Storing PII we don't need
- "Just in case" data collection
- Cross-purposing data (e.g., using a client's data for prospecting)
- Long-lived backups outside approved storage
- Sharing data with third parties without explicit consent
- Selling, renting, or otherwise monetizing customer data

## Saudi PDPL Alignment Notes

(Not legal advice; for engagement DPA reference)

- Lawful basis for processing: contract performance + legitimate interest (clearly stated to data subject)
- Data subject rights: access, correction, deletion (we accommodate within 30 days)
- Data localization: data on GitHub (US-hosted) — disclose to clients; offer Saudi-hosted private storage on Custom AI tier
- Breach notification: per incident response plan, < 72 hours
- DPO: founder (until size warrants designated)

## Review Cadence

- Monthly: deletion run + log review
- Quarterly: data inventory audit
- Annually: full policy re-review against Saudi PDPL updates
