# Follow-up Machine | آلة المتابعة

## Purpose | الغرض
Generate multi-touch follow-up drafts for conversations that did not get a reply
on the first touch. Maintain cadence discipline so accounts are nurtured, not
spammed.

Follow-ups are drafts. Founder approves each send.

## Inputs | المدخلات
- Original outbound send (across LinkedIn, email, form)
- Last contact timestamp
- Reply state (none, soft no, ghost)
- Persona preferences (channel + tone)
- Trigger refresh signals

## Outputs | المخرجات
- `followup.queue`: queue_id, original_send_id, channel, touch_number (2..5),
  draft_text, scheduled_for, state
- Per-account cadence map (history of touches)

## Cadence rules | قواعد التواتر
- Touch 1: day 0 (original send)
- Touch 2: day 4 — soft bump, same channel
- Touch 3: day 10 — value-add bump, new angle or proof artifact
- Touch 4: day 21 — channel switch (e.g., LinkedIn → email)
- Touch 5: day 45 — break-up message, polite close
- Max 5 touches total; account moves to Nurture Machine after

## Cadence pauses | إيقاف التواتر
- Pause immediately when a reply lands (Reply Router takes over)
- Pause if account is flagged trust-risk
- Pause if founder marks "do not follow up"

## Personalization rules | قواعد التخصيص
- Each touch references *new* signal where possible (new trigger, new proof)
- Never identical to a previous touch
- Tone softens over time, never pushy
- No price/contract/commitment language at any touch

## Data source | مصدر البيانات
`followup.queue`, `outbound.sends`, `reply.state`, `intelligence.trigger_events`.

## Approval class | فئة الموافقة
- A1: drafting follow-ups, scheduling
- A2: per-touch approval before send
- A3: any touch to a regulated/government recipient

## Trust gate | بوابة الثقة
- No more than 5 touches ever
- Reply state must be `none` or `ghost` before next touch
- Each touch carries its own policy snapshot + audit row
- No language implying a commitment from buyer ("as agreed", etc.)

## Owner | المالك
Founder approves each follow-up before send.

## Worker name
`growth.followup_machine`

## KPI | المؤشرات
- Reply rate per touch number
- Median touches to first reply
- # accounts moved to Nurture vs # accounts closed-lost
- Approval rate (drafts approved / drafts produced)

## Failure mode | حالات الفشل
- Cadence runs after a reply landed (race condition)
- Same content used in touch 2 and touch 3
- Touch 5 break-up sent to an active conversation

## Recovery path | مسار الاسترداد
- Reply-state recheck immediately before send; abort if state changed
- Content similarity check; > 70% similarity blocks the draft
- Final state check before any "break-up" send
