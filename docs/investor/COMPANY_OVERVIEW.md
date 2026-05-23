# Company Overview — One-Pager — نظرة عامة على الشركة

## Purpose
A single-page company overview used in investor and partner conversations. Evidence-backed, free of hype. Replaces a marketing deck when the conversation calls for substance.

## Owner
Founder. Reviewed quarterly.

## Inputs
- Operating model from `docs/founder/CEO_OPERATING_MODEL.md`.
- Proof gates from `docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md`.
- Case studies from `docs/case-studies/`.
- Sector reports from `docs/sector-reports/`.

## Outputs
- This document.
- PDF export to `data-room/00_overview/02_one-pager.pdf` quarterly.

## The One-Pager Content

### Identity
- **Name**: Dealix
- **What we do**: We run AI-supported commercial sprints for Saudi B2B operators. Each sprint produces a verified outcome and an internal asset the client owns.
- **Where**: Riyadh, KSA. Bilingual operating language (Arabic primary, English parallel).
- **Stage**: Pre-Series A; revenue-funded; proof-gate driven.

### What We Sell (Today)
- **Commercial Sprint** — a fixed-scope engagement with defined outcomes, weekly reports, kill criteria, and a verified close-out.
- **Sector Report** — quarterly, methodology-disclosed, sector-specific.
- **Specialist Engagement** — bespoke advisory tied to one named outcome.

### What We Do Not Sell
- No outbound automation. No cold WhatsApp. No LinkedIn bots. No scraping.
- No guarantees of sales numbers or conversion rates.
- No multi-tenant SaaS product (yet — see `docs/product/SAAS_CANDIDATE_RULES.md`).

### Who We Serve
- Saudi B2B founders and commercial leaders (revenue 5-50m SAR/year).
- Sectors of current focus: [listed quarterly in `docs/01_go_to_market/`].

### Proof Status (As of [date])
- Proof of Interest: [status, evidence link].
- Proof of Conversion: [status, evidence link].
- Proof of Delivery: [status, evidence link].
- Proof of Retention: [status, evidence link].

### Operating Principles
- Evidence over hype. A3 before action. Kill criteria on every commitment.
- One accountability per role. No silent delegation of strategic decisions.
- PDPL-first. AI workflows logged with provenance.

### Disclosure
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة

## Rules
1. No claim on this page without an evidence link in the data room.
2. No client name without written approval.
3. No projected revenue stated as fact.
4. Updated quarterly; never older than 90 days when shared.
5. Bilingual: AR + EN parallel structure.

## Metrics
- Sharing log: who received it, when, with what watermark.
- Update freshness (≤ 90 days).

## Cadence
- Quarterly refresh.

## Evidence
- `evidence/investor/overview/<YYYY-Qn>.md` per revision.

## Verifier
Founder.

## Runtime Command
`make company-overview` — regenerates the PDF, refuses to publish without proof-gate evidence links.

## Arabic Summary — ملخص عربي
صفحة واحدة عن الشركة: ما نبيع، ما نرفض بيعه، حالة بوابات الإثبات، مبادئ التشغيل. لا ادعاءات بلا أدلة، لا أسماء عملاء بلا موافقة. القيم التقديرية ليست مُتحقَّقة.
