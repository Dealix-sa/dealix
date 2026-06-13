# WhatsApp After Consent Library

> **Status:** Draft copy. **Only after explicit consent.** No cold WhatsApp.
> **Trust preflight:** mandatory + consent record required.

## The consent record (required before any message)

```json
{
  "consent_id": "consent_001",
  "account_id": "agency_x_riyadh",
  "channel": "whatsapp",
  "granted_by": "Sara",
  "granted_at_iso": "2024-12-01T10:00:00Z",
  "scope": "service discussion, audit follow-up",
  "expires_iso": "2024-12-31T23:59:59Z",
  "revocable": true,
  "source": "explicit_reply_to_email"
}
```

If the consent record is missing, **do not send**. Log the attempt as a preflight failure.

## When to use WhatsApp (allowed)

- The prospect replied to an email saying "send me WhatsApp".
- The prospect gave you their number in person at an event.
- The prospect is an existing client and the WhatsApp thread is part of the engagement scope.
- A referral intro happened over WhatsApp.

## When NOT to use WhatsApp (forbidden)

- Cold outreach. Never.
- Scraped numbers. Never.
- Purchased lists. Never.
- "I saw your number on the website" — without explicit ask, do not message.
- Group broadcasts. Never.
- Auto-replies from a bot. Never (we don't run a bot).

## The first WhatsApp message (after consent)

> مرحبا [الاسم]، أنا [الاسم] من Dealix. أرسلت إيميل قبل أيام وردّيت "ابعت لي واتساب". هذي الرسالة.
>
> نقطة سريعة: نعمل audit 5 أيام يكشف 10 فرص ضايعة في الواتساب والمتابعة. بدون ربط، بدون التزام.
>
> تحب نكمل هنا ولا تفضّل إيميل؟

## The follow-up sequence (only if they reply)

### Day 3 follow-up

> مرحبا [الاسم]،
>
> ما ردّيت. لو ما عندك وقت، لا ترد.
> لو تحب نموذج تقرير (PDF)، أرسل لك.
>
> — [الاسم]

### Day 7 follow-up

> آخر رسالة مني هنا. لو احتجتني، اعمل reply.
>
> — [الاسم]

After day 7 with no reply, **stop sending on WhatsApp**. Switch to email or LinkedIn if appropriate.

## The voice note (only if they used voice first)

If the prospect sent a voice note, you can reply with a voice note. The same rules apply.

If they never sent a voice note, do not send one. Voice notes in cold WhatsApp are intrusive.

## The image / screenshot (only if relevant)

If the audit found a specific leak that you can show without revealing client identity, a screenshot can help. Rules:

- No real client name or logo.
- No real PII.
- Add a watermark: "Sample data, anonymized".
- Send only after they reply, not as a first message.

## The thread management

| Situation | Action |
| --- | --- |
| They reply on WhatsApp but the conversation needs a long doc | move to email: "هل تحب نكمل على الإيميل؟ أحتاج أرسل لك proposal." |
| They send a complaint | escalate to human. Do not auto-reply. Do not delete. |
| They ask for pricing | do not give a number. "أرسل لك proposal خلال يومين بعد discovery." |
| They send a photo / file | do not download without asking. Confirm. |
| They go silent for 14+ days | send the breakup. Move on. |

## The human handoff (when AI is not enough)

If the conversation goes into:

- A complaint.
- A legal question.
- A pricing negotiation.
- A privacy question.
- A health / medical question (out of scope).

You (the founder) take over. Do not let the conversation drift back to drafts. The handoff is logged in `templates/launch/approval_queue.example.json` with `action: human_handoff`.

## The consent revocation

If the prospect says "stop messaging me" or "remove me from your list":

1. Acknowledge: "تمام. أحذفك من القائمة."
2. Do not pitch.
3. Do not argue.
4. Log the revocation in the consent record (`status: revoked`).
5. Do not contact them on any channel again.

## The data handling

- WhatsApp messages may contain PII. Do not paste them into reports without redaction.
- The trust preflight includes a PII check: it fails any draft with phone numbers, emails, or names that look real.
- Store WhatsApp data only in the engagement's secure folder. Do not sync to public cloud.

## When to update

- After 30 consent-granted threads: if reply rate < 30%, rewrite the first message.
- If 1+ thread escalates to a complaint, add a "complaint detection" rule to the human handoff trigger.
- If a thread produces a paying client, write a case study (with permission) and reference it in the next WhatsApp first message.
