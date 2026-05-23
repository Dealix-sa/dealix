# Distribution War Machine | آلة الحرب التوزيعية

## Purpose | الغرض
The Distribution War Machine is the orchestrator over every distribution sub-machine
(Outbound, LinkedIn, Email, Contact Form, Follow-up, Reply Router, Nurture, Partner
Referral, ABM, Proof-to-Demand). It decides daily *who* gets reached, on *which*
channel, with *what* draft — then queues everything for founder approval.

Nothing leaves the queue automatically. Distribution = drafting + queueing, not
sending.

## Inputs | المدخلات
- Account Scoring Model (A/B/C buckets)
- Trigger Event System (urgency, freshness)
- ICP segmentation + Buyer Persona
- Sector Ranking (weekly heat)
- Channel capacity budgets (LinkedIn DMs/day, emails/day, forms/day)
- Reply Router state (open conversations not yet closed)
- Founder calendar capacity for approvals

## Outputs | المخرجات
- Daily distribution plan (target accounts × channels × draft pack)
- Drafts queued in each sub-machine
- Capacity heatmap (where the founder bottleneck is)
- Audit log of every draft generated

## Sub-machines orchestrated | الآلات الفرعية
1. Autonomous Distribution Machines (meta-coordinator)
2. Outbound Draft Machine
3. LinkedIn Queue Machine
4. Email Draft Machine
5. Contact Form Queue Machine
6. Follow-up Machine
7. Reply Router Machine
8. Nurture Machine
9. Partner Referral Machine
10. ABM Strategic Account Machine
11. Proof-to-Demand Machine

## Decision logic | منطق القرار
- A-bucket accounts → ABM machine first, then LinkedIn personal touch
- B-bucket accounts → Outbound (LinkedIn / Email / Form) with persona-tagged draft
- C-bucket accounts → Nurture machine
- Open replies → Reply Router (founder must respond, no auto-reply)
- Stale conversations → Follow-up Machine
- Proof-published events → Proof-to-Demand Machine

## Daily capacity budget | الميزانية اليومية
- LinkedIn DMs queued: up to 30 drafts/day
- Email drafts queued: up to 50/day
- Contact form drafts queued: up to 20/day
- Follow-ups queued: up to 40/day
- ABM touchpoints queued: up to 10/day

(Numbers are budgets, not sends. Founder approves a subset.)

## Data source | مصدر البيانات
`distribution.plans`, `distribution.drafts`, `intelligence.accounts`,
`intelligence.trigger_events`, `personas.profiles`.

## Approval class | فئة الموافقة
- A1: drafting, queueing, capacity allocation, internal dashboards
- A2: any draft sent externally (per-draft approval)
- A3: ABM touchpoint to regulated / government accounts

## Trust gate | بوابة الثقة
- Every draft carries persona tag + evidence row
- No guaranteed revenue language
- No pricing / contract / payment commitments
- No competitor naming without battle-card approval
- Policy snapshot + audit row per draft

## Owner | المالك
Founder is the final approver for every external send.

## Worker name
`growth.distribution_war_machine`

## KPI | المؤشرات
- Drafts generated per day (capacity utilization)
- Drafts approved per day (founder throughput)
- Approved-draft → reply conversion rate (rolling 14d)
- Reply → meeting conversion rate
- # accounts contacted per A/B/C bucket

## Failure mode | حالات الفشل
- Over-queuing: more drafts than founder can review
- Channel collision: same account hit on 3 channels in same day
- Stale persona tag attached to a draft

## Recovery path | مسار الاسترداد
- Auto-throttle when approval queue > 100 drafts
- Channel collision detector: max 1 channel per account per 72 hours
- Persona freshness check at draft time; if stale > 30d, re-tag before queueing
