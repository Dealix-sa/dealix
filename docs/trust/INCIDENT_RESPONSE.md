# Incident Response

> What happens when something breaks Trust.
> Used by founder + advisor; lives next to muscle memory.

## Severity Classification

| Severity | Definition | Response time | Notification |
|---|---|---|---|
| **SEV-1** | Customer data leak, public overclaim that hurts a customer, regulatory exposure | < 1 hr | Founder + advisor + affected customer |
| **SEV-2** | Suppression-list breach, claim_guard miss in published material, prolonged trust gate outage | < 4 hr | Founder + advisor; customer if affected |
| **SEV-3** | Single missed approval, claim_guard catch (not missed), agent misbehavior caught internally | < 24 hr | Founder; log only |
| **SEV-4** | Process gap noticed (no harm done) | < 7 days | Log + Weekly CEO Review |

## Response Procedure (the 4 R's)

For every incident, follow this order:

1. **Reduce harm** — stop the bleeding (pause sends, retract artifact, block channel)
2. **Record** — log timestamp, what happened, who knew, what we did
3. **Reach out** — notify affected parties if SEV-1 or SEV-2
4. **Reform** — post-mortem + rule change to prevent recurrence

## Step-By-Step (SEV-1)

```
T+0    Detect / receive notification
T+5m   Pause all outbound automation
T+15m  Notify advisor
T+30m  Initial assessment: scope, affected parties, regulatory implications
T+1h   First customer / regulator outreach (if applicable)
T+4h   Public communication if required (PR, social, blog) — claim_guard pass
T+24h  Full incident document in trust/data_incidents.md
T+7d   Post-mortem + rule changes committed
T+30d  Follow-up with affected parties; close-out
```

## Incident Log Schema

`trust/data_incidents.md` (private repo) format:

```markdown
## INC-NNNN — YYYY-MM-DD — {short title}

**Severity:** SEV-N
**Detected by:** {who, how}
**Affected:** {parties, count, scope}
**Root cause:** {one paragraph}
**What we did:**
- {action} at {timestamp}
- {action} at {timestamp}
**Communication:**
- {who notified, when, channel}
**Rule changes:**
- {file → change}
**Status:** open / resolved
**Closed:** YYYY-MM-DD (with closing note)
```

## Communication Templates

### Customer notification (SEV-1, data-related)

> Subject: Important: a notice from Dealix
>
> {Customer name},
>
> On {date}, {what happened, in plain terms}. We've taken {actions} to contain it. The impact on your engagement is {scope}. We're sharing this proactively because trust matters more than convenience.
>
> Here's what we're doing: {steps}.
> Here's what we're asking of you: {action items if any}.
> Here's our timeline: {dates}.
>
> I'm available immediately. {Founder contact}.
>
> — Bassam

### Customer notification (SEV-2, message-related)

> {Customer name}, a quick note: {what happened, in plain terms}. We've corrected it ({how}). No customer data was affected. We're sharing because we always do, even on smaller misses. Anything else you need?

## Post-Mortem Template

```markdown
## INC-NNNN Post-Mortem

### What happened
{3-5 sentences, blameless, factual}

### Timeline
{HH:MM events}

### Why it happened (root cause)
{Why, not who}

### Why our existing controls didn't catch it
{Honest assessment}

### What we changed
- {Rule / code / process change}
- {Test added}
- {Doc updated}

### What we learned
{1-2 sentences for company learning log}

### Follow-up actions (with owners + dates)
- [ ] {action} — owner — by date
```

## What This Process Refuses

- Hiding incidents (every SEV-1/2 gets logged + reviewed)
- Blaming individuals (root cause, not blame)
- Closing without rule change (if there's no rule change, the root cause wasn't reached)
- "It won't happen again" without a test or policy that makes it not happen again
- Skipping customer notification for SEV-1/2 because "they might not have noticed"

## Drills

- Quarterly: tabletop drill of a SEV-1 scenario (founder + advisor)
- Annual: full review of all incidents, pattern analysis
- After any SEV-1: drill within 30 days on the same scenario
