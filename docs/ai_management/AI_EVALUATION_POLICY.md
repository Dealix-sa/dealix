---
title: AI Evaluation Policy
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# AI Evaluation Policy — سياسة تقييم أنظمة الذكاء الاصطناعي

## Purpose

Define what gets evaluated, how often, what pass means, and when a system is rolled back. Maps to NIST AI RMF "Measure" function. Evaluation is not a one-time gate; it is a cadence.

## What gets evaluated

| Surface | Evaluations |
|---|---|
| Prompts | output quality on a fixed eval set, regression vs baseline |
| Models | same eval set re-run on version change |
| Agents | task success rate, refusal correctness, oversight respect |
| RAG / retrieval | grounding accuracy, citation correctness, redaction respect |
| Claim-safety | percentage of outputs flagged correctly by the claim-safety filter |

## Pass/fail criteria

- Each eval set has a baseline score and a tolerance band.
- Pass = at or above baseline minus tolerance.
- Fail = below tolerance, or any unsafe-output regression.
- A single unsafe-output regression triggers rollback regardless of aggregate score.

## Cadence by risk tier

| Tier | Cadence | Trigger evals |
|---|---|---|
| T1 | quarterly | major prompt change |
| T2 | monthly | any prompt or model change |
| T3 | weekly | any change; pre-release gate |

## Eval set composition

- Held-out from training and not used in prompt iteration.
- Mix of clean cases, adversarial cases (prompt-injection attempts), edge cases, and Arabic/English parallels where applicable.
- Reviewed quarterly to prevent eval rot.

## Rollback

1. On fail, the prior known-good version is restored within 24 hours.
2. Failure is logged in `dealix-ops-private/ai_management/eval_results.csv`.
3. Root cause is added to [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md) if novel.
4. A new candidate is prepared; the cadence does not pause.

## Operations

1. Eval runs are scheduled and named, not ad hoc.
2. Results are committed; passing alone is not enough — the diff vs baseline is reviewed.
3. Sampling for T1 systems: 10% of runs are human-reviewed.

## Non-negotiables

- No system goes to production without a passing eval on a current-quarter eval set.
- No eval set is edited after a failing run to make it pass.
- No model change ships without a re-run of the eval set per [AI_CHANGE_MANAGEMENT.md](./AI_CHANGE_MANAGEMENT.md).

## Evidence

- Eval results file with timestamps and reviewer.
- Cross-link from [docs/06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md) when applicable.

## Owner & cadence

- AI Governance Lead owns the policy.
- Cadence per tier above; reviewed quarterly.

## AR — ملخّص

سياسة التقييم تحدّد ماذا يُقيَّم (موجّهات، نماذج، وكلاء، استرجاع، أمان الادّعاء)، ومعايير النجاح، وإيقاع التقييم حسب مستوى الخطر، وآلية التراجع خلال 24 ساعة عند الفشل. لا إنتاج بلا نجاح حالي، ولا تعديل لمجموعة التقييم بعد الفشل. القيمة التقديرية ليست قيمة مُتحقَّقة.
