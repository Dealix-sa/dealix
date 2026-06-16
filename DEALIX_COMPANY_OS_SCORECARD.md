# Dealix Company OS Scorecard

A weekly view of every operating system inside Dealix. Updated every Monday during the CEO Loop.

## Purpose
Give the founder a single page that shows which systems are READY, which need FIX, and what evidence backs each score. Drives the weekly operating decision.

## Owner
Sami (Founder).

## Review Cadence
Weekly (Monday morning) and after every major customer event.

## Inputs
- Output of `scripts/verify_full_ops.py`.
- Pipeline tracker counts.
- Approval log entries.
- Weekly intelligence review.
- Customer evidence (paid, delivered, churned).

## Outputs
- Updated scorecard table.
- Top 1–3 fixes for the week.
- Decision triggers to escalate to the doctrine.

## Rules
- Every system must show: score, status, evidence, verification script, next action.
- Status must be one of: `PASS`, `READY INTERNAL`, `FIX`, `BLOCKED`.
- A system without evidence cannot score above 60.
- A system without a verification script cannot score above 75.

---

## Scorecard

| System | Score | Status | Evidence | Verification | Next Action |
|---|---:|---|---|---|---|
| Founder OS | 60 | FIX | `docs/founder/DAILY_COMMAND_BRIEF.md` | `verify_document_quality.py` | Run brief daily for 7 days |
| Strategy OS | 70 | FIX | `docs/strategy/` (22 files) | `verify_document_quality.py` | Reduce to 5 active strategy docs |
| Revenue OS | 50 | FIX | `docs/revenue/OFFER_LADDER.md`, `docs/revenue/PIPELINE_STAGES.md` | `verify_company_os_deep.py` | Add 25 leads + send 25 DMs |
| Acquisition OS | 40 | FIX | `docs/acquisition/` (seeded) | `verify_document_quality.py` | Fill channel playbooks |
| Sales OS | 65 | FIX | `docs/sales/` (32 files) | `verify_document_quality.py` | Bring to standard sections |
| Delivery OS | 70 | FIX | `docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md`, `QA_CHECKLIST.md` | `verify_company_os_deep.py` | Prepare 3 samples |
| Trust OS | 80 | READY INTERNAL | `docs/trust/APPROVAL_MATRIX.md`, `AUTONOMY_POLICY.md` | `verify_company_os_deep.py` | Log every approval for 7 days |
| Learning OS | 55 | FIX | `docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md` | `verify_company_os_deep.py` | Write first weekly review |
| Finance OS | 45 | FIX | `docs/finance/` (seeded) | `verify_document_quality.py` | Connect to `dealix-ops-private` |
| Client Success OS | 45 | FIX | `docs/client_success/` (seeded) | `verify_document_quality.py` | Define retention loop |
| Product OS | 65 | FIX | `docs/product/` (54 files) | `verify_document_quality.py` | Compress to current product surface |
| Content OS | 60 | FIX | `docs/content/` (7 files) | `verify_document_quality.py` | Bring to standard sections |
| People OS | 40 | FIX | `docs/people/` (seeded) | `verify_document_quality.py` | Define hiring loop |
| Agents OS | 50 | FIX | `docs/agents/` (seeded) | `verify_document_quality.py` | Map active sub-agents |
| AI Management OS | 55 | FIX | `docs/ai_management/` (seeded) | `verify_document_quality.py` | Add autonomy roadmap |
| Control Plane OS | 60 | FIX | `docs/control_plane/` (seeded), `docs/ops/OPERATING_LOOPS.md` | `verify_company_os_deep.py` | Wire to weekly review |

---

## Top 3 Fixes This Week

1. **Revenue OS** → load 25 leads, send 25 DMs, log every reply in `pipeline/pipeline_tracker.csv`.
2. **Delivery OS** → prepare 3 sample proof packs in `delivery/research/` and `delivery/reports/`.
3. **Learning OS** → write the first `weekly_intelligence_review.md` with real evidence.

## After First Paid Outcome

When the first payment lands, update the row:

| Revenue OS | 90 | PASS | first payment / PO logged | `verify_company_os_deep.py` | Convert to retainer |

## Metrics
- Number of systems at `PASS` or `READY INTERNAL` this week vs last week.
- Number of `FIX` items closed week over week.
- Time to upgrade a `FIX` to `READY INTERNAL`.

## Evidence
- This file, updated every Monday.
- `scripts/verify_full_ops.py` exit code 0 on the latest commit to `main`.
- Linked private operating files showing real customer activity.

## Last Reviewed
2026-05-23
