# Follow-up System

> **Status:** Operating policy. Every reply gets a follow-up. Every "no" gets logged.
> **Tool:** `templates/launch/approval_queue.example.json` + `scripts/founder_daily_command_dry_run.py`.

## The principle

> A follow-up is not a nudge. It is a structured re-engagement that respects the prospect's time.

## The 3 categories of follow-up

### 1. Pending reply (no response yet)

| Day | Action |
| --- | --- |
| Day 0 | First message sent. |
| Day 3 | Follow-up 1. Short, low-friction, no pitch. |
| Day 7 | Follow-up 2. One specific question. |
| Day 14 | Breakup. Final message. Re-engage in 60 days. |

After the breakup, move the account to `paused` status. Do not send again for 60 days.

### 2. Replied but not converted (objection, "think about it", "next quarter")

| Day | Action |
| --- | --- |
| Day 0 | Reply received. Log it. |
| Day 1 | Send a 1-sentence acknowledgement: "شكراً على الرد." |
| Day 3 | Send a relevant resource (1 case study, 1 article). |
| Day 7 | Re-engage with the original CTA. |
| Day 14 | If no movement, ask: "متأكد ما تناسبكم في هذي المرحلة؟" |
| Day 30 | Last touch. Move to `paused`. |

### 3. Converted (became a client)

The follow-up shifts to delivery. See `docs/delivery/CLIENT_VALUE_REPORTING_AR.md`.

## The 5 rules for follow-ups

1. **Always add value.** A follow-up that says "just checking in" is a waste of their time and yours.
2. **One ask per follow-up.** Not three.
3. **Same channel as the first message** (unless they switched).
4. **Reference the previous message** ("بناءً على رسالتي السابقة...").
5. **Always give an exit.** "لو ما تحب، اعمل reply بكلمة 'لا' وأنا أوقف."

## The 5 follow-up types (templates)

### A. "Resource" follow-up

> مرحبا [الاسم]،
>
> قبل ما أكمل، لقيت هذا المقال/الـ case study مناسب لحالتكم:
> [رابط]
>
> لو ما عندك وقت، احذف الإيميل. لو عجبك، نكمل.
>
> — [الاسم]

### B. "Question" follow-up

> مرحبا [الاسم]،
>
> سؤال واحد: [سؤال محدد].
> لو ما تحب تجاوب، احذف الإيميل.
>
> — [الاسم]

### C. "Specific ask" follow-up

> مرحبا [الاسم]،
>
> أحتاج 30 دقيقة من وقتك. متى يكون أسهل — الأسبوع هذا أو الجاي؟
>
> — [الاسم]

### D. "Breakup" follow-up

> مرحبا [الاسم]،
>
> أرسلت 3–4 رسائل ما في رد. أفهم إن الأولويات غيرت.
> لو احتجتني بعد 60 يوم، اعمل reply على أي إيميل سابق.
> ما راح أزعجك قبلها.
>
> — [الاسم]

### E. "Reactivation" follow-up (after 60+ days)

> مرحبا [الاسم]،
>
> رجعت أتكلم معك بعد 60 يوم. أرسلت لك قبل كذا عن [الموضوع].
> هل الموضوع لا يزال مهماً، أو تغيّرت الأولويات؟
>
> — [الاسم]

## The timing rules

- **Email follow-up:** Day 3, 7, 14, then 60.
- **LinkedIn follow-up:** Day 3, 7, 14, then 60 (only if connection still alive).
- **Phone follow-up:** 1 missed call + 1 LinkedIn DM same day. 2 missed calls = stop.
- **WhatsApp follow-up:** Day 3, 7, then stop (consent = revocable; do not push).

## The logging

Every follow-up is logged in `templates/launch/approval_queue.example.json` with:

```json
{
  "follow_up_id": "fu_001",
  "account_id": "agency_x_riyadh",
  "channel": "email",
  "type": "resource",
  "sent_at_iso": "2024-12-04T10:00:00Z",
  "previous_follow_up_id": null,
  "next_follow_up_id": "fu_002",
  "result": "no_reply",
  "next_action": "send_follow_up_2"
}
```

## The metrics

Weekly:

- Follow-up count by type.
- Reply rate by follow-up type.
- Reactivation rate (60+ day follow-ups that get a reply).
- Disqualification rate (after breakup or reactivation).

## When to update

- If the resource follow-up has < 5% reply rate, drop it (no value).
- If the breakup has < 1% reactivation, drop it (no recovery).
- If the question follow-up has > 20% reply rate, double down.
