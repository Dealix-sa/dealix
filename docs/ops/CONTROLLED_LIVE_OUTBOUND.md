# Dealix Controlled Live Outbound OS

Dealix supports live external sending only through controlled, auditable, rate-limited workflows.

## Operating modes

- disabled: all outbound blocked
- draft_only: drafts generated only
- controlled_live: approved, verified, compliant messages may be sent

## Global gates

Live outbound is allowed only when:

- EXTERNAL_SEND_ENABLED=true
- OUTBOUND_MODE=controlled_live
- OUTBOUND_REQUIRE_APPROVAL=true
- OUTBOUND_REQUIRE_VERIFIED_TARGET=true
- OUTBOUND_REQUIRE_SOURCE_URL=true
- OUTBOUND_REQUIRE_OPT_OUT=true
- OUTBOUND_BLOCK_FAKE_CLAIMS=true
- OUTBOUND_BLOCK_GUARANTEED_ROI=true

## Email gates

Email may be sent only when:

- EMAIL_SEND_ENABLED=true
- message.status=approved
- contact.verification_status=approved_to_send
- contact.email exists
- contact.email_opt_out=false
- contact.source_url exists
- message contains unsubscribe or opt-out wording
- daily limits are not exceeded
- no fake ROI
- no fake testimonials
- no misleading identity

## WhatsApp gates

WhatsApp may be sent only when:

- WHATSAPP_SEND_ENABLED=true
- WHATSAPP_ALLOW_LIVE_SEND=true
- WHATSAPP_SEND_MODE=template_only
- contact.whatsapp exists
- contact.whatsapp_opt_in=true
- contact.whatsapp_opt_out=false
- approved template is used
- STOP / إيقاف / إلغاء requests are honored immediately
- daily limits are not exceeded

## Never allowed

- spam blasting
- random WhatsApp cold automation
- sending after opt-out
- fake guarantees
- fake testimonials
- scraping sensitive personal data
- sending without source_url
- sending without logs
- uncontrolled external sends

## Founder rule

Dealix should automate preparation, scoring, drafting, routing, logging, follow-up reminders, and reporting.  
Live sending is automated only after policy gates pass.
