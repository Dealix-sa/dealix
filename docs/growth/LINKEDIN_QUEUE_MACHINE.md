# LinkedIn Queue Machine | آلة طابور لينكدإن

## Purpose | الغرض
Adapt outbound drafts to LinkedIn-specific format (connection request note + DM
follow-up), respect LinkedIn's platform limits, and queue everything for founder
manual send. Dealix never automates LinkedIn sends.

## Inputs | المدخلات
- Outbound Draft Machine output
- LinkedIn channel availability (account has a real LinkedIn presence)
- Buyer's public LinkedIn URL (verified, current)
- Founder's daily LinkedIn send budget

## Outputs | المخرجات
- `linkedin.queue`: queue_id, draft_id, buyer_url, connect_note (≤ 300 chars),
  followup_dm (≤ 1000 chars), state (queued/approved/sent/declined)
- Daily founder-friendly send list (top 20)
- Per-item audit row

## Format constraints | قيود التنسيق
- Connect note ≤ 300 chars (LinkedIn limit)
- Follow-up DM ≤ 1000 chars (readability)
- AR or EN inferred from buyer's profile language
- No external links in connect note (LinkedIn anti-spam)
- 1 link maximum in follow-up DM, only to a public Dealix page

## Manual-send protocol | بروتوكول الإرسال اليدوي
1. Founder opens daily list
2. Reviews each draft, edits inline if needed
3. Marks each as approved or declined
4. Founder manually pastes into LinkedIn (or uses a manual-paste flow)
5. State updated to sent + timestamp

## Anti-abuse rules | قواعد منع الإساءة
- Max 20 connect requests per day per founder profile
- Max 30 DMs per day per founder profile
- Max 1 touchpoint per buyer per 30 days unless they reply
- No automation tools; no third-party LinkedIn bots

## Data source | مصدر البيانات
`linkedin.queue`, `outbound.drafts`, `intelligence.buyers`.

## Approval class | فئة الموافقة
- A1: drafting, queueing, formatting
- A2: per-item approval before send
- A3: founder-level approval for any LinkedIn touch to a regulated/government buyer

## Trust gate | بوابة الثقة
- LinkedIn URL re-verified at queue time
- No automation; sends are manual only
- No commitments on price/contract/payment
- Policy snapshot + audit row per item

## Owner | المالك
Founder owns the daily LinkedIn send pass.

## Worker name
`growth.linkedin_queue`

## KPI | المؤشرات
- Daily queue length / approved / sent
- Connect acceptance rate
- Reply rate on follow-up DM
- Meeting booked per 100 sent DMs

## Failure mode | حالات الفشل
- Buyer's LinkedIn URL is dead or changed
- Daily budget overrun → LinkedIn flags account
- Same buyer queued twice within 30 days

## Recovery path | مسار الاسترداد
- Re-verify URL at queue time; if dead, drop and notify founder
- Hard cap enforced before queueing
- Dedup by buyer + 30-day window
