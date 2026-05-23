# Content to Demand Engine

**Owner:** Founder + Content Lead
**Source of truth:** This doc + `docs/growth/CONTENT_ENGINE.md` + `docs/growth/CONTENT_CALENDAR_MONTH_1.md`

## Purpose

The Content to Demand Engine produces and distributes Dealix's public content — sector signals, founder principles, sprint recaps, sector scorecards — and routes resulting engagement into the Distribution War Machine. Content is the inbound counterpart to outbound: it lets the right buyers find Dealix without Dealix reaching out first.

The engine is opinion-led, not topical. It produces fewer pieces than competitors, each carrying a position only Dealix can defend.

## Inputs

- **Content calendar** — see `docs/growth/CONTENT_CALENDAR_MONTH_1.md`.
- **Sector intelligence** — from `docs/intelligence/SAUDI_B2B_MARKET_MAP.md` and sector scorecards.
- **Proof Pack distillations** — from the Proof to Demand Machine.
- **Founder principle log** — operating principles the Founder has formalized that quarter.
- **Active sector content backlog** — pieces drafted and awaiting publication.

## Outputs

| Content type | Cadence | Format |
|---|---|---|
| Founder principle post | 1 per week | LinkedIn long-form, 600-900 chars |
| Sector signal post | 1 per week | LinkedIn long-form + Arabic parallel |
| Sprint recap post | 1 per week | LinkedIn long-form |
| Proof brief | 2 per month | LinkedIn long-form referencing case-safe summary |
| Sector scorecard | 1 per quarter per active sector | Long-form report (`docs/sector-reports/`) |
| Open question | 1 per month | LinkedIn invitation post |

Plus:

- **LinkedIn carousel** — 1 per month, repackaging a recurring theme.
- **Founder podcast/interview clip** — opportunistic, when relevant.

## Source of truth

This doc + `docs/growth/CONTENT_ENGINE.md` + the content calendar.

## Approval class

- **A1** — Internal publication (newsletter to opted-in list).
- **A2** — LinkedIn posts (Founder voice; Brand Lead reviews for voice checklist).
- **A3** — Sector scorecards and any public-facing report (Founder only).

## Trust gate

- Every claim cites source and date.
- Every aggregated stat passes the methodology check.
- Every anonymized reference passes the deanonymization audit.
- Bilingual posts are parallel (per `DEALIX_BRAND_VOICE.md`).
- No banned phrases (per `DEALIX_BRAND_VOICE.md`).
- No customer name without written authorization.

## Owner

- **Code owner:** Operations Engineering (scheduling, queue).
- **Operational owner:** Founder + Content Lead.

## Worker script (placeholder)

`workers/content_to_demand_worker.py` (planned). Manages content calendar, drafts assembly, scheduling, engagement tracking.

## KPI

| Metric | Target |
|---|---|
| Calendar adherence | >= 90 percent of scheduled posts shipped |
| Voice checklist pass (first try) | >= 95 percent |
| Inbound from content (Contact Form attribution) | observed |
| Engagement-to-Diagnostic-call conversion | observed |
| Sector scorecard publication cadence | 1 per quarter per active sector |

## Distribution routing

When a content piece is published, the Content to Demand Engine routes downstream:

- **Nurture Machine** — references the piece in next nurture touches.
- **ABM Strategic Account Machine** — uses sector-specific pieces as land-and-expand assets.
- **Outbound Draft Machine** — drafts can cite the piece as warm-context.
- **Reply Router** — incoming Contact Form submissions citing the piece are tagged for high-fit routing.

## Failure mode

- Calendar drifts; posts go cold for weeks.
- A post claims a result without source.
- Content drifts into commodity productivity tips.
- Sector scorecard publishes without methodology section.

## Recovery path

1. Re-anchor calendar.
2. Re-source every published number.
3. Re-anchor content to Dealix's defensible positions.
4. Restore methodology section before re-publication.

## What this engine does NOT do

- It does not engage in engagement-bait posting.
- It does not auto-comment on competitor posts.
- It does not buy followers, likes, or comments.
- It does not publish unsourced claims.

## Cross-links

- Content engine: `docs/growth/CONTENT_ENGINE.md`
- Content calendar: `docs/growth/CONTENT_CALENDAR_MONTH_1.md`
- Social media kit: `docs/brand/DEALIX_SOCIAL_MEDIA_KIT.md`
- Proof to Demand Machine: `docs/growth/PROOF_TO_DEMAND_MACHINE.md`

## Disclaimer

Dealix does not guarantee inbound demand from content publication. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
