# Dealix Commercial OS Rules

## Offer ladder

**Only two offers are commercially active.** Canonical sources of truth:

- `docs/DEALIX_BUSINESS_MODEL.md` for the founder-governed commercial model;
- `auto_client_acquisition/service_catalog/registry.py` for executable offer status;
- `landing/assets/data/services-catalog.json` as the synchronized committed export.

Everything else in the catalog is `internal_experiment` and must not be sold or publicly priced without a separate approved decision.

| # | Offer | Price | `commercial_status` |
|---|-------|-------|---|
| 1 | Free Mini Diagnostic | Free | `free_entry` |
| 2 | Revenue Command Pilot — 30 days | Quote after discovery; no public fixed price | `quote_only` |

## Positioning

Dealix is a Saudi Revenue Command OS delivered first as a concierge-assisted operating service. It overlays the client's existing CRM, ERP, email, WhatsApp, spreadsheets, and reporting; it is not a CRM replacement, generic chatbot, blind automation agency, or self-serve SaaS at this stage.

Primary paid entry: **Revenue Command Pilot — 30 days**. Discovery-first; price, scope, data boundary, approvals, acceptance criteria, and remedy terms are defined in a documented quote after discovery. Never state a fixed public price.

## First-five ICP

Focus on Saudi B2B SaaS and business-service companies with approximately 20–200 employees, direct founder/GM access, a specific revenue-operations pain, usable lawful data, and willingness to run a measured 30-day pilot.

Defer banks, government, heavily regulated enterprise transformation, anonymous mass outbound, and customers requesting guaranteed revenue until repeatable proof exists.

## Language rules

- Business/sales docs: Arabic (AR) by default.
- Technical docs, code, commit messages: English.
- PR titles and CI output: English.

## Claim rules — NON-NEGOTIABLE

- No fake testimonials, client names, logos, revenue, or case studies.
- No guaranteed ROI or guaranteed sales claims.
- A proposal is not an invoice; an invoice is not revenue; revenue requires payment evidence.
- Use hypothesis and measurement language:
  - "نتوقع" / "we expect"
  - "الهدف هو" / "the goal is"
  - "سنقيس" / "we will measure"
  - NOT "مضمون" / NOT "guaranteed"

## Sales assets location

```
sales/ONE_PAGE_OFFER_AR.md
sales/CEO_INTRO_MESSAGE_AR.md
sales/DISCOVERY_SCRIPT_AR.md
sales/OBJECTION_HANDLING_AR.md
sales/FOLLOW_UP_SEQUENCE_AR.md
sales/PROPOSAL_TEMPLATE_AR.md
sales/FIRST_10_CLIENTS_PLAYBOOK_AR.md
sales/DAILY_FOUNDER_SELLING_ROUTINE_AR.md
```

## Approval required before

- Sending any external message (WhatsApp, email, LinkedIn DM)
- Issuing or sending any proposal, quote, invoice, or contract
- Enabling any live outbound channel
- Charging any customer or recording revenue
- Publishing a case study or customer claim

## Draft generation is always allowed

Generating WhatsApp drafts, email drafts, proposal briefs, follow-up sequences, pilot scopes, proof packs, and approval cards is safe and encouraged. The founder reviews and approves before any external action.
