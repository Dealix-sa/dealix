# Experiment Backlog | قائمة التجارب

## Purpose | الغرض
The queue of proposed experiments to improve Dealix's revenue performance. Each
experiment is a hypothesis with a clear success metric, runtime, and rollback
trigger. Experiments are prioritized; founder approves the top of the queue.

## Inputs | المدخلات
- Conversion Diagnostics recommended fixes
- Performance Improvement OS bottleneck reports
- Founder strategic priorities
- Open experiment capacity (max 3 concurrent)

## Outputs | المخرجات
- `performance.experiments`: id, hypothesis, success_metric, runtime,
  sample_size, rollback_trigger, owner, state, results
- Prioritized experiment list
- Per-experiment kickoff brief

## Experiment record fields | حقول التجربة
- Hypothesis (one sentence)
- Affected stage / node in KPI tree
- Success metric (specific, measurable)
- Minimum runtime (days) + minimum sample size
- Rollback trigger (e.g., "if conversion drops > 15%, rollback")
- Approval class (A2 for external-facing, A3 for sensitive)
- Owner (worker + founder co-owner)
- State: proposed → approved → running → analyzing → closed (success/failure)

## Prioritization | الأولوية
Score each experiment 0-100:
- Expected lift × confidence (40%)
- Implementation effort (inverse) (20%)
- Strategic relevance (founder priority weight) (20%)
- Reversibility (10%)
- Learning value (10%)

Highest score floats to the top.

## Concurrency rules | قواعد التشغيل المتوازي
- Max 3 active experiments at a time
- No two active experiments touch the same KPI node simultaneously
- No two active experiments touch the same channel simultaneously
- Founder can force-pause any experiment

## Lifecycle | دورة الحياة
1. Proposed (from Diagnostics or founder)
2. Reviewed (worker validates fields, no missing rollback)
3. Approved by founder
4. Running (telemetry collected, no other changes to same node)
5. Analyzing (results computed)
6. Closed: success (embed into playbook) OR failure (archive learning) OR
   inconclusive (extend runtime or close)

## Data source | مصدر البيانات
`performance.experiments`, `performance.diagnostics`, `performance.kpi_tree`.

## Approval class | فئة الموافقة
- A1: backlog maintenance, scoring
- A2: experiments that change external-facing behavior
- A3: experiments touching pricing, contracts, proof, regulated workflows

## Trust gate | بوابة الثقة
- Every experiment has a rollback trigger before approval
- No experiment violates non-negotiables (no auto-send, no proof publish, etc.)
- All results archived (success and failure)
- Policy snapshot + audit row per state transition

## Owner | المالك
Founder approves each experiment. Worker runs and records.

## Worker name
`performance.experiment_backlog`

## KPI | المؤشرات
- Backlog depth (target 10-30 proposed)
- Median time: proposed → approved (target ≤ 5 business days)
- Median time: approved → closed
- Experiment success rate
- # experiments embedded into playbooks per quarter

## Failure mode | حالات الفشل
- Experiment runs past runtime without analysis
- Rollback trigger fires but rollback never executes
- Successful experiment never gets embedded into the playbook

## Recovery path | مسار الاسترداد
- Watchdog timer per experiment; auto-pause if past runtime
- Rollback execution is gated and audited; SLA for completion
- Embedment checklist; experiment cannot close "success" without playbook patch
