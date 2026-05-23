# Outbound Policy

> The rules for every outbound message Dealix or its agents send.
> Enforced by `dealix/trust/approval_matrix.py` and `dealix/trust/claim_guard.py`.

## Allowed Channels

- LinkedIn (founder personal account)
- Email (founder personal address or transactional from dealix.sa once verified)
- WhatsApp Business (with explicit prior opt-in only)
- Booked-call follow-up (always permitted post-meeting)

## Forbidden Channels (this quarter)

- Cold WhatsApp messaging
- Cold SMS
- Cold phone calls without prior interaction
- Mass email blasts (any list > 50)
- Direct LinkedIn InMail at scale (> 10/day on a single account)
- Scraped contact databases of any kind

## Per-Message Requirements

Every outbound message must:
1. Be addressed to a single person (no BCC mass-sends)
2. Contain a specific reason for reaching out (sector, trigger, name reference)
3. State a clear next step (15-min call, sample request, content link)
4. Include an opt-out path
5. Pass `claim_guard.py` (no unsubstantiated AI / ROI / compliance claims)
6. Be founder-approved (until automation tier explicitly allows otherwise per `APPROVAL_MATRIX.md`)

## Volume Caps

- LinkedIn DMs: max 25/day per founder account
- Email: max 50/day, max 200/week
- WhatsApp: opt-in only, no cap on opt-in conversations
- Per prospect: max 3 messages without reply, then move to nurture or suppression

Volume caps exist to:
- Protect founder accounts from platform bans
- Force quality over volume
- Stay below "spam" thresholds

## Suppression List Rules

Once a prospect is on the suppression list, **no further automated or manual outbound** for any reason. List sources:

- Explicit "remove me" reply
- "Not interested" reply
- 3 unanswered messages in 60 days
- Negative public signal about Dealix
- Any prior incident (logged in `trust/data_incidents.md`)

Suppression list lives in `trust/suppression_list.csv` (private). The list is **monotonic** — additions only, no removals without founder + advisor signoff.

`dealix/trust/suppression.py` blocks any send to a suppression-list contact.

## Messaging Quality Bar

A message is allowed to leave if:
- It mentions a specific sector or trigger
- It references something real about the prospect's company
- It does not contain superlatives without evidence
- It does not promise ROI numbers
- It does not impersonate a person or role we don't have
- Length: < 600 characters (LinkedIn), < 1500 characters (email)

A message is **rejected** if:
- It contains "synergy", "transformational", "10x", or similar
- It contains a percentage / multiplier claim without source
- It uses a template variable that was not filled (e.g. `{{first_name}}`)
- It links to a destination that isn't allow-listed
- It would arrive on a Saudi public holiday or Friday

## Approval Tiers

| Tier | Definition | Approval needed |
|---|---|---|
| A0 | Internal-only draft (not sent) | none |
| A1 | First outreach to a single prospect | founder approval per message until volume justifies batch approval |
| A2 | Follow-up to existing thread | founder approval per batch |
| A3 | Any public claim (LinkedIn, web) | founder + evidence pack |
| A4 | Regulated / compliance claim | prohibited from automation; founder + advisor required |

These tiers come from `docs/trust/APPROVAL_MATRIX.md`.

## Logging

Every send logs to `trust/approval_log.csv` (private):
```
timestamp, prospect_id, channel, tier, message_id, approver, message_hash, suppression_check_pass
```

The log is append-only. Auditable. Reviewed weekly during Trust check.

## What Happens On Violation

A message that bypasses these rules and is sent anyway:
1. Logged as an incident in `trust/data_incidents.md`
2. Founder runs a 1-hour root cause: process gap or policy gap?
3. Rule added to `DEALIX_DECISION_RULES.md` if systemic
4. Affected prospects added to suppression list pre-emptively
5. Trust scorecard takes a 20-point hit that month

## Review Cadence

- Daily: founder reviews previous day's approval log
- Weekly: incident review in Weekly CEO Review (Trust section)
- Quarterly: rewrite this policy as channel landscape changes

## What This Policy Refuses

- "Just one test cold email blast"
- "Let's try WhatsApp at scale, what's the worst that happens"
- "Buy this Saudi B2B list"
- "Automate the LinkedIn replies too"
- "Use the founder's account from a server in another country"
