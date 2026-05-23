# Market Domination Intelligence

**Owner:** Founder + Strategy Office
**Source of truth:** This doc + `docs/intelligence/`

## Purpose

This doc is the top-level frame for how Dealix builds and uses market intelligence. "Market domination" is not a marketing claim — it is the discipline of knowing each sector, each ICP, each buyer, and each trigger event well enough to deploy a Sprint that produces evidence within 14-21 days.

Intelligence at Dealix is operational, not academic. Every intelligence artifact must change a decision.

## The intelligence stack

| Layer | What it answers | Source doc |
|---|---|---|
| Sector ranking | Which sectors do we focus on next? | `SECTOR_RANKING_SYSTEM.md` |
| ICP segmentation | Within a sector, which company profiles? | `ICP_SEGMENTATION_SYSTEM.md` |
| Buyer persona | Within an ICP, who do we engage? | `BUYER_PERSONA_SYSTEM.md` |
| Competitive intelligence | Who else is selling to this buyer? | `COMPETITIVE_INTELLIGENCE_SYSTEM.md` |
| Trigger events | What signals an open window? | `TRIGGER_EVENT_SYSTEM.md` |
| Account scoring | Which named accounts now? | `ACCOUNT_SCORING_MODEL.md` |
| Offer-channel fit | Which sprint, which channel? | `OFFER_CHANNEL_FIT_SYSTEM.md` |
| Saudi market map | Where does each sector sit overall? | `SAUDI_B2B_MARKET_MAP.md` |

Each lower layer depends on the layer above. Account scoring without ICP segmentation produces noise. Trigger events without buyer persona produce mistimed outreach.

## Operating rhythm

| Rhythm | Cadence | Output |
|---|---|---|
| Sector review | Quarterly | Updated sector rankings, sector entry/exit decisions |
| ICP review | Monthly | Refined ICP definitions per active sector |
| Buyer persona review | Monthly | Updated persona pain-and-language notes |
| Trigger event scan | Weekly | List of triggered accounts entering account scoring |
| Account scoring run | Weekly | Updated tier list (A / B / C / Out) |
| Offer-channel calibration | Per sprint | Updated routing rules |

The rhythm is not aspirational. Missed cycles invalidate downstream sprint targeting.

## Intelligence governance

- All intelligence artifacts cite source and date.
- Aggregated patterns only. No PII in published artifacts.
- Customer-specific intelligence is treated as customer-confidential and lives in the customer's project folder, not in shared intelligence docs.
- Sector reports for public publication follow `docs/brand/DEALIX_REPORT_TEMPLATE_GUIDE.md`.

## What this stack does NOT do

- It does not generate guaranteed leads.
- It does not predict customer purchase decisions.
- It does not replace the founder's judgment on engagement fit.
- It does not scrape, harvest, or repurpose any data that violates source-platform terms.

## Trust gate

| Artifact | Approval class | Approver |
|---|---|---|
| Internal intelligence note | A0 | Self |
| Sector rank update | A1 | Strategy Office |
| Sector report (external) | A3 | Founder |
| Account tier change for an active prospect | A2 | Founder + Operator |

## Failure mode

- Intelligence artifacts pile up without changing sprint decisions.
- A sector report leaks identifying detail.
- Account scoring drifts from documented rules; targeting becomes arbitrary.

## Recovery path

1. Re-run the offending layer with the documented rules.
2. Pull and re-issue any leaked artifact.
3. Re-anchor weekly intelligence rhythm in the founder's calendar.

## Cross-links

- Sector ranking: `docs/intelligence/SECTOR_RANKING_SYSTEM.md`
- ICP segmentation: `docs/intelligence/ICP_SEGMENTATION_SYSTEM.md`
- Buyer persona: `docs/intelligence/BUYER_PERSONA_SYSTEM.md`
- Competitive intel: `docs/intelligence/COMPETITIVE_INTELLIGENCE_SYSTEM.md`
- Trigger events: `docs/intelligence/TRIGGER_EVENT_SYSTEM.md`
- Account scoring: `docs/intelligence/ACCOUNT_SCORING_MODEL.md`
- Offer-channel fit: `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md`
- Saudi market map: `docs/intelligence/SAUDI_B2B_MARKET_MAP.md`

## Disclaimer

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة. Dealix does not guarantee revenue, meetings, or conversion outcomes.
