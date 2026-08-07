# Commercial Safety Gates

## Default

Dealix generates drafts and reports only. It does not send externally by default.

## Required before live email

- EXTERNAL_SEND_ENABLED=true
- EMAIL_SEND_ENABLED=true
- OUTBOUND_MODE=controlled_live
- approved draft
- source_url
- unsubscribe wording
- suppression list checked
- daily limit

## Required before WhatsApp

- WHATSAPP_SEND_ENABLED=true
- WHATSAPP_ALLOW_LIVE_SEND=true
- explicit opt-in
- approved template
- opt-out handling
- daily limit

## Current PR

This PR does not enable any live send.
