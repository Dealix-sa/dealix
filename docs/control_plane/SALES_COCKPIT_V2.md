# Sales Cockpit v2

## Relationship to existing docs
Complements, does not replace:
- `dealix/commercial_ops/founder_cockpit.py` and `tests/test_founder_cockpit.py` — the existing in-process founder cockpit module remains the source of truth for built-in cockpit logic.
- `docs/ops/CEO_TOP50_TRACKER.csv` — strategic account row source.
- `docs/ops/DAILY_OPERATING_LOOP.md` — daily operating cadence the cockpit feeds.

The Sales Cockpit v2 is a **generated markdown artifact** at `docs/founder/sales_cockpit.md`, produced by `scripts/generate_sales_cockpit.py` from private-ops CSVs. It is a CEO surface, not a replacement module.

## Purpose
Give the founder one commercial command center for all distribution and conversion work.

## Panels
1. Lead Intelligence Base
2. Outreach Pending Approval
3. Ready-to-Send Queue
4. Follow-Ups Due
5. Positive Replies
6. Sample Queue
7. Proposal Queue
8. Payment Capture Queue
9. Delivery Triggers
10. Retention / Proof / Referral
11. Trust Risks
12. Today's Top CEO Action

## CEO Actions
Approve batch.
Reject weak leads.
Approve drafts.
Push sample.
Approve proposal.
Push payment.
Start delivery.
Ask retainer.
Request proof.
Ask referral.

## Rule
The cockpit surfaces decisions. The founder should not search through raw files.

## Generation
- Input: `/opt/dealix-ops-private/{growth,intelligence,outreach,sales,finance,client_success}/*.csv`
- Script: `scripts/generate_sales_cockpit.py`
- Output: `docs/founder/sales_cockpit.md`
- Cadence: every 30 minutes via `deploy/cron/dealix_growth_factory.cron`.
