# Ultimate Delivery OS | نظام التسليم الشامل

## Purpose | الغرض
Run every paid engagement end-to-end: onboarding, scope tracking, deliverable
production, quality gating, client communication, change requests, milestones,
closeout, and proof-event registration.

Ultimate Delivery OS is the operational layer where Dealix earns the renewal and
the referral. Every external client touch is drafted → approved → sent.

## Inputs | المدخلات
- Signed proposal + accepted invoice (from Revenue Factory)
- Engagement plan (scope, milestones, success criteria)
- Client point-of-contact roster
- Delivery capacity calendar
- Standard operating procedures per service line

## Outputs | المخرجات
- `delivery.engagements`: id, client_id, scope, milestones, state, health_score
- Per-engagement deliverable artifacts (each QA-gated)
- Client weekly status update drafts (founder approves)
- Closeout report + proof-event handoff to Proof Approval OS
- Renewal / expansion handoff to Retention & Referral OS

## Engagement lifecycle | دورة حياة الارتباط
1. **Kickoff** — onboarding form, expectations set, RACI confirmed
2. **Discovery** — initial signal collection, alignment workshop
3. **Build** — deliverable production with QA gating
4. **Review** — client review on each milestone, structured feedback capture
5. **Closeout** — final deliverables, retrospective, proof-event proposal
6. **Renewal/Referral** — handoff to Retention & Referral OS

## Health scoring | تقييم صحة الارتباط
Per engagement, daily compute:
- Schedule adherence
- Quality (QA pass rate)
- Client sentiment (from communication transcripts, anonymized)
- Scope-creep magnitude
- Change-request frequency

Health = green / yellow / red. Red triggers founder alert + recovery plan.

## Change requests | طلبات التغيير
- Captured formally with `scope.change_requests` row
- Impact estimate (time, cost, risk) drafted
- Founder approves; client signs the change
- Never apply scope changes without written approval

## Client communication | التواصل مع العميل
- Weekly status update drafted by worker
- Founder reviews and sends
- Ad-hoc updates also drafted → approved → sent
- No automated client emails ever

## Data source | مصدر البيانات
`delivery.engagements`, `delivery.deliverables`, `delivery.qa_reviews`,
`scope.change_requests`, `delivery.communications`.

## Approval class | فئة الموافقة
- A1: internal engagement tracking, health computation
- A2: every client-facing send (status update, deliverable, change-request response)
- A3: regulated/government clients; any decision that re-scopes the engagement

## Trust gate | بوابة الثقة
- No client deliverable leaves without Delivery QA OS pass + founder sign-off
- No scope change without written client approval
- No proof event registered without explicit client consent
- Policy snapshot + audit row per state transition

## Owner | المالك
Founder owns engagement health and final client sign-off on every artifact.

## Worker name
`delivery.ultimate_os`

## KPI | المؤشرات
- # active engagements
- Engagement health distribution (% green / yellow / red)
- On-time milestone delivery rate
- Client satisfaction (post-engagement survey)
- Renewal rate, referral generation rate

## Failure mode | حالات الفشل
- Engagement drifts to red without alert
- Scope creep accepted informally over chat → not captured as change request
- Closeout skipped → proof event never registered

## Recovery path | مسار الاسترداد
- Daily health computation surfaces yellow/red on founder dashboard
- Scope-creep detector scans communications; flags possible informal changes
- Closeout checklist is gating — engagement cannot mark "complete" without it
