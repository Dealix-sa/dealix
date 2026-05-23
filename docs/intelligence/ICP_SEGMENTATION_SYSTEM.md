# ICP Segmentation System

Saudi B2B is not one market. It is a stack of overlapping verticals where
the same company name can be three different buyers depending on the
business unit and the regulator. This document defines how Dealix segments
the ideal customer profile (ICP) inside each ranked sector.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Why ICPs are layered

A "company list" is a starting point, not a target. Two companies with the
same revenue and the same sector can have completely different buying
behaviour because of:

- Procurement maturity (open list vs. vendor master).
- Decision authority (CEO vs. business unit head).
- Data sensitivity (regulated workload vs. open data).
- Local presence (KSA HQ vs. regional office).
- Saudisation profile and operating language.

Segmenting by these layers, rather than just by sector, is what stops the
team from running a one-shape outreach motion against a many-shape market.

## 2. ICP structure

Every ICP entry has the following fields:

- `icp_id` — slug.
- `sector_id` — references `growth/sector_targets.csv`.
- `name` — human label.
- `tier` — T1, T2, T3 (see section 4).
- `firmographics` — revenue band, employees band, locations.
- `operating_signals` — what the company looks like operationally (e.g.
  "has a named CRO", "uses HubSpot or Salesforce", "publishes RFPs").
- `buying_signals` — recent activity that suggests buying intent.
- `authority_map` — who decides, who signs, who blocks.
- `pain_anchors` — specific, dated, costly pains the offer can address.
- `proof_required` — what kind of proof this ICP will trust (logos,
  sector references, pilot output, third-party audit).
- `channels` — which channels Dealix uses (warm intro, founder content,
  partner referral, structured email/LinkedIn). Channel selection is
  bounded by `OFFER_CHANNEL_FIT_SYSTEM.md`.
- `disqualifiers` — explicit list (see section 5).
- `notes`

## 3. ICP segmentation procedure

1. Start with sectors at tier "active" in `growth/sector_targets.csv`.
2. For each sector, draft up to 3 ICPs that meet the structure above.
3. Validate each ICP with at least one named buyer conversation or one
   partner conversation; record the source.
4. Score the ICP against tier criteria (section 4).
5. Write to `growth/icp_segments.csv`.
6. Re-validate every 90 days or when an ICP underperforms.

## 4. ICP tiers

- T1 — High-fit, named buyer reachable, named pain anchor with a date, at
  least one warm path or partner path. Goes into proactive Distribution War
  Machine rotation.
- T2 — High-fit but no warm path yet. Goes into Content-to-Demand
  rotation; partner backlog if applicable.
- T3 — Plausible fit, but data is thin. Goes into Watchlist and Market
  Research Protocol queues.

Tier movement is logged in `growth/icp_segments_delta.md`. Promotion
requires a named source. Demotion requires a date.

## 5. Disqualifiers

An account is disqualified, regardless of sector ranking, if any of the
following is true:

- The buyer is on the suppression list (`outreach/suppression.csv`).
- The account has explicitly opted out at any prior step.
- Engagement requires guaranteed-revenue/guaranteed-meeting language.
- The required outreach channel is one Dealix does not operate (e.g. cold
  WhatsApp without prior consent, mass SMS, paid scrape lists).
- Delivery would require capability Dealix has not yet productised and
  cannot ship a sample for within 30 days.
- The data risk profile (e.g. regulated, classified) is beyond the
  Trust Guardian's current posture.
- The account is in active legal or financial dispute with Dealix or a
  Dealix partner.

Disqualifiers are recorded with reason and date. Disqualified accounts are
not re-queued without an explicit override and a new attribution.

## 6. CSV output schema

`growth/icp_segments.csv` columns:

- `icp_id`
- `sector_id`
- `name`
- `tier`
- `firmographics_revenue_band`
- `firmographics_employees_band`
- `locations`
- `authority_map`
- `pain_anchors`
- `proof_required`
- `channels`
- `disqualifiers`
- `source_refs`
- `last_validated_at`
- `validated_by`

## 7. Saudi-specific patterns

The ICP layer accounts for patterns that generic CRM templates miss:

- Decision authority often sits with founder or chairman; the title
  matters less than the relationship.
- Procurement can be slow but final; verbal yes is not a deal.
- Bilingual operating reality: Arabic and English coexist; ICP entries
  declare which is the dominant operating language.
- Regulator exposure differs by sector; some sectors require explicit
  data-residency proof before a sample is even discussed.
- Partner-introduced accounts move faster than direct ones; the ICP
  layer flags which ICPs have realistic partner paths.

## 8. Cadence

| Cadence | Activity |
|---|---|
| Weekly | Add new ICPs from sector triggers |
| Monthly | Re-validate T1 ICPs; review T2 promotion candidates |
| Quarterly | Cull T3 ICPs that have not advanced |

## 9. Owners and approval

- Owner: Growth Strategist.
- Approver: Founder Console for tier changes and disqualifier additions.
- Auditor: Trust Guardian.

## 10. Failure modes and recovery

| Failure | Symptom | Recovery |
|---|---|---|
| ICP under-converts | Proposal-win rate < band | Re-validate ICP; downgrade tier |
| Disqualifier ignored | Suppressed buyer queued | Trust Guardian blocks; re-train pipeline |
| ICP drift | T1 accounts not engaging | Re-interview buyers; refresh pain anchors |
| Source aging | Validation > 90 days old | Force re-validation; move to T3 if stale |
| Over-segmentation | More than 3 ICPs per sector | Consolidate; merge by authority map |

## 11. Non-negotiables

- No "guaranteed" language ever appears in ICP narratives.
- No external action originates here. The ICP feeds the Distribution War
  Machine, which terminates at an approval queue.
- A3 approval class is banned.

The ICP is not a buyer persona, and not a target list. It is the rule that
decides who gets included or excluded before either of those tools runs.
