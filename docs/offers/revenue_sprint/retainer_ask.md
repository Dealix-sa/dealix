# Retainer Ask — `<client>`

> Sent with the handoff. Separate message from the feedback request — they
> have different jobs.

## Message

```
Hi <first-name>,

You now have <artefact 1, 2, 3>. The fastest way to compound it is to keep
running, on a monthly cadence, the same loop that produced those.

Retainer scope (one page, no fluff):

- 2 sprints / month, picked from the same kit.
- Same fixed scope per sprint, named outcome per sprint.
- SAR <amount> / month.
- No multi-month lock-in. Cancel any month, end-of-month.
- I am still your single point of contact.

If "yes": reply "let's do it" and I'll send the agreement + first month's
payment link.

If "not yet": tell me what would need to be true for this to be a yes in 30
days, and I'll come back then.

If "no": no chasing — and thank you again for the sprint.

— <founder>
```

## Hard rules

- One retainer ask per client per sprint. **Do not** also ask in the feedback
  message or the next-step section of the delivery report.
- Price the retainer based on **delivered value**, not on time spent.
- If the client says "yes" — payment / PO must be logged in
  `revenue/revenue_action_log.csv` before any retainer work starts.

## After the ask

- [ ] Log the ask in `revenue/revenue_action_log.csv` (`action_type=retainer_ask`).
- [ ] Schedule a 7-day follow-up in `founder/decision_queue.md`.
- [ ] If accepted: stage moves to `won_retainer` in the pipeline tracker.
