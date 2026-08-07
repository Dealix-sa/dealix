# Dealix Growth Command Center OS

## Executive purpose

This system turns Dealix into a founder-led commercial operating machine for Saudi B2B companies.

It combines:

- Company Brain OS
- Revenue Command Room OS
- AI Sales Agent OS
- Offer Intelligence OS
- Customer Pain Radar
- Client Delivery OS
- Trust and Safety Gates
- HubSpot Commercial OS

## Positioning

Dealix is not a chatbot, CRM, dashboard, or marketing agency.

Dealix builds AI Operating Systems that transform scattered sales, WhatsApp follow-up, proposals, delivery, reports, and executive decisions into measurable daily workflows.

## What companies buy

Companies do not buy AI. They buy relief from operational pain:

| Pain | Dealix system | Business outcome |
|---|---|---|
| Lost leads and weak follow-up | Revenue Command Room OS | daily next actions and pipeline visibility |
| Unclear owner decisions | Company Brain OS | daily CEO decision and weekly board memo |
| Sales team replies inconsistently | AI Sales Agent OS | approved drafts, objection handling, and negotiation guardrails |
| Offers do not close | Offer Intelligence OS | clearer offer, pricing ladder, and proposal structure |
| Delivery proof is scattered | Client Delivery OS | proof packs and acceptance criteria |
| AI is used without controls | Trust and Governance OS | human gates, audit log, and data rules |

## AI Sales Agent policy

The Sales Agent may act as:

- Dealix Sales Assistant
- Dealix team
- authorized sales assistant for the client company
- approved representative identity when explicitly authorized by the owner

The Sales Agent must not:

- impersonate a named manager without explicit approval
- imply a reply or relationship that does not exist
- promise guaranteed revenue
- invent case studies
- bypass approval gates
- send messages after opt-out
- initiate WhatsApp production messages without opt-in and approved template

## Daily targeting system

Daily research is not daily spam.

The operating rhythm is:

| Step | Target |
|---|---:|
| research accounts | 100 |
| verify accounts | 40 |
| generate drafts | 25 |
| founder-approved contacts | 10-15 |
| call attempts | 3-5 |
| discovery calls | 1-2 |
| proposal or diagnostic offer | 1 |

Each target must have:

- source_url
- sector
- city
- pain hypothesis
- recommended product
- verification_status
- owner_decision
- opt-out handling for email drafts

## Negotiation doctrine

- Diagnose first, discount last.
- Never reduce price without reducing scope.
- Use pilot/sprint entry points instead of speculative full builds.
- Attach each offer to a measurable operating outcome.
- Convert sprint proof into retainer scope.
- Keep proof language factual.

## Command Center lanes

### 1. Revenue lane

Tracks targets, drafts, follow-ups, proposals, meetings, and pipeline.

### 2. Company Brain lane

Generates daily decision, weekly board memo, bottleneck scan, and future radar.

### 3. Sales Agent lane

Creates reviewable drafts, discovery questions, objection responses, and negotiation guardrails.

### 4. Delivery lane

Tracks client intake, diagnosis, blueprint, acceptance criteria, proof pack, and renewal risk.

### 5. Trust lane

Blocks live external action unless safety gates are complete.

## External communication state

Default state remains draft-first:

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

Production sending may be enabled only in a separate controlled-live release after DNS, opt-out, consent, suppression, rate limits, audit logs, and owner approval are complete.

## Founder daily operating question

Every day, Dealix must answer:

1. Who should we target today?
2. What pain are we solving for them?
3. Which product fits best?
4. What message should be reviewed?
5. What follow-up is due?
6. What proposal should be created?
7. What risk must be blocked?
8. What proof can we show?
9. What is the single CEO decision today?
10. What must not be done today?
