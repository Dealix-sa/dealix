# Communication Activation Gates

## Purpose

This document defines what must be true before Dealix enables production communication.

## Email gates

- SPF or DKIM is configured for the sending domain.
- Bulk sending requires SPF, DKIM, and DMARC.
- TLS is used.
- PTR and forward DNS are valid.
- Spam rate is monitored and remains below 0.30 percent.
- Marketing messages include one-click unsubscribe and a visible unsubscribe link.
- Sender identity, From header, subject, and display name are accurate.
- Sending volume increases gradually.

Reference: https://support.google.com/a/answer/81126

## WhatsApp gates

- Official WhatsApp Business Platform is used.
- Business portfolio, WABA, and business phone number are configured.
- Recipient opt-in is captured.
- Template messages are approved before use.
- Business name is clear in opt-in.
- Webhooks are configured for replies and status updates.

Reference: https://developers.facebook.com/docs/whatsapp/overview

## HubSpot gates

- Owner approves each write-back category.
- Products are mapped to service catalog.
- Tasks are attached to companies or contacts.
- Deals are created only after discovery qualification.
- Notes are factual and audit-friendly.
- Line items are added only after offer scope is approved.

Reference: https://knowledge.hubspot.com/products/create-and-manage-products

## Current status

Current status remains controlled automation. HubSpot products and tasks are created. Production communication is not enabled.
