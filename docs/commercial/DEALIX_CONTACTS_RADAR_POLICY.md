# Dealix Contacts Radar Policy

## Purpose

Google Contacts is not a cold lead source. It is a warm-list hygiene and context layer.

## Current finding

Searches performed:

- `Dealix` — no records
- `RoadLink` — no records
- `MEDCO` — no records
- `Sami` — self/unknown records only; not useful for commercial targeting

## Decision

Do not use Google Contacts for commercial outreach until warm contacts are manually confirmed.

## Contact eligibility

A contact can enter Dealix Contacts Radar only if at least one condition is true:

- inbound lead
- prior reply
- customer or active prospect
- explicit opt-in
- partner referral
- founder-approved warm relationship
- calendar meeting participant with business context
- existing CRM record with permission/source

## Required fields

- Name
- Company
- Role
- Email or phone
- Source
- Relationship context
- Consent / warmth status
- Allowed channel
- Next safe action
- Do-not-contact flag

## Prohibited

- No cold WhatsApp from contacts.
- No mass email from contacts.
- No blind export from personal contacts.
- No assumption that stored contact equals consent.
- No outreach to unknown/self records.

## Status values

```txt
Research
Warm
Opt-in
Customer
Partner
Do Not Contact
Blocked
```

## First manual task

Create a seed list of 20 real warm contacts with context:

```txt
Name | Company | Role | Source | Why relevant | Allowed channel | Safe next step
```

Then Dealix can score and draft messages, but still cannot send without approval.
