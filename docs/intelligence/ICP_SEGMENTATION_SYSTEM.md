# ICP Segmentation System

**Owner:** Strategy Office + Founder
**Source of truth:** This doc + `docs/intelligence/SECTOR_RANKING_SYSTEM.md`

## Purpose

The Ideal Customer Profile (ICP) defines who Dealix engages within a sector. Without an explicit ICP, sprint targeting drifts into adjacent companies that look similar but do not convert.

## ICP definition rubric

Every ICP entry must specify:

| Field | Example |
|---|---|
| Sector | Cybersecurity B2B |
| Company size band | 10-80 FTEs |
| Annual revenue band | SAR 3M-50M |
| Geography | Riyadh / Jeddah / Eastern Province |
| Sales motion | Founder-led or Head-of-Sales-led; outbound + referral |
| Tech maturity | CRM in use OR explicit CRM-less stage with intent to formalize |
| Deal size band | SAR 80,000-800,000 ACV |
| Decision speed | 4-12 weeks discovery to close |
| Pain pattern | Scattered deal flow, ungoverned outbound, no Proof loop |
| Trust posture | Audit-conscious; rejects black-box agencies |

## ICP segments (illustrative — refresh per quarter)

### Segment 1 — Founder-led B2B services (5-50 FTE)

The core Dealix ICP at launch stage.

- Sector relevance: cybersecurity, ERP/CRM consulting, B2B agencies, boutique consulting.
- Buyer: founder.
- Sprint fit: Lead Intelligence Sprint, AI Quick Win Sprint, Proof Pack Sprint.
- Price band: SAR 9,500-25,000 per sprint.
- Cycle: 2-4 weeks discovery to first sprint signed.

### Segment 2 — Head-of-Sales-led B2B (50-200 FTE)

The second wave once Segment 1 produces a steady Proof Pack flow.

- Sector relevance: enterprise logistics, regional B2B SaaS, enterprise services.
- Buyer: Head of Sales, with Founder sign-off on contract.
- Sprint fit: Sector Map Sprint, Trigger Activation Sprint, Retainer Onboarding Sprint.
- Price band: SAR 25,000-75,000 per sprint or SAR 35,000+ per month retainer.
- Cycle: 6-12 weeks discovery to first sprint signed.

### Segment 3 — Head-of-GTM-led regional SaaS expanding into KSA

The expansion wave for companies that are not Saudi-native but are committing to KSA market entry.

- Sector relevance: B2B SaaS, vertical SaaS, AI-tool vendors.
- Buyer: Head of GTM or VP Sales (regional), with KSA Country Manager sign-off on operating commitments.
- Sprint fit: KSA Entry Sprint, Sector Scorecard Sprint, Partner Activation Sprint.
- Price band: SAR 35,000-120,000 per sprint or SAR 50,000+ per month retainer.
- Cycle: 8-16 weeks discovery to first sprint signed.

## Out-of-ICP (must not engage)

- B2C companies of any sector.
- Companies that explicitly require guaranteed leads or guaranteed meetings.
- Companies that require scraping, WhatsApp automation, or unapproved bulk cold outreach.
- Companies that refuse founder-approval gating as an operating commitment.
- Companies under SAR 2M revenue if they cannot fund a 9,500 SAR sprint without strain.
- Companies above SAR 500M revenue at first contact (enterprise procurement cycle is incompatible with sprint velocity unless a sponsoring executive shortens it).

## ICP scoring

Each candidate account is scored against the active ICP definition. See `ACCOUNT_SCORING_MODEL.md` for the 0-100 scoring rubric.

ICP fit is a precondition for tier-A account placement. An account that scores high on triggers but fails ICP is parked, not pursued.

## ICP evolution

ICP is a living artifact. It evolves as Dealix learns.

- Monthly: review ICP fit for closed-won and closed-lost sprints. If a closed-lost cluster shares a trait, the ICP excludes that trait next iteration.
- Quarterly: publish the updated ICP definition per active sector.
- Each iteration carries a version stamp (e.g., `Cybersecurity ICP v3 — 2026-Q1`).

## ICP and sprint catalog mapping

| ICP segment | Default first sprint | Default upgrade path |
|---|---|---|
| Segment 1 | Lead Intelligence Sprint | AI Quick Win Sprint → Retainer |
| Segment 2 | Sector Map Sprint | Trigger Activation Sprint → Retainer |
| Segment 3 | KSA Entry Sprint | Partner Activation Sprint → Retainer |

## Trust gate

| Action | Approval class |
|---|---|
| ICP definition update | A1 — Strategy Office |
| ICP segment add or remove | A2 — Founder + Strategy Office |
| Public ICP publication | A3 — Founder |

## Failure mode

- ICP becomes a wishlist; targeting drifts back to "anyone who picks up the phone."
- Closed-lost patterns are not fed back into ICP exclusion.
- Three sprints in a row fail because the buyer was out-of-ICP and the operator ignored the signal.

## Recovery path

1. Pull the last 10 closed-lost sprints; cluster the disqualifying patterns; add to ICP exclusions.
2. Re-run account scoring with the updated ICP.
3. Re-train operators on the disqualification calls.

## Disclaimer

ICP is directional, not predictive. Dealix does not guarantee revenue from any ICP segment. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
