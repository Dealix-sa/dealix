# Outreach Cadence

> Per-prospect sequence, channel mix, timing.

## Default Cadence (per qualified lead, score 60–89)

| Step | Day | Channel | Action |
|---|---|---|---|
| 1 | 0 | LinkedIn | Personalized DM (per sector playbook) |
| 2 | 4 | LinkedIn | Soft follow-up if no reply, share a sector signal/resource |
| 3 | 9 | Email | Different angle, founder-personal, link to relevant content |
| 4 | 16 | LinkedIn | "Last note for now" — explicit close-loop |
| — | 60 | Nurture | If still no reply: move to nurture (content + quarterly check-in) |

## High-Priority Cadence (score 90+)

| Step | Day | Channel | Action |
|---|---|---|---|
| 1 | 0 | Warm intro (if available) OR LinkedIn DM | Founder-personal |
| 2 | 2 | LinkedIn | Soft follow-up if no reply |
| 3 | 5 | Email | Different angle, attached sanitized sample artifact |
| 4 | 9 | Voice note (LinkedIn) | Founder-personal voice |
| 5 | 14 | Final | Explicit close-loop, polite |
| — | 30 | Nurture | If no reply: 90-day check-in scheduled |

## Inbound Cadence

| Step | Day | Channel | Action |
|---|---|---|---|
| 1 | within 24 hr | Same channel inbound came on | Personal reply, no template language |
| 2 | within 48 hr | Calendar | Book a 15-min Free Diagnostic call |
| 3 | post-call | Email | Send sanitized sample + proposal-ready scope |

## Cadence Rules

- **Max 4 outbound touches per prospect across all channels** (before nurture)
- **Min 4 days between touches** (no spam)
- **Always different angles** — never repeat the same message in different words
- **Always include opt-out** in messages 2+
- **Never call without explicit prior interaction** (suppression risk)
- **No SMS / WhatsApp without explicit prior opt-in**

## Channel Switching Rules

- Stay on the channel the prospect first responded on
- If switching channels for a follow-up, reference the prior message
- Never run multiple parallel channels simultaneously to the same person

## Friday + Weekend Rule

- No outbound sends on Friday (Saudi work week)
- No outbound sends on public holidays
- Saturday is forced founder rest day; no outbound founder-sourced sends

## Volume Caps (recap from OUTBOUND_POLICY)

- 25 LinkedIn DMs/day per founder account
- 50 emails/day, 200/week
- WhatsApp opt-in only

## Cadence Tracking

Every prospect has a cadence_state in `pipeline/pipeline_tracker.csv` (private):
```
cadence_step (0-4)
last_touch_at
next_touch_due_at
cadence_type (default | high_priority | inbound)
```

## When To Pause A Cadence

Pause if:
- Prospect replies (even negatively — drop to single human follow-up)
- Prospect engages with content (LinkedIn post like / comment)
- Prospect's company has a public crisis (layoffs, scandal — wait it out)
- Saudi public holiday during cadence window — pause and resume

## When To Kill A Cadence

Kill if:
- "Not interested" / "remove me" → suppression list immediately
- 4 touches no reply → nurture
- Buyer left the company → restart with new contact (new lead row, not continuation)
- Negative public signal about Dealix from this contact → suppression + incident log

## Review Cadence

- Daily: cadence_step transitions logged
- Weekly: reply rate per cadence step (which message converts?)
- Monthly: A/B test cadence variants (with formal hypothesis in `learning/`)
