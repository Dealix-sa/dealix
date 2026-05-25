# Build / Defer / Kill — قرار البناء أو التأجيل أو الإلغاء

## Purpose
A single decision rule applied to every feature intake. Replaces opinion with a rubric. Forces explicit Kill or Defer; "maybe later" is not an option.

## Owner
Founder. Decision made within 7 days of intake filed.

## Inputs
- Feature intake from `docs/product/FEATURE_INTAKE.md`.
- Current proof gate status from `docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md`.
- Cash and runway snapshot from `docs/finance/`.
- Productization stage of related workflow.

## Outputs
- Stamped decision: BUILD / DEFER / KILL with reason and review date.
- Log entry in `docs/product/intake/FT-YYYY-NNN.md`.
- If BUILD: scope, owner, deadline, kill criterion.
- If DEFER: re-review date and what evidence would unlock it.
- If KILL: reason, never re-opened without new evidence.

## The Rubric
| Signal | BUILD | DEFER | KILL |
|---|---|---|---|
| Distinct paying clients requesting | ≥ 3 | 1-2 | 0 |
| Workflow stage | Template+ | Manual | Hypothetical |
| Estimated margin impact | ≥ 60% per run | 30-59% | < 30% |
| Build hours | ≤ 40h | 40-120h | > 120h pre-proof |
| Touches `docs/product/NO_OVERBUILD_POLICY.md` | Auto-Kill | Auto-Kill | Auto-Kill |
| Stage of company | Proof of Delivery passed | Pre-proof | Pre-proof + speculative |

## Rules
1. Any feature listed in `docs/product/NO_OVERBUILD_POLICY.md` is auto-Kill regardless of votes.
2. No BUILD without an explicit kill criterion (what would make us stop).
3. DEFER must name the evidence needed to revisit, and a calendar date.
4. KILL is final unless new client evidence arrives.
5. Estimated impact is labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Metrics
- BUILD count, DEFER count, KILL count per month.
- Kill rate target: ≥ 40% (discipline).
- BUILD-on-time delivery rate.
- BUILD post-launch usage (must be reviewed in 30 days).

## Cadence
- Weekly triage of new intakes.
- Monthly review of DEFER queue.
- Quarterly review of KILL list (only to confirm, not revive).

## Evidence
- Decision log in intake file.
- Founder signature.

## Verifier
Founder. No counter-veto; founder is final.

## Runtime Command
`make feature-decide FT=<id>` — prints the rubric, requires explicit BUILD/DEFER/KILL with reason and kill criterion before saving.

## Arabic Summary — ملخص عربي
كل طلب ميزة يُحسم خلال 7 أيام: بناء، أو تأجيل، أو إلغاء. لا توجد خانة "ربما". أي ميزة في قائمة "لا نبني" تُلغى تلقائيًا. القيم التقديرية ليست مُتحقَّقة.
