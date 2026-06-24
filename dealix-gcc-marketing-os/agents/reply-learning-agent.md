# Reply Learning Agent

## Role
Processes all inbound replies, classifies them, updates suppression list, and extracts angle/language learning signals.

## Reply Categories
- positive_interested → book follow-up
- soft_no_timing → schedule follow-up in 30 days
- hard_no → add to suppression.jsonl immediately
- referral → create new lead from referred contact
- auto_reply → reschedule same draft in 3 days
- question → route to founder for manual reply
- unclassified → flag for manual review

## Learning Output → memory/learning_log.jsonl
```json
{
  "type": "reply",
  "sector": "legal",
  "country": "saudi_arabia",
  "language": "ar",
  "angle": "document_retrieval",
  "draft_version": "A",
  "outcome": "positive_interested",
  "signal": "reply_open_rate|click|reply"
}
```

## Rules
- Hard no → immediate suppression, no follow-up
- Soft no → respectful pause, no aggressive follow-up
- Learning signals feed back into pain-hypothesis agent angle selection
- All suppression updates are immediate and permanent
