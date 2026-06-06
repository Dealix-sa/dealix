# Dealix — Private Launch Readiness

> Generated for Wave 7. Run `python scripts/verify_dealix_launch_readiness.py`
> for the live asset score and `bash scripts/run_dealix_full_verification.sh`
> for the full gate report.

**Asset readiness score:** 100/100 → **Private Launch Ready** (threshold to start: ≥ 70).

> Scoring bands: 0–49 No-Go · 50–69 Internal Only · 70–84 Private Launch Ready · 85–100 Public Limited Ready.

## The 10 questions

| # | Question | Answer | Basis |
|---|----------|--------|-------|
| 1 | Is Dealix ready for private launch? | **Yes** | Asset score 100/100; frontend build passes; safety gates green. |
| 2 | Is Command Sprint sellable? | **Yes** | `landing/command-sprint.html`, one-pager, scope template all present. |
| 3 | Is Start/Diagnostic path ready? | **Yes** | `landing/start.html` + `landing/diagnostic.html`, both linked from funnel. |
| 4 | Is Sales Kit ready? | **Yes** | `sales/COMMAND_SPRINT_ONE_PAGER.md` + diagnostic script. |
| 5 | Is Customer Folder template ready? | **Yes** | `customers/_template/` — 12 files, creation script tested. |
| 6 | Is Proof Pack template ready? | **Yes** | `customers/_template/10_proof_pack.md` + `data/templates/proof_pack_ar.md`. |
| 7 | Is Governance ready? | **Yes** | Claims Register + Human Approval Policy under `docs/governance/`. |
| 8 | Are unsafe claims removed? | **Yes** | Negation-aware + allowlist scan passes; no positive guarantees on the surface. |
| 9 | Can the founder manually deliver the first 3 sprints? | **Yes** | Engagement is founder-led; every step has a template + ledger. |
| 10 | What blocks private launch? | **Nothing blocking** | Remaining items are public-launch / hygiene (see below). |

## Verdict
- **Private launch: GO.** Send up to 5 founder-approved messages manually.
- **Public launch: NOT YET.** Public launch needs the P1 hygiene items cleared
  (lint drift, security-smoke fixture findings) and a live payment path configured.

## Top 10 required fixes (priority order)
1. Configure manual payment + (later) Moyasar live cutover before charging beyond manual.
2. Clean `make security-smoke` findings (test fixtures using `sk_live_*`/`ghp_*` patterns; `.env.*.example` files flagged). Pre-existing — not a private-launch blocker.
3. Address frontend `npm run lint` drift (pre-existing; not a correctness gate).
4. Fill real companies into `data/growth/first_30_targets.csv` (replace placeholders).
5. Add `evidence_url` or a warm-intro reason to every target before status `approved`.
6. Finalize pricing on `command-sprint.html` / `pricing.html` (no guaranteed-outcome copy).
7. Confirm refund-window wording matches the Claims Register (#7) everywhere.
8. Re-run `bash scripts/run_dealix_full_verification.sh` and attach the report to the PR.
9. Verify `landing/security.html` reflects the current data boundary + PDPL posture.
10. Dry-run one customer workspace end-to-end before the first real customer.

## Top 10 founder actions (this week)
1. Approve or rephrase the first safe outreach message.
2. Pick the first 5 real targets and add evidence/warm-intro.
3. Send 5 manual messages (no automation).
4. Open 3 diagnostic slots.
5. Run diagnostics; score fit honestly; redirect non-fits.
6. Send the first Command Sprint proposal.
7. Confirm the first manual payment; log it in `09_delivery_log.md`.
8. Create the customer workspace (`scripts/create_customer_workspace.py`).
9. Deliver Day 1; keep the Approval Register current.
10. Run a weekly CEO review; choose the next segment.

## Exact first outreach plan
1. Shortlist 5 targets from `first_30_targets.csv` (status `research` → `approved` only with evidence).
2. For each, the sales sub-agent drafts the safe message into `data/revenue/outreach_queue.jsonl` (`approval_status: draft`).
3. Founder reviews in `reports/revenue/outreach_approval_queue.md`, edits, sets `approved`.
4. Founder sends manually (WhatsApp/email), then marks `sent`.
5. Log replies on the target row; book diagnostics for positive replies.
6. Never exceed 5 sends in the first batch; learn, then iterate.

---
_Do not begin private launch unless this score is ≥ 70. It is 100 — you are clear to start manual sends._
