# Outbound Draft Machine | آلة مسودات التواصل الخارجي

## Purpose | الغرض
Generate channel-agnostic outbound first-touch drafts (subject line, opener, proof
bullet, CTA) for B-bucket accounts with a confirmed persona and at least one
trigger event. Drafts are queued — never sent.

## Inputs | المدخلات
- B-bucket account list from Account Scoring Model
- Buyer persona profile
- Most recent trigger event for the account
- Matched proof artifact (sample, case study, peer reference)
- Channel hint (LinkedIn / email / form) from Outreach Fit score

## Outputs | المخرجات
- `outbound.drafts`: draft_id, account_id, persona_id, trigger_id,
  proof_artifact_id, channel, subject, body, cta, language (AR/EN), confidence
- Founder approval queue entries
- Per-draft policy snapshot + audit row

## Draft structure | بنية المسودة
1. Personalized opener referencing the trigger (1 sentence)
2. Why-now: brief framing of the pain pattern (1-2 sentences)
3. Proof bullet: 1 line referencing a matched artifact (no guaranteed numbers)
4. Soft CTA: short ask (15-min call, share a one-pager, intro question)
5. Signature block: founder name, KSA office, no pricing, no contract terms

## Language | اللغة
Default AR for Saudi-HQ accounts; EN for foreign-HQ KSA branches. Persona override
can flip this.

## Data source | مصدر البيانات
`outbound.drafts`, `intelligence.accounts`, `personas.profiles`,
`proof.artifacts`, `intelligence.trigger_events`.

## Approval class | فئة الموافقة
- A1: drafting and queueing
- A2: founder approval per draft before any external send
- A3: drafts to regulated / government accounts

## Trust gate | بوابة الثقة
- No price, no contract, no payment terms in copy
- No guaranteed revenue language ("we will deliver X deals")
- Proof citations reference real artifact IDs
- Persona tag must be current (< 30 days)
- Trigger must be < 60 days old at draft time
- Policy snapshot + audit row per draft

## Owner | المالك
Founder approves every send.

## Worker name
`growth.outbound_drafter`

## KPI | المؤشرات
- Drafts per day produced
- Approval rate (drafts approved / drafts produced)
- Reply rate on approved drafts (rolling 14d)
- Meeting-booked rate per 100 approved drafts

## Failure mode | حالات الفشل
- Persona/trigger mismatch produces awkward opener
- Same proof artifact reused too often within the same segment
- Founder edits 90% of drafts → drafts are not yet good enough

## Recovery path | مسار الاسترداد
- Mismatch detector flags drafts where persona pain ≠ trigger type
- Per-segment proof rotation: max 3 reuses of an artifact in 30 days
- Founder edit-distance tracked; when > 70% over 1 week, draft model recalibrated
