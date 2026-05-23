# Done-For-You Acquisition OS

## Purpose
Move Dealix from "founder-thinks-about-leads" to "founder-approves-leads". The OS
prepares qualified sector batches, drafts outreach, and queues founder approval
gates so nothing leaves the building without explicit sign-off.

## Operating Mode
- `mode: draft_only`
- No external send without founder approval.
- No cold WhatsApp. No LinkedIn automation. No scraped personal data.
- Public business contact paths only (see `CONTACT_DISCOVERY_POLICY.md`).
- No guaranteed-revenue, guaranteed-reply, or guaranteed-meeting claims in
  copy (gate enforced by `tests/acquisition/test_erp_crm_batch.py`).

## Flow
1. **Sector pick** — choose a sector with B2B buyers + high LTV.
2. **Source target list** — `acquisition/source_targets.csv` lists directories
   / search queries to mine.
3. **Seed batch** — `acquisition/lead_batches/<date>-<sector>-seed.csv`
   captures company-level rows (no personal data).
4. **Scoring** — `scripts/score_lead_batch.py` writes A/B/C priority based on
   `fit_score`.
5. **Outreach drafting** — `scripts/generate_outreach_for_batch.py` produces
   per-lead first-touch + follow-up drafts in EN+AR.
6. **Contact discovery** — `acquisition/contact_discovery_queue.csv` records
   the public contact path per company (form, sales email, partnership email).
7. **Approval queue** — `scripts/generate_outreach_approval_queue.py` builds
   `acquisition/approvals/<batch>.md`. Founder marks Approved / Edit / Reject.
8. **Send queue** — only Approved rows flow to
   `scripts/build_outreach_send_queue.py`, which writes a queue file the
   founder uses to create Gmail drafts manually (no auto-send).
9. **Reply handling** — positive replies trigger the Revenue Sprint sample
   pack (`docs/delivery/REVENUE_SPRINT_SAMPLE_TEMPLATE.md`); proposal trigger
   rules live in `docs/revenue/PROPOSAL_TRIGGER_RULES.md`.

## Non-Negotiables
- No fabricated CRM/KPI numbers.
- No revenue claim before invoice paid.
- No upsell before proof.
- Every batch passes `scripts/verify_done_for_you_acquisition.py` before push.
- Every approval state change is logged in the approval queue file.

## Current Batches
- `2026-05-23-erp-crm-seed.csv` — Saudi ERP / CRM vendors (Batch 1).
