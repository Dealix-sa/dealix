# Paid Sprint Handoff — تسليم الـ Sprint المدفوع

When a target accepts the **7-Day Revenue Intelligence Sprint (499 SAR)**, this
is the handoff from sales into delivery. It is the gate between "money agreed"
and "work started".

## Pre-conditions (all must be true)

- [ ] Offer accepted and recorded in `data/revenue/pipeline.jsonl` (`stage: won`).
- [ ] Payment arranged per `sales/COMMAND_SPRINT_TERMS.md` (no live charge without approval — non-negotiable #8).
- [ ] A customer workspace exists: `python scripts/create_customer_workspace.py --name "<client>"`.
- [ ] Source data received with a clear **Source Passport** (origin, owner, consent).

## The 7-day shape

| Day | Step | Workspace file |
|---|---|---|
| 1 | Intake + Source Passport + DQ score | `00_intake.md`, `01_company_intelligence.md` |
| 2 | Diagnostic summary | `02_diagnostic_summary.md` |
| 3 | Sprint scope locked | `03_command_sprint_scope.md` |
| 4 | Revenue map (accounts scored) | `04_revenue_map.md` |
| 5 | Draft pack + governance review | `05_proof_register.md`, `06_approval_register.md` |
| 6 | Proof Pack assembled (score ≥ 70) | `10_proof_pack.md` |
| 7 | Upsell recommendation + handoff | `11_upsell_recommendation.md`, `08_executive_command_brief.md` |

## Definition of done

- Proof Pack score **≥ 70**.
- At least **one Capital Asset** registered in `data/revenue/proof_assets.jsonl`.
- Every customer-facing file ends with the bilingual disclaimer.
- An Upsell recommendation exists, mapped via the
  [Proof → Upsell Playbook](PROOF_TO_UPSELL_PLAYBOOK.md).

## Handoff record

The completed handoff is logged in the customer's `09_delivery_log.md` and
reflected in the next `scripts/founder_daily_command.py` run.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
