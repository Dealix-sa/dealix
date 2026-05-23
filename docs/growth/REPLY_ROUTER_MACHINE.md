# Reply Router Machine | آلة توجيه الردود

## Purpose | الغرض
Triage every inbound reply (LinkedIn DM, email, form response, WhatsApp, partner
intro) and route it to the right next action. Reply Router *never auto-replies*.
It only classifies, suggests a draft response, and surfaces it to the founder.

## Inputs | المدخلات
- Inbound reply payloads from each channel
- Original outbound context (which draft, which persona, which trigger)
- Buyer persona profile
- Account scoring + ICP context
- Calendar availability (for meeting suggestions)

## Outputs | المخرجات
- `reply.events`: event_id, channel, account_id, original_send_id,
  reply_text, intent, sentiment, suggested_action, suggested_draft_id, state
- Founder reply dashboard
- Routed handoffs (Sample Factory, Proposal Factory, Nurture, Close-Lost)

## Intent classification | تصنيف النية
- **Interested — wants meeting**
- **Interested — wants info first**
- **Wants sample**
- **Wants proposal**
- **Soft no — wrong time**
- **Soft no — wrong person**
- **Hard no — not interested**
- **Out of office**
- **Spam / irrelevant**
- **Ambiguous**

## Routing rules | قواعد التوجيه
- Wants meeting → draft calendar suggestion (founder approves)
- Wants info → draft info reply with proof artifact attached (founder approves)
- Wants sample → handoff to Sample Factory
- Wants proposal → handoff to Proposal Factory
- Soft no (wrong time) → schedule for Nurture Machine 60-90 days
- Soft no (wrong person) → draft polite ask for referral
- Hard no → close-lost with reason, 180-day cooldown
- OOO → wait, reschedule follow-up after OOO end-date
- Spam → drop, no action
- Ambiguous → founder review

## Approval class | فئة الموافقة
- A1: classification, routing, draft generation
- A2: per-reply approval before any external response
- A3: any reply to a regulated/government recipient

## Trust gate | بوابة الثقة
- Auto-reply is forbidden
- Suggested draft must be approved by founder; nothing is sent automatically
- PII in reply minimized before storage
- Per-event policy snapshot + audit row

## Data source | مصدر البيانات
`reply.events`, channel inbound webhooks, `outbound.sends`, `personas.profiles`.

## Owner | المالك
Founder owns every outbound reply.

## Worker name
`growth.reply_router`

## KPI | المؤشرات
- Time-to-classification (median, target < 5 min)
- Time-to-founder-action (median, target < 4 business hours)
- Intent classification accuracy (founder corrections / total)
- % replies that reach handoff stage (sample, proposal)

## Failure mode | حالات الفشل
- Misclassification routes a hard-no into Sample Factory
- Auto-reply triggered accidentally (must be impossible)
- Spam classification drops a real inbound

## Recovery path | مسار الاسترداد
- Founder can override classification with one click; correction trains rules
- Hard architectural guarantee: no send path exists in Reply Router code
- All "spam" drops logged with full text so founder can audit weekly
