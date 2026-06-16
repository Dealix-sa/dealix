# WhatsApp Business Runbook

## Account Setup
1. Meta Business Manager.
2. WhatsApp Business API (Cloud API).
3. Verified phone number.
4. Approved message templates.

## Opt-In Requirements
- Explicit opt-in before first business-initiated message.
- Record consent source and timestamp.
- Easy opt-out via STOP keywords.

## Sending Rules
- Business-initiated messages must use approved templates.
- Template-only mode by default.
- 10 messages/day limit.
- 5 messages/batch limit.
- 120 seconds between sends.

## STOP Keywords
`STOP`, `UNSUBSCRIBE`, `إيقاف`, `الغاء`, `إلغاء`

## Webhook
Endpoint: `GET/POST /api/v1/webhooks/whatsapp`
- Verify token configured in Meta dashboard.
- Signature verified in production.

## Monitoring
- Template rejection rate.
- Message delivery rate.
- Opt-out rate.
