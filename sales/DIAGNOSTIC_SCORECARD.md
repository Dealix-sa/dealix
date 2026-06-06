# Diagnostic Scorecard — بطاقة تقييم التشخيص المجاني

The deliverable for **Rung 0 — Free AI Ops Diagnostic**. A structured, honest
read of where a prospect stands, ending in one clear recommendation.

## Scoring dimensions (0–5 each, 30 max)

| # | Dimension | What we look at |
|---|---|---|
| 1 | Data readiness | Is commercial data captured, clean, and accessible? |
| 2 | Process clarity | Are sales/ops steps defined or tribal knowledge? |
| 3 | Decision latency | How long from signal to action today? |
| 4 | Governance | Is there any approval/audit trail on outbound actions? |
| 5 | Proof culture | Do they measure outcomes, or assert them? |
| 6 | Revenue leak | Where do opportunities visibly drop? |

## Bands

| Total | Band | Lead recommendation |
|---|---|---|
| 0–10 | Foundational | Start with a Sprint to create the first clean revenue map |
| 11–20 | Operational | Sprint → Data-to-Revenue Pack |
| 21–30 | Scaling | Managed Revenue Ops or Custom AI Setup |

## Output structure (what the prospect receives)

1. The six scores + total, each with a **sourced observation** (no un-sourced claims).
2. The single biggest revenue leak, named plainly.
3. One recommended next rung, with price.
4. The bilingual disclaimer.

## Rules

- Every observation cites where it came from (the prospect's own data/answers).
- Estimated value is labeled estimated. No guarantees (non-negotiable #5).
- The scorecard is **delivered**, not auto-sent — approval gate applies.

## Wired into

- E2E dry run: `scripts/run_dealix_e2e_dry_run.py` produces a sample scorecard.
- Customer workspace: lands in `02_diagnostic_summary.md`.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
