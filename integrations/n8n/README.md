# n8n — external automation (allowed surface only)

`distribution_blueprint.json` is a **reference** workflow you import into your
own n8n instance. It ships with `active: false` and must stay inactive until
reviewed. It connects an external lead-intake webhook to the Dealix
`POST /api/v1/distribution/prospects` endpoint — the prospect is created in a
**draft-only** state; outreach still waits for founder approval inside Dealix.

## Allowed in n8n (plan §18)

- Lead intake → create prospect (draft-only)
- Approval reminders / follow-up reminders (notify the founder)
- Calendly booking prep
- HubSpot sync
- Moyasar paid-event ingestion → mark a payment handoff `paid`
- Weekly distribution summary delivery (to the founder)

## NOT allowed in n8n

- The AI deciding to send a message
- Cold WhatsApp automation
- LinkedIn automation
- Scraping
- Editing secrets
- Production deployment

## Environment

| Variable | Purpose |
|----------|---------|
| `DEALIX_API_BASE` | Base URL of the Dealix API |
| `DEALIX_ADMIN_API_KEY` | Admin key for the distribution endpoints |

Keep credentials in n8n's own credential store; never commit them. The
`agent_security_gate` and the doctrine guards apply to anything that touches
the repo — n8n lives outside the repo and must follow the same posture.
