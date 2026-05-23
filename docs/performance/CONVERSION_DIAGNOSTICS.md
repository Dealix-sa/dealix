# Conversion Diagnostics | تشخيصات التحويل

## Purpose | الغرض
When the Revenue KPI Tree flags a node below target, Conversion Diagnostics drills
into *why* the conversion is failing. It produces a structured diagnosis and a
ranked list of candidate fixes for the Experiment Backlog.

Diagnostics observes; it does not act.

## Inputs | المدخلات
- Revenue KPI Tree node + history
- Per-stage telemetry (drafts, replies, meetings, proposals, payments)
- Sample of records at the failing stage (anonymized)
- Persona / segment / sector context
- Prior diagnostics for the same node (avoid repeating the same diagnosis)

## Outputs | المخرجات
- `performance.diagnostics`: id, node_id, period, candidate_root_causes,
  evidence_snippets, ranked_fixes, founder_review_state
- Per-diagnosis memo (1-2 pages)
- Handoff to Experiment Backlog

## Diagnostic patterns | أنماط التشخيص
1. **Volume bottleneck** — not enough input arriving at this stage
2. **Quality bottleneck** — input arrives but does not match downstream needs
3. **Speed bottleneck** — input processed too slowly, decays
4. **Approval bottleneck** — founder approval queue is the choke point
5. **Channel bottleneck** — specific channel under-performs vs others
6. **Persona/segment bottleneck** — specific segment under-performs
7. **Proof bottleneck** — proof artifact mismatch with stage
8. **Trust bottleneck** — gates blocking volume legitimately

## Diagnostic method | منهجية التشخيص
1. Compare current period vs trailing baseline
2. Decompose by channel, segment, persona, sector
3. Identify the dimension with largest variance
4. Pull representative anonymized examples
5. Pattern-match against known diagnostic patterns
6. Rank candidate root causes by evidence strength
7. Propose 1-3 fixes per top root cause

## Anti-patterns | ما يجب تجنبه
- Single-example diagnosis (need ≥ 5 examples per pattern)
- Cause-effect inference from correlation alone
- Diagnosing across periods with major external changes (season, holiday)
- Recommending fixes that violate non-negotiables

## Data source | مصدر البيانات
`performance.diagnostics`, `performance.kpi_tree`, machine telemetry,
anonymized stage samples.

## Approval class | فئة الموافقة
- A1: diagnostic computation, sample pulling, pattern matching
- A2: any diagnostic memo shared externally
- A3: diagnoses involving regulated client samples

## Trust gate | بوابة الثقة
- Samples anonymized before storage
- No identifying client data in published memos
- All recommended fixes lint-checked against non-negotiables
- Policy snapshot + audit row per diagnosis

## Owner | المالك
Founder reviews each diagnosis and decides which fixes go to experiments.

## Worker name
`performance.diagnostics`

## KPI | المؤشرات
- Time: KPI flag → diagnosis completed (target ≤ 72h)
- % diagnoses that produced an approved experiment
- % experiments that confirmed the diagnosis
- # repeat diagnoses on same node (should fall)

## Failure mode | حالات الفشل
- Diagnosis on too small a sample → spurious pattern
- Diagnosis ignores upstream cause (real bottleneck is one stage earlier)
- Recommendations violate non-negotiables silently

## Recovery path | مسار الاسترداد
- Minimum sample size enforced
- Upstream-cause check: re-run diagnosis on prior stage when no fix lands
- Pre-output linter against non-negotiables
