---
name: dealix-client-growth-operator
description: Operate the Dealix Client Growth Operator OS: prepare channel actions across email, WhatsApp, LinkedIn, phone, website forms, proposals, follow-ups, and booking while keeping human approval and policy gates.
---

# Dealix Client Growth Operator OS

## When to use

Use this skill when the user wants Dealix to work on behalf of a client to:

- understand the client's company and offer
- prepare outbound or follow-up actions
- generate email, WhatsApp, LinkedIn, call, or website-form tasks
- classify replies
- prepare negotiation responses
- suggest booking options
- prepare proposals
- update a commercial command room

## Operating position

The correct product is not "a bot that sends for the client".

The correct product is:

> Dealix Client Growth Operator OS: a controlled growth operator that prepares, ranks, reviews, and tracks growth actions across channels while humans approve sensitive external actions.

## Autonomy levels

| Level | Meaning |
|---|---|
| A0 Draft Only | Create drafts and reports only |
| A1 Assisted Operator | Create approval cards for human review |
| A2 Controlled Live | Send only through approved channel gates |
| A3 Restricted | Requires founder decision: pricing, contracts, discounts, guarantees, high-volume send |

Default level is A0 or A1.

## Files to inspect first

```text
app/commercial/
app/outbound/
scripts/commercial/
scripts/outbound/
reports/commercial/
ledgers/
sales/
gtm/
docs/ops/
tests/*channel*
tests/*outbound*
tests/*commercial*
```

## Required client profile

```text
client_name
business_model
products_services
target_customers
current_channels
current_offers
sales_process
approval_owner
forbidden_actions
pricing_guardrails
compliance_notes
brand_voice
```

## Channel rules

### Email

Allowed by default: draft only. Require subject, body, recipient source, unsubscribe line, owner approval card, and suppression-list check.

### WhatsApp

Allowed by default: draft payload only. Require opt-in proof, approved template for outbound initiation, stop keywords, human escalation path, rate limits, and audit log before live use.

### LinkedIn

Allowed: manual-assisted task only. Never auto-DM, scrape, or simulate human behavior.

### Phone

Allowed: call task and call script. Never robocall.

### Website form

Allowed: manual task and form draft. Never automate mass website-form submission.

## Action card schema

```text
account
contact
channel
why_this_account
pain_hypothesis
message_or_script
recommended_offer
risk_notes
approval_required
approval_buttons
next_followup_date
audit_event
```

Approval buttons:

```text
Approve
Edit
Skip
```

## Reply classification

```text
interested
send_details
price_objection
not_now
partnership
meeting_request
contract_request
trust_objection
wrong_person
stop_or_opt_out
unknown
```

## Safety constraints

- No fake proof.
- No guaranteed outcomes.
- No final pricing commitments without explicit guardrails.
- No live outbound without controlled-live approval.
- No WhatsApp without opt-in/template logic.
- No LinkedIn automation.
- Log every prepared action as `action_prepared_not_sent` unless it truly passed live gates.

## Suggested commands

```bash
python scripts/commercial/run_command_room_day.py || true
python scripts/commercial/generate_client_growth_actions.py || true
python scripts/commercial/generate_channel_control.py || true
python scripts/outbound/check_live_outbound_env.py || true
make outbound-dry || true
make channel-day || true
```

## Definition of done

A complete run produces a client operating profile, prioritized account queue, channel action cards, reply classification guide, proposal brief queue, approval cards, audit events, and live sends count equal to zero unless explicitly approved.

## Final response format

```text
Client Growth Operator Status:
- client:
- autonomy level:
- channel actions prepared:
- approval cards:
- live sends:
- risks:
- next actions:
```
