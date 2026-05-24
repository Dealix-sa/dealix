# Nurture Machine | آلة التغذية طويلة الأمد

## Purpose | الغرض
Maintain long-cycle relationships with C-bucket accounts, soft-no's, and "not now"
buyers without spamming them. Generate value-led drip drafts on a slow cadence,
keyed to refreshed signals.

Drafts only. No automated sends.

## Inputs | المدخلات
- C-bucket accounts
- Soft-no accounts from Reply Router (wrong time, wrong person)
- New trigger events on previously-rejected accounts
- New proof artifacts that match the account's sector

## Outputs | المخرجات
- `nurture.queue`: queue_id, account_id, channel, draft_text, cadence_slot,
  reason_for_inclusion, state
- Monthly nurture digest for founder

## Cadence | التواتر
- Default: 1 touch every 60-90 days per account
- Accelerated: if a high-confidence new trigger appears, move to Outbound queue
- Decelerated: after 3 unanswered nurture touches, pause for 180 days

## Content types | أنواع المحتوى
- Sector insight bullet (citing public sources)
- Relevant Dealix proof artifact (sample, case study, anonymized peer outcome)
- "Thinking of you because" referencing a new trigger
- Polite check-in with one open question

## Pause conditions | حالات الإيقاف
- Hard no in history → pause 180 days minimum
- Trust risk flag raised → permanent pause
- Founder manual exclusion
- Account closed-lost less than 90 days ago

## Data source | مصدر البيانات
`nurture.queue`, `intelligence.accounts`, `reply.events`, `proof.artifacts`.

## Approval class | فئة الموافقة
- A1: drafting, queueing, cadence scheduling
- A2: per-touch approval
- A3: nurture touches to regulated/government accounts

## Trust gate | بوابة الثقة
- Cadence cap enforced (no more than 1 touch per 60-90 days)
- Reason-for-inclusion required for every queued draft
- No price/contract language
- Policy snapshot + audit row per draft

## Owner | المالك
Founder approves each touch before send.

## Worker name
`growth.nurture_machine`

## KPI | المؤشرات
- # active nurture accounts
- Reactivation rate (nurture → outbound move) per quarter
- Reactivation → proposal rate
- % accounts that opt-out (target very low)

## Failure mode | حالات الفشل
- Account accidentally entered nurture while still in active outbound
- Cadence collision across multiple drafts in the same week
- Stale proof artifact attached to a fresh touch

## Recovery path | مسار الاسترداد
- Mutex: an account is in exactly one machine at a time
- Cadence collision detector blocks second draft within 60 days
- Proof artifact freshness check at draft time
