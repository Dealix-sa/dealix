# Controlled Communication Roadmap

## Purpose

Dealix can support intelligent client communication, but production use must be controlled, reviewed, and auditable.

## Baseline state

- Mode: draft_only
- External sending: disabled
- Sales agent: authorized assistant
- Founder review: required
- Identity: transparent

## Required gates before production email

1. SPF configured.
2. DKIM configured.
3. DMARC configured.
4. Sender identity is clear.
5. Unsubscribe handling exists for commercial scale.
6. Suppression list exists.
7. Bounce handling exists.
8. Rate limits exist.
9. Audit events exist.
10. Manual stop switch exists.

## Required gates before production WhatsApp

1. Recipient opt-in exists.
2. Business name is clear in opt-in context.
3. Template is approved.
4. Suppression and opt-out handling exists.
5. Conversation category is known.
6. Human approval exists for sensitive flows.
7. Audit trail exists.

## Identity rules

Allowed:

- Dealix Sales Assistant
- Dealix team
- authorized sales assistant for the client

Requires explicit owner approval:

- named founder identity
- named sales director identity
- named executive identity

Not allowed:

- misleading display names
- fake reply framing
- fake urgency
- hidden sender identity
- guaranteed revenue claims

## Phases

### Phase 1: Draft-only

Generate drafts, packs, objections, and next actions.

### Phase 2: Approval queue

Queue drafts and allow owner approval one by one.

### Phase 3: Controlled email

Use only approved messages under rate limits and suppression checks.

### Phase 4: Controlled WhatsApp

Use only opt-in contacts and approved templates.

### Phase 5: Client-owned Sales Agent

Deploy per-client voice, identity, limits, audit trail, and approval matrix.

## Non-negotiable

No production external communication is enabled unless the gates above are satisfied.
