---
name: dealix-revenue-command-room
description: Run or build the Dealix Revenue Command Room OS: target research, scoring, drafts, follow-ups, proposal briefs, daily reports, and founder review actions without uncontrolled external sending.
---

# Dealix Revenue Command Room OS

## When to use

Use this skill when the user asks to:

- run Dealix's daily revenue workflow
- build or improve a revenue command room
- generate target lists, outreach drafts, follow-ups, or proposal briefs
- prioritize leads and deals
- create a founder daily sales report
- prepare commercial launch artifacts
- turn sales scripts into a repeatable operating loop

## Core doctrine

Dealix does not sell generic automation. Dealix builds a daily revenue operating system that converts scattered prospects, conversations, offers, follow-ups, and decisions into a clear action queue.

The system may generate drafts and recommendations. It must not send externally by default.

Required safe defaults:

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Files to inspect first

```text
Makefile
scripts/revenue/
scripts/commercial/
scripts/outbound/
app/commercial/
app/outbound/
ledgers/
reports/revenue/
reports/commercial/
reports/command_room/
sales/
gtm/
tests/saas/
tests/*revenue*
tests/*outbound*
```

## Expected workflow

1. Detect the current repo state.
2. Confirm safe outbound defaults.
3. Locate the canonical revenue ledger.
4. Validate targets.
5. Score targets.
6. Generate outreach drafts only.
7. Generate follow-ups only.
8. Generate proposal briefs.
9. Build or refresh the command room snapshot.
10. Produce a founder daily report.
11. Print exact next actions.

## Required target schema

```text
company_name
sector
city
website
source_url
contact_page_url
public_email
phone
linkedin_url
verification_status
confidence
pain_hypothesis
dealix_angle
recommended_offer
owner_decision
```

## Safety gates

Do not allow a send-ready action unless:

- `source_url` exists
- `verification_status` is at least `verified` or `approved_to_contact`
- the message is not deceptive
- opt-out language exists for email
- WhatsApp has opt-in and approved template logic
- LinkedIn is manual task only
- a human approval card exists

## Suggested commands

```bash
python scripts/revenue/run_revenue_day.py || true
python scripts/commercial/run_command_room_day.py || true
python scripts/commercial/generate_founder_review_actions.py || true
python scripts/commercial/generate_command_room_snapshot.py || true
make company-day || true
make full-revenue-day || true
make command-room || true
```

## Definition of done

A complete Revenue Command Room run produces:

- updated revenue report
- updated command room snapshot
- target score list
- outreach drafts
- follow-up queue
- proposal brief queue
- founder review actions
- proof that live sends remain zero
- final summary with exact next 10 actions

## Final response format

```text
Revenue Command Room Status:
- branch:
- files inspected:
- files changed:
- commands run:
- reports generated:
- drafts generated:
- live sends:
- blockers:
- next actions:
```
