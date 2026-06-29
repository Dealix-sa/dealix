---
name: dealix-trust-and-outbound-safety
description: Review Dealix claims, privacy, consent, outbound actions, channel policies, approval cards, audit logs, and safe defaults before any external communication or client delivery.
---

# Dealix Trust and Outbound Safety OS

## When to use

Use this skill when the user asks to:

- enable or review outbound email, WhatsApp, LinkedIn, SMS, phone, or website form actions
- check if Dealix can send externally
- review claims, pricing, ROI, testimonials, or case studies
- build policy gates for client communications
- prepare compliance or trust documentation
- verify no-auto-send defaults
- protect client data and sensitive information

## Non-negotiable defaults

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

Do not change these defaults unless the user explicitly asks for controlled-live mode and the repo already has proper gates.

## Safety doctrine

Dealix can prepare actions. Dealix must not execute sensitive external actions by default.

Allowed by default:

- drafts
- approval cards
- call scripts
- proposal briefs
- follow-up suggestions
- proof packs
- audit logs
- command room reports

Blocked by default:

- live WhatsApp send
- live cold email send
- live SMS
- auto LinkedIn DM
- robocalls
- website form spam
- signing contracts
- final pricing commitments
- guaranteed ROI claims

## Files to inspect first

```text
.env.example
.env.production.example
docs/ops/
app/outbound/
app/commercial/
scripts/outbound/
scripts/commercial/
scripts/ops/
reports/commercial/
reports/go_live/
tests/*outbound*
tests/*safety*
tests/*channel*
tests/*policy*
```

## Required gates

### Email

Require external send enabled, email send enabled, approved message, verified target, opt-out language, suppression list check, rate limit, and audit event.

### WhatsApp

Require opt-in proof, approved template for outbound initiation, stop keywords, human escalation path, rate limit, audit event, and channel-specific approval.

### LinkedIn

Allow manual task only. Never automate connection requests, DMs, scraping, or fake engagement.

### Phone

Allow call task only. Never robocall.

### Website form

Allow manual task only. Never automate bulk form submissions.

## Claims guardrails

Block or rewrite:

- guaranteed revenue
- guaranteed ROI
- fake client names
- fake testimonials
- fake logos
- claims of official partnership without proof
- unverifiable market domination language
- deceptive urgency
- hidden automation identity

Preferred wording:

- "designed to help"
- "can reduce manual follow-up work"
- "draft-first workflow"
- "manual review before external send"
- "operational proof report"
- "pilot before scale"

## Validation commands

```bash
python scripts/outbound/check_live_outbound_env.py || true
python scripts/verify_no_auto_external_send.py || true
python scripts/verify_company_launch_ready.py || true
python -m pytest -q tests/*outbound* tests/*safety* tests/*channel* 2>/dev/null || true
grep -Rni "guaranteed revenue\|guaranteed ROI\|fake testimonial" docs sales business app scripts || true
```

## Review report

A complete trust review must state:

```text
Outbound mode:
Live sends enabled:
Email status:
WhatsApp status:
LinkedIn status:
SMS status:
Approval cards present:
Opt-out present:
Suppression list present:
Fake claims found:
Sensitive data risk:
Decision:
```

## Definition of done

The repo is safe when live outbound is off by default, every external action requires approval, every target requires source or verification, opt-out exists for commercial email, WhatsApp requires opt-in/template logic, LinkedIn is manual only, logs distinguish prepared actions from sent actions, and no fake proof exists.

## Final response format

```text
Trust and Outbound Safety Status:
- outbound mode:
- live sends:
- policy gates:
- risky claims:
- files changed:
- tests/commands:
- decision:
```
