# Disqualification Rules

> **Status:** Hard rules. If a rule fires, walk away.

## The 5 hard disqualifiers

1. **"Send us a proposal first, we'll see."** — No audit, no proposal. Walk.
2. **"Can you guarantee 2X pipeline in 90 days?"** — We don't guarantee. Walk.
3. **"We need you to send a WhatsApp campaign to 10k numbers."** — Cold WhatsApp. Walk.
4. **"We can't sign a consent record; just access our data."** — No consent, no access. Walk.
5. **"We'll pay you in outcomes, not fees."** — Outcomes-based pricing is a known scam shape. Walk.

## The 5 soft disqualifiers (proceed with care)

1. **The decision maker is in a different city and unreachable.** — Defer until you have a warm intro.
2. **The company is in a sector we have not yet scored.** — Score the sector first; if score < 60, walk.
3. **The founder has a public dispute / controversy.** — Defer; risk of brand association.
4. **The account is in a regulated industry (health, legal, finance) AND we don't have a DPA template signed.** — Defer until DPA is in place.
5. **The ICP score is below 50.** — Drop from the active list. Re-score in 90 days.

## The 3 walk-away scripts

If you need to say no:

### "No audit, no proposal"

> "شكراً على الاهتمام. الطريقة اللي نشتغل فيها هي: نبدأ بـ audit صغير (5 أيام، تقرير واحد). لو التقرير ما استفدت منه، ما نكمل. لو تحب، نبدأ من هنا."

If they insist on a proposal first: walk.

### "We don't guarantee"

> "ما نقدر نضمن نتيجة رقمية. اللي نقدر نضمنه: تقرير audit محدد + خطة إصلاح. لو ما استفدت، تنسى الموضوع."

If they insist on a guarantee: walk.

### "We don't do cold WhatsApp"

> "ما نرسل cold WhatsApp، وننصحكم ما تسوون. الحل اللي نقدمه يعتمد على الـ consent."

If they insist on a cold blast: walk.

## The 3 escalation paths

If the prospect is good but the rules are blocking:

| Rule | Escalation |
| --- | --- |
| No consent record, no access | founder + counsel sign a one-time exception (logged in approval queue). |
| Regulated industry, no DPA | founder + counsel draft a sector-specific DPA. Time-box: 2 weeks. |
| ICP < 50 but warm intro | founder decides to pursue as a "named account" override (logged in approval queue). |

Escalation is founder-decision, not a script. Do not escalate without logging it.

## How to log a disqualification

```json
{
  "account_id": "agency_x_riyadh",
  "status": "disqualified",
  "rule": "no_audit_no_proposal",
  "reason": "Insisted on a proposal before the audit; we declined.",
  "logged_at_iso": "2024-12-01T10:00:00Z",
  "logged_by": "founder"
}
```

Add to `templates/launch/approval_queue.example.json` with `action: disqualified`.

## Why disqualification is a feature

The fastest way to lose trust is to take a deal that does not fit. The fastest way to grow is to take deals that do. Disqualification is a discipline, not a failure. Log it, learn from it, move on.
