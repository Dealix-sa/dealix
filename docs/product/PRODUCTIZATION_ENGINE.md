# Productization Engine — محرك التحويل لمنتج

## Purpose
Define the exact mechanical pipeline that converts a one-off paid service into a templated workflow, then into an automated workflow, then into a SaaS candidate. The engine is sequential and earns its way forward; nothing skips a stage.

## Owner
Founder. Operated by delivery analyst with weekly founder review.

## Inputs
- Signed Statement of Work (paid).
- Delivery artifact stored under `evidence/delivery/<sprint_id>/`.
- Client feedback evidence per `docs/client_success/FEEDBACK_LOOP.md`.
- Workflow run logs.

## Outputs
- Stage promotion decisions.
- Reusable templates checked into `templates/`.
- Automated workflow registered in `docs/product/WORKFLOW_REGISTRY.md`.
- SaaS candidate brief (only when all gates pass).

## Rules — The 3 → 5 → 10 Ladder
| Stage | Gate | Evidence required | Decision |
|---|---|---|---|
| Manual | 3 paid runs delivered | Signed SOW + delivery artifact + client feedback | Promote to Template |
| Template | 5 templated runs, rework < 10%, NPS ≥ 7 | Template file + 5 run logs + rework log | Promote to Automation |
| Automation | 10 automated runs, margin > 60%, < 1 escalation per 10 | 10 run logs + margin proof + escalation log | Promote to SaaS Candidate |
| SaaS Candidate | See `docs/product/SAAS_CANDIDATE_RULES.md` | Full candidate brief | Build / Defer / Kill |

Non-negotiables:
1. No automation before 5 successful templates.
2. No SaaS before 10 successful automations.
3. No marketing of an "AI product" before SaaS gate is passed.
4. Skipping a stage triggers an A3 review.
5. Estimated ROI is labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Metrics
- Time at each stage (median days).
- Stage promotion rate.
- Rework rate per template.
- Margin per automated run.
- Escalations per 10 automated runs.

## Cadence
- Weekly: candidate stage review with `docs/product/PRODUCTIZATION_COMMAND_CENTER.md`.
- Monthly: promotion decisions documented.
- Quarterly: SaaS candidate decision.

## Evidence
- `evidence/productization/<candidate>/stage_<n>/` per stage.
- Client written approval for any external mention.

## Verifier
Founder. Delivery analyst supplies counts; founder signs the promotion. Disagreement triggers hold, not override.

## Runtime Command
`make productization-promote CANDIDATE=<id>` — checks gates, prints missing evidence, refuses promotion if any gate fails.

## Arabic Summary — ملخص عربي
المحرك يتقدم من يدوي إلى قالب إلى أتمتة إلى منتج، بالترتيب فقط. لا قفز بين المراحل. كل ترقية تتطلب أدلة مُوثقة وموافقة المؤسس. القيم التقديرية ليست قيمًا مُتحقَّقة.
