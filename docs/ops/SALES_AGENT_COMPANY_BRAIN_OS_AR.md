# Dealix Sales Agent and Company Brain OS

## Purpose

This document defines a review-first commercial operating layer for Dealix.

Dealix should help the founder and client teams prepare better sales work:

- account research
- pain hypothesis
- product fit
- sales draft preparation
- discovery questions
- negotiation notes
- proposal brief
- delivery proof plan

The system does not send messages by default. It prepares work for human review.

## Positioning

Dealix is a Saudi B2B AI Operating Systems company.

It is not just a chatbot, CRM, dashboard, or marketing agency.

Dealix builds operating systems that connect sales, follow-up, proposals, client delivery, trust, and management decisions into daily workflows.

## Sales Agent OS

The Sales Agent OS helps create:

- first draft
- follow-up draft
- discovery call agenda
- objection notes
- proposal brief
- next action
- HubSpot task or note proposal

## Company Brain OS

The Company Brain OS helps create:

- daily executive decision
- top opportunities
- top risks
- bottleneck notes
- weekly board memo
- 30-day action plan
- proof pack after delivery

## Target assessment fields

Each target company should have:

| Field | Purpose |
|---|---|
| company_name | target account |
| sector | business sector |
| source_url | public source |
| verification_status | research state |
| buyer_persona | likely decision maker |
| pain_hypothesis | proposed business pain |
| recommended_product | best first offer |
| draft_message | review-only draft |
| discovery_questions | call preparation |
| negotiation_notes | boundaries and options |
| owner_decision | hold, review, send, call, discard |

## Negotiation rules

- Start with a diagnostic or sprint.
- Do not discount without scope change.
- Do not promise guaranteed revenue.
- Do not use fake proof.
- Keep the first engagement narrow and measurable.
- Create a scope card before delivery.

## Daily operating rhythm

- research 100 companies
- verify 40 companies
- prepare 25 sales packs
- review 10 to 15 drafts
- attempt 3 calls
- qualify 1 to 2 discovery calls
- prepare 1 scoped proposal

## Safety defaults

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Acceptance criteria

- every target has source_url
- every pain statement is framed as a hypothesis
- every draft is review-only
- every proposal has scope and acceptance criteria
- every delivery produces a proof pack
