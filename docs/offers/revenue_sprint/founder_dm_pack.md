# Founder DM Pack (template)

> Drafted patterns the founder picks from. **None of these send themselves.**
> The CLI prepares a draft; the founder presses send.

## Pattern A — pipeline lift

```
Hi <first-name>, I noticed <specific signal from their public activity>.

I run Dealix; we help <segment> founders pull 25 named, qualified leads into
their pipeline in 7 days. Fixed scope, SAR 2,500 first sprint.

If useful, I can show you a sample built from your own public footprint —
no commitment. Worth 15 minutes?
```

## Pattern B — outreach pack

```
Hi <first-name>, your team posted <signal>. We help <segment> founders
build a personalised outreach pack — 25 DMs / emails ready to send + a
response playbook — in 7 days. SAR 2,500.

Want me to draft 3 examples against your real ICP this week?
```

## Pattern C — proof pack

```
Hi <first-name>, you mentioned <objection: "show me results"> on <where>.

We build customer-ready proof packs that show your offer's measurable value
on real data. 7-day sprint, SAR 2,500 first.

Want a 1-page sample built from a similar customer in your sector?
```

## Pattern D — pricing reset

```
Hi <first-name>, congrats on <recent milestone>. One thing I see often at
this stage: pricing left on the table. We do 7-day pricing resets —
new card, objection rebuttal pack, scripts. SAR 2,500.

Worth a 15-min look at your current pricing?
```

## Pattern E — retainer bridge

```
Hi <first-name>, I see you have <X happy clients>. We help founders convert
one-off projects into retainers — plan + scripts in 7 days. SAR 2,500.

Want me to look at your top 3 clients and draft the retainer ask?
```

## Sending rules (enforced)

1. **No DM is automated.** The CLI saves to `drafts/dm_<lead_id>_v<n>.md` and
   waits for the founder to send.
2. **No mass sends.** Max 10 / day on any single channel until reply rate
   > 15%.
3. **Every send logged the same day** in `revenue/revenue_action_log.csv`
   with `action_type=dm_sent`.
4. **No personal data lives in this public file.** Names/handles live in
   `pipeline/pipeline_tracker.csv` in the private repo.

## Related

- `docs/revenue/REVENUE_COMMAND_CENTER.md`
- `docs/trust/TRUST_COMMAND_CENTER.md`
