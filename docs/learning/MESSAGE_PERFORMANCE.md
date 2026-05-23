# Message Performance

> Track which messages, in which sectors, on which channels, actually convert.

## Storage

`learning/message_performance.csv` (private):

```
message_id, framing, sector, channel, language, sent_at, sent_count, reply_count, reply_rate, call_booked_count, proposal_sent_count, paid_count, founder_hours_to_produce
```

## Capture Discipline

- Every approved outreach message gets a `message_id` before it's sent
- Send count incremented per send
- Reply count incremented when a reply is logged in pipeline
- Conversion counts updated at each stage transition

## Monthly Review

```markdown
# Message Performance Review — YYYY-MM

## Top Performers (by reply rate, n ≥ 5 sends)
1. message_id ___ | reply_rate ____% | sector ____ | framing ____
2. message_id ___ | reply_rate ____% | sector ____ | framing ____
3. message_id ___ | reply_rate ____% | sector ____ | framing ____

## Bottom Performers (by reply rate, n ≥ 5 sends)
- _____ — why?
- _____ — why?

## Patterns
- Most-replied framing this month: _____
- Most-replied sector: _____
- Most-replied channel (LinkedIn / email): _____
- Most-replied length / format: _____

## Decisions
- Promote to playbook (sector update): _____
- Iterate: _____
- Kill: _____
```

## Sector × Channel Matrix

Maintain a rolling matrix:

| Sector | LinkedIn DM | Email | Voice note | Inbound (content) |
|---|---|---|---|---|
| Logistics | _% | _% | _% | _ leads |
| B2B services | _% | _% | _% | _ leads |
| Manufacturing | _% | _% | _% | _ leads |

Update monthly.

## Promotion Rule

A message variant gets promoted into the sector playbook when:
- ≥ 5 sends
- ≥ 15% reply rate
- Reply quality > "remove me" (real engagement)
- Founder approval

## Kill Rule

A message variant gets killed when:
- ≥ 10 sends with < 5% reply rate, OR
- Generates suppression-list adds at higher rate than baseline, OR
- Triggers any claim_guard or trust flag

## Per-Send Logging Discipline

- Every send → CSV row
- Every reply → CSV update
- Don't backfill; log in real time

## Confounders To Watch

- Channel saturation (LinkedIn changes throttles)
- Sector cycles (Ramadan, year-end, sector-specific dead seasons)
- Founder volume (when founder sends fewer, each one is more curated)
- Recipient quality (high-fit list → higher replies regardless of message)

## What This Refuses

- A/B claims with n < 5
- Promoting a message because "it felt right"
- Killing a message before n ≥ 10 sends
- Mixing reply quality into reply rate (track both)
- Comparing messages across very different sectors as if they're comparable
