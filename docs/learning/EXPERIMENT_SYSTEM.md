---
title: Experiment System
owner: PM
status: active
last_review: 2026-05-23
---

# Experiment System — نظام التجارب

## Purpose

Convert hunches into evidence. Every Dealix experiment follows the same shape: hypothesis, test, measure, decide. No experiment runs without an intake row and a stop date.

## Definitions

- **Hypothesis** — a one-sentence claim with a measurable outcome.
- **Test** — the minimal action that exposes the hypothesis to reality. No bigger than two weeks.
- **Measure** — the named metric and the threshold that decides yes/no.
- **Decide** — keep, kill, or extend. Written, dated, owned.

## Intake template

```yaml
experiment_id: EXP-YYYY-NNN
hypothesis: "If we X, then Y will move by Z."
owner: name
sector: optional
start_date: YYYY-MM-DD
stop_date: YYYY-MM-DD
metric_primary: name and target
metric_guardrail: name and threshold
sample_size_min: n
cost_ceiling_sar: amount
decision_rule: "keep if metric >= target and guardrail not breached"
linked_signals: [router intake ids]
```

## Operations

1. Intake row filed in `dealix-ops-private/learning/experiments.csv`.
2. PM confirms the test does not violate any non-negotiable (no scraping, no cold WA, no LinkedIn automation, no bulk outreach, no PII exposure).
3. Test runs. Raw data is logged, not paraphrased.
4. On stop date, decision is written with evidence link. No silent extensions.
5. Outcome enters the [LEARNING_ROUTER.md](./LEARNING_ROUTER.md) for promotion.

## Guardrails

- Experiments touching client communication require approval per [docs/05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).
- Experiments touching AI prompts or models follow [docs/ai_management/AI_CHANGE_MANAGEMENT.md](../ai_management/AI_CHANGE_MANAGEMENT.md).
- No experiment promises a sales outcome. Outputs are framed as evidenced opportunities.

## Evidence

- Experiment file with raw data, decision, and linked artifacts.
- Cross-link to [COMPANY_MEMORY.md](./COMPANY_MEMORY.md) when an experiment produces a decision, kill, or double.

## Owner & cadence

- PM owns the intake and the stop discipline.
- Founder reviews the experiments list at the Sunday review.

## AR — ملخّص

نظام التجارب يحوّل الحدس إلى دليل: فرضية، اختبار، قياس، قرار. كل تجربة لها بطاقة دخول، تاريخ توقّف، مقياس أساسي، وحارس. لا تجربة تمسّ تواصل عميل بلا موافقة، ولا تجربة تعد بمبيعات. القيمة التقديرية ليست قيمة مُتحقَّقة.
