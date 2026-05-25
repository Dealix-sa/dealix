# Partner Revenue Machine

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external and irreversible actions.

## Purpose

Turn partners into qualified referral and co-sell channels. In Saudi B2B, a warm intro through a credible operator converts faster than cold outreach. Partner motion is therefore a first-class distribution channel, not an afterthought.

## Partner Types

| Type | Description |
|------|-------------|
| Consultants | Independent advisors with buyer relationships |
| Agencies | Marketing, sales, or implementation agencies |
| ERP implementers | Integration partners with active enterprise accounts |
| Cybersecurity advisors | Trusted operators in regulated industries |
| Accountants | CFOs and accounting firms with SME relationships |
| Startup ecosystem operators | Accelerator, fund, hub operators |
| Chamber / event contacts | Sector association and event organizers |

## Weekly Partner Motion

| Activity | Volume (warmup) |
|----------|-----------------|
| Referral asks | 10 per week |
| Partner conversations | 3 per week |
| Co-sell opportunities surfaced | 1 per week |
| Qualified intros received | 1 per week |

Volumes are warmup targets; they are not commitments to a partner.

## Core Rules

- A partner cannot promise an outcome on Dealix's behalf.
- A partner cannot change price or scope on Dealix's behalf.
- Commission is paid only on **collected cash**, never on pipeline or signed PO alone.
- Every referral is tracked with its source partner.
- A partner who consistently sources bad-fit leads is given feedback once, then deprioritized.
- A partner relationship that produces no qualified intros over a two-month window is reviewed and either repositioned or paused.

## Referral Ledger

A referral ledger records:

- Source partner
- Referred account
- Date of intro
- Status (open / qualified / proposal / paid / closed-lost / suppressed)
- Commission terms
- Commission paid (if any)
- Source-evidence link to the cash event (if paid)

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Weekly | Partner motion review: who got asked, who responded, who delivered intros |
| Monthly | Partner scorecard: intros, conversions, cash, complaints |
| Quarterly | Partner mix review: which types to invest in, which to retire |

## Runtime Wiring

- Existing partner docs (6 files in `docs/partners/`) provide partner program and pitch material.
- Audit log (records every external touch including partner outreach): `db/models.py::AuditLogRecord`.
- Revenue events (track partner-sourced cash): `auto_client_acquisition/revenue_memory/event_store.py`.
- Lead intelligence base (where referred accounts land): `db/models.py::LeadRecord`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Qualified intros received per month | tracked, trending up | referral ledger |
| Referral-to-paid conversion | tracked, expected higher than cold baseline | revenue events |
| Active partner relationships | tracked | partner scorecard |
| Commission paid per quarter | tracked | finance |
| Partners deprioritized for bad-fit pattern | tracked; signal for sourcing fix | scorecard |

## Cross-Links

- Existing partner docs in `docs/partners/`
- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/distribution/ABM_STRATEGIC_ACCOUNT_MACHINE.md`
- `docs/legal/COMMERCIAL_CONTRACT_PACK.md`
- `docs/founder/REVENUE_WAR_ROOM_OS.md`
- `docs/finance/BILLING_RECEIVABLES_OS.md`

## Open Items

- A first-class `partner` and `referral` table do not yet exist in `db/models.py`; today the ledger is a markdown / spreadsheet artifact.
- A partner-portal product surface (so partners can submit intros without email) is not in scope this quarter.
- Standard partner agreement template is referenced in `docs/legal/COMMERCIAL_CONTRACT_PACK.md` but lives across files today.
