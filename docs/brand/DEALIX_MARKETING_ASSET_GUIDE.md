# Dealix Marketing Asset Guide

How to produce a branded artifact in under 10 minutes.

## 1. Asset families

| Family | Source | Output |
|---|---|---|
| Landing hero | `apps/web/components/brand/` | Live page |
| Founder console page | `apps/web/components/brand/` + page route | Live page |
| Proposal cover | `assets/brand/logo/dealix-logo-full.svg` + Inter | PDF |
| Sales deck | `assets/brand/logo/` + brand tokens palette | PPTX |
| Social card (OG) | `assets/brand/social/dealix-social-card.svg` | 1200×630 PNG |
| LinkedIn banner | derived from social card, 1584×396 | PNG |
| Email signature | wordmark + tagline, 320 px wide | PNG / HTML |
| Case study | full signature on cover, deep navy body | PDF |
| Invoice / report | wordmark + ZATCA fields | PDF |

## 2. Asset checklist

Every outgoing artifact must:

- [ ] Use one of the approved brand colour tokens, never a one-off hex.
- [ ] Use Inter (Latin) and IBM Plex Sans Arabic (Arabic) only.
- [ ] Contain the wordmark or full signature at the documented minimum size.
- [ ] Pass the **banned claim** regex check (`scripts/verify_brand_system.py`).
- [ ] Be labelled `Drafted by Dealix — for founder approval` if it is
      an outbound draft (proposal, email, LinkedIn message).
- [ ] Be filed in the matching ledger (proof, proposal, outbound queue).

## 3. Social cadence

The social card is parameterized — swap only the eyebrow
("Sector report · Logistics") and the headline. The mark and tagline
stay locked.

## 4. Banned in marketing assets

- ❌ "Guaranteed revenue", "guaranteed leads", "guaranteed ROI".
- ❌ "Fully autonomous outbound", "set-and-forget growth".
- ❌ Unauthorized logos of customers in case studies.
- ❌ Photography of real customer dashboards without redaction.
- ❌ Pricing in marketing assets without referencing
  `docs/product/PRICING_GUARDRAILS.md`.

## 5. Distribution

Drafts produced by the Distribution machines go to the **Approval
Queue**, not to LinkedIn / email / WhatsApp directly. Only after a
founder approval can the asset move to the outbox.
