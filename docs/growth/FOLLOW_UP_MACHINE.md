# Follow-up Machine

| Field | Value |
|---|---|
| Purpose | Plan time- and event-based reminders across all channels |
| Inputs | sent records, reply events, cadence config |
| Outputs | `followup_queue.csv` |
| Approval class | Internal — reminders surface to operator; sends still gated |
| Trust gate | Suppression, cadence cap, recency |
| Owner | Distribution Operator |
| KPI | Conversion uplift from follow-up vs. first-touch |
| Failure mode | Reply detected after follow-up draft created → draft auto-cancelled |

## Reminder rules

- Default: 4 business days post-send.
- Adjust to persona pace: founder personas → 3 days; ops personas → 5 days.
- Maximum 2 follow-ups per cadence step.
- Reminder auto-cancels if any human reply lands.

## Surface

The Sales Cockpit shows pending follow-ups grouped by account, with the original message and recommended next message.

## Brand notes

- Acknowledge time has passed; do not pretend the prior message did not exist.
- Add new value (a fresh insight, a recent proof) rather than restating the prior ask.
