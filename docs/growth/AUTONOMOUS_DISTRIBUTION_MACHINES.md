# Autonomous Distribution Machines | آلات التوزيع الذاتية

## Purpose | الغرض
Coordinate every autonomous draft-producing sub-machine into one coherent flow.
"Autonomous" here means autonomous *drafting and queueing* — never autonomous
sending. The founder is always the last gate before any external action.

## Inputs | المدخلات
- Distribution War Machine plan
- Account, persona, trigger, sector context
- Reply router state
- Founder availability + approval queue depth

## Outputs | المخرجات
- Coordinated draft batches across LinkedIn / Email / Form / Follow-up
- Per-machine telemetry: drafts produced, approval rate, conversion rate
- Founder daily distribution dashboard

## Sub-machine inventory | فهرس الآلات الفرعية
- Outbound Draft Machine — top-of-funnel cold draft producer
- LinkedIn Queue Machine — LinkedIn-specific channel adapter
- Email Draft Machine — email-specific channel adapter
- Contact Form Queue Machine — website contact form adapter
- Follow-up Machine — multi-touch cadence drafts
- Reply Router Machine — inbound triage
- Nurture Machine — long-cycle drip drafts
- Partner Referral Machine — partner-led intro drafts
- ABM Strategic Account Machine — high-touch named-account drafts
- Proof-to-Demand Machine — proof-event triggered drafts

## Coordination rules | قواعد التنسيق
- One account, one channel per 72-hour window
- Reply state pauses outbound machines for that account
- Approval queue capacity dictates per-machine daily draft caps
- ABM always takes priority on A-bucket accounts
- Proof-to-Demand has 24-hour fast-lane priority after proof event

## Failure isolation | عزل الأعطال
Each sub-machine fails independently; one failure does not stop others. Failed
sub-machine surfaces a status on founder dashboard with recovery action.

## Data source | مصدر البيانات
`distribution.machines`, per-machine queues, `policy.snapshots`, `audit.events`.

## Approval class | فئة الموافقة
- A1: orchestration, scheduling, dashboard
- A2: per-draft approval (handled by each sub-machine)
- A3: ABM + regulated/government routing

## Trust gate | بوابة الثقة
- No machine can bypass the others — coordination is centrally enforced
- No machine can send externally; sending is a separate, approval-gated action
- Per-batch policy snapshot + audit row

## Owner | المالك
Founder reviews coordinated batch daily.

## Worker name
`growth.autonomous_distribution_coordinator`

## KPI | المؤشرات
- # drafts produced per machine per day
- Per-machine approval rate
- End-to-end draft-to-meeting conversion
- Founder approval-queue depth (target < 60 at end of day)

## Failure mode | حالات الفشل
- Coordinator gets stuck waiting on a slow sub-machine
- Conflicting drafts queued for the same account from two sub-machines
- Stale state in reply router lets outbound resume too early

## Recovery path | مسار الاسترداد
- Watchdog timer: sub-machine that misses heartbeat is bypassed
- Conflict resolver picks highest-priority machine; others queue is paused
  for that account
- Reply router state synced every 5 minutes; mismatches trigger founder alert
