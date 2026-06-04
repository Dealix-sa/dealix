# Reply Classifier Prompt

You are classifying an inbound reply to a Dealix outreach email.

## Reply
From: {{from_name}} at {{company_name}}
Body:
---
{{reply_body}}
---

## Categories
- positive_interested: Wants to learn more, asks for info, agrees to call
- soft_no_timing: Not now, busy, try later
- hard_no: Not interested, please stop, unsubscribe
- referral: Refers to someone else
- auto_reply: Out of office
- question: Asks a specific question
- unclassified: Cannot determine

## Output
```json
{
  "category": "positive_interested",
  "confidence": 0.92,
  "recommended_action": "send_one_pager_and_book_call",
  "suppress": false,
  "urgency": "high"
}
```
