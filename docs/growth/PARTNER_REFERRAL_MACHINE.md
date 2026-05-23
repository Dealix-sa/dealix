# Partner Referral Machine | آلة الإحالات عبر الشركاء

## Purpose | الغرض
Turn the Dealix partner network (agencies, consultancies, integrators, ecosystem
contacts) into a steady source of warm intros. Generate drafts for partner-facing
asks and drafts for the resulting intro emails — both queued for founder approval.

## Inputs | المدخلات
- Active partner registry (`partners.network`)
- A-bucket and high-trust B-bucket accounts that match partner reach
- Partner relationship strength score
- Last-touch cadence per partner
- Previous referral outcomes

## Outputs | المخرجات
- `partner.referral_queue`: queue_id, partner_id, target_account_id,
  ask_draft, intro_template, state
- Partner CRM update suggestions
- Quarterly partner-performance digest

## Ask types | أنواع الطلبات
- **Direct intro** — partner forwards a 2-line intro to target account
- **Warm name-drop** — partner mentions Dealix in next conversation
- **Co-pitch** — partner and Dealix jointly approach a target
- **Referral fee opt-in** — only if a formal partner agreement exists

## Cadence | التواتر
- Max 1 referral ask per partner per 30 days
- High-strength partners: monthly check-in draft
- Mid-strength: quarterly value-add update draft
- Low-strength: warm-up cadence (build trust before asking)

## Trust rules | قواعد الثقة
- Never share a partner's contact list publicly
- Never imply a partner endorses something they haven't approved
- Referral fees only with signed partner agreement; no implied promises
- Pricing/commercial terms in partner asks must reference written agreement only

## Data source | مصدر البيانات
`partners.network`, `partner.referral_queue`, `crm.accounts`.

## Approval class | فئة الموافقة
- A1: drafting asks, scheduling cadence
- A2: per-ask approval before any partner contact
- A3: asks involving regulated/government targets or financial terms

## Trust gate | بوابة الثقة
- Partner relationship status verified (active, not dormant) at draft time
- Cadence cap enforced
- Referral-fee mention only if signed agreement present
- Policy snapshot + audit row per ask

## Owner | المالك
Founder owns every partner ask.

## Worker name
`growth.partner_referral_machine`

## KPI | المؤشرات
- Active referring partners per quarter
- Referrals received per quarter
- Referral → proposal rate (target higher than cold outbound)
- Referral → paid rate

## Failure mode | حالات الفشل
- Asking the same partner too often → relationship strain
- Asking for an intro to an account already in another partner's pipeline
- Partner agreement lapsed but referral-fee language used

## Recovery path | مسار الاسترداد
- Per-partner cadence cap enforced
- Account ↔ partner overlap detector blocks conflicting asks
- Partner agreement status checked at draft time; lapsed → strip fee language
