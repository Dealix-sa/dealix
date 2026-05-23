# Delivery QA OS | نظام جودة التسليم

## Purpose | الغرض
Quality-gate every deliverable that leaves Dealix to a paying client. Delivery QA
OS sits between the working drafts of an engagement and the founder's final sign-off.

QA is internal — but its outputs (sign-offs, regressions, defect notes) determine
whether anything reaches the client.

## Inputs | المدخلات
- Active engagements (`delivery.engagements`)
- Per-engagement deliverable checklist
- Standard quality bar per service line
- Client-stated success criteria from proposal
- Prior delivery telemetry (what tends to fail in this service line)

## Outputs | المخرجات
- `delivery.qa_reviews`: review_id, engagement_id, deliverable_id, checklist_state,
  pass/fail, defects, recommended_action, reviewer_id
- Defect log + recurrence patterns
- Per-engagement quality scorecard

## Checklist domains | محاور الفحص
1. **Correctness** — does the deliverable do what the proposal said?
2. **Completeness** — are all promised components present?
3. **Trust** — no client PII leaks, no competitor info leaks
4. **Compliance** — PDPL, contract terms, no out-of-scope claims
5. **Polish** — naming, formatting, branding, file integrity
6. **Reproducibility** — can another team member rebuild this if needed?
7. **Evidence** — links to source signals/data points where relevant

## Pass/fail rules | قواعد القبول
- Any "fail" in Trust or Compliance → hard block until fixed
- Any "fail" in Correctness or Completeness → block, sent back to delivery team
- Polish fail → fix-then-pass (no escalation)
- Reproducibility fail → coach the operator, deliverable can still ship if low-risk

## Sign-off chain | سلسلة الاعتماد
- QA review by worker → flagged defects → fix → re-review → pass
- Founder gives final sign-off on every client deliverable

## Data source | مصدر البيانات
`delivery.engagements`, `delivery.deliverables`, `delivery.qa_reviews`.

## Approval class | فئة الموافقة
- A1: QA review run, defect logging
- A2: founder sign-off on every deliverable before it reaches client
- A3: deliverables for regulated/government clients

## Trust gate | بوابة الثقة
- No cross-client data contamination
- No out-of-scope claims slipped in
- All evidence cited
- Policy snapshot + audit row per QA review and per sign-off

## Owner | المالك
Founder signs off on every deliverable.

## Worker name
`delivery.qa_os`

## KPI | المؤشرات
- First-pass QA pass rate (target ≥ 70%)
- Median time: deliverable ready → QA passed (target ≤ 24h)
- Defect recurrence rate (should fall over time)
- Founder rejection rate post-QA (should be < 10%)

## Failure mode | حالات الفشل
- QA passes a deliverable with hidden defect
- Founder bottleneck delays sign-off → client SLA missed
- Checklist drift (stops catching real-world defects)

## Recovery path | مسار الاسترداد
- Post-delivery defect feedback loops back into checklist refresh
- SLA breach dashboard for founder
- Quarterly checklist review against last 90 days of escaped defects
