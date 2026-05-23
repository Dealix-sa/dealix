# Performance Improvement OS | نظام تحسين الأداء

## Purpose | الغرض
A continuous-improvement layer over every Dealix machine. Performance Improvement
OS reads the KPI tree, finds the weakest link, diagnoses it, proposes experiments,
runs them under controls, and feeds learnings back into the playbooks.

It improves the *factory*; it does not sell, deliver, or transact.

## Inputs | المدخلات
- Revenue KPI Tree state
- Conversion Diagnostics findings
- Experiment Backlog status
- Learning Loop archive
- Telemetry from every machine
- Founder strategic priorities (where to focus this month)

## Outputs | المخرجات
- Weekly bottleneck report
- Per-bottleneck experiment proposals (drafted, founder approves)
- Per-experiment results memo
- Updated playbook patches across machines
- Quarterly performance retrospective

## Improvement loop | حلقة التحسين
1. **Measure** — pull latest KPI tree numbers
2. **Diagnose** — Conversion Diagnostics identifies weakest stage
3. **Hypothesize** — propose root cause + 1-3 candidate fixes
4. **Experiment** — design controlled test with success criterion
5. **Approve** — founder approves the experiment plan
6. **Run** — execute experiment with audit trail
7. **Learn** — record result in Learning Loop
8. **Embed** — if successful, patch the relevant playbook + worker

## Experiment design rules | قواعد تصميم التجربة
- Each experiment has: hypothesis, success metric, runtime, sample size,
  rollback trigger
- Experiments that change external-facing behavior need A2 per send
- Experiments that touch pricing, contracts, or proof publication need A3
- Negative results are first-class outputs and must be archived

## Bottleneck priority | أولويات الاختناقات
- Stage with lowest conversion rate relative to benchmark gets attention first
- Stage with largest absolute drop in volume gets second
- Stage with highest cost per outcome gets third
- Founder strategic preference can override

## Data source | مصدر البيانات
`performance.kpi_tree`, `performance.diagnostics`, `performance.experiments`,
`performance.learning_loop`.

## Approval class | فئة الموافقة
- A1: measurement, diagnosis, internal experiment design
- A2: experiments that change external-facing behavior
- A3: experiments touching pricing, contract terms, regulated workflows

## Trust gate | بوابة الثقة
- No experiment runs without recorded hypothesis + rollback trigger
- No external-facing experiment without per-send approval
- All results (positive AND negative) archived in Learning Loop
- Policy snapshot + audit row per experiment lifecycle

## Owner | المالك
Founder approves the weekly improvement focus and every external-facing experiment.

## Worker name
`performance.improvement_os`

## KPI | المؤشرات
- # bottlenecks identified per week
- # experiments approved per week
- Experiment success rate (% reaching success metric)
- Median time: hypothesis → embedded improvement
- KPI tree delta over rolling 90d (this is the meta-metric)

## Failure mode | حالات الفشل
- Many experiments running simultaneously → noise
- Negative results not archived → repeated mistakes
- Improvement embedded into one playbook but related playbooks not updated

## Recovery path | مسار الاسترداد
- Concurrency cap: max 3 active experiments at a time
- Archive enforcement: experiment cannot close without result memo
- Cross-playbook propagation checklist when an improvement is embedded
