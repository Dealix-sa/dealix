# Competitive Intelligence System

Dealix is positioned against a crowded landscape of scraping tools, spam
tools, generic CRM, and agency offers. Operators and buyers compare us to
those alternatives — sometimes directly, often implicitly. This document
defines how we track competitors without doing anything we would not want
done to us.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Why this layer exists

A clean view of the alternative landscape is necessary because:

- The buyer's objection set borrows directly from previous tools they
  tried.
- Channel saturation has changed: cold scraping is increasingly burned;
  spam tools degrade domain reputation; generic CRM produces revenue
  theatre, not revenue.
- Agencies vary wildly; some are partners, some are competitors.
- Saudi-specific compliance and trust signals favour transparent vendors.

This system gives the team a current, dated view of where each alternative
sits and how Dealix is differentiated. It feeds the Objection Library, the
Outreach Draft Machine, and the Proof factory.

## 2. Categories tracked

1. Scraping tools — bulk export / list builders / contact enrichment.
2. Spam tools — high-volume cold email automations with weak deliverability
   posture.
3. Generic CRM — Salesforce, HubSpot, Zoho, Pipedrive used as a system of
   record but not as a system of growth.
4. Agencies — outbound, content, SDR-as-a-service, growth consultancies.
5. AI-native point tools — meeting note takers, AI SDR claims, AI
   research, AI writing.
6. Internal incumbent — the buyer's existing manual or spreadsheet
   process.

For each entry we maintain:

- `competitor_id`
- `category` — one of the six above
- `name`
- `claim` — what they say they do
- `actual_outcome` — what we have observed buyers actually receive
- `pricing_band`
- `where_they_win` — honest list of strengths
- `where_we_win` — what Dealix does differently
- `buyer_objection_signals` — objection phrases that come from buyers who
  used this alternative
- `last_reviewed_at`
- `source_refs`

## 3. Signal sources (allowed)

- Buyer interviews where the buyer freely describes their previous tool
  use, with explicit recorded consent to use the content.
- Public marketing material on the competitor's own site (read, not
  redistributed).
- Public reviews and analyst notes with attribution.
- Founder content engagement signals on Dealix-owned channels.
- Partner conversations with named partners.

## 4. What we do NOT do (explicit)

- We do not scrape competitor sites, dashboards, or customer lists.
- We do not access competitor product accounts using non-Dealix
  credentials.
- We do not bait competitor demos under false names.
- We do not "test" competitor products in ways that violate their terms.
- We do not redistribute competitor content beyond fair-use citation.
- We do not record competitor calls without explicit consent.
- We do not use scraped Saudi contact lists, branded competitor lists, or
  resold lead packs.
- We do not infer "guaranteed" claims about ourselves by comparison to
  competitor failure.

If a piece of intelligence cannot be obtained inside these rules, we do
not collect it. The Trust Guardian audits this monthly.

## 5. Output schema

`growth/competitor_intel.csv` with the columns above plus:

- `category_tier` — observed | watched | reviewed
- `last_buyer_mention_at` — last date a buyer named this in a call
- `objection_library_links` — references to entries in
  `OBJECTION_LIBRARY_SYSTEM.md`

A weekly delta is appended to `growth/competitor_intel_delta.md`.

## 6. Research cadence

| Cadence | Activity |
|---|---|
| Weekly | Buyer-interview signal pass; objection trace |
| Monthly | Category review; pricing band check (public sources only) |
| Quarterly | Full review; cull dead entries; refresh win-loss notes |

## 7. How this feeds other systems

- Objection Library: each competitor entry links to the objections we
  expect from buyers exposed to it.
- Outbound Draft Machine: drafts explicitly avoid mirroring competitor
  spam patterns (subject-line tricks, fake-personalisation).
- Proof Factory: when the competitor failure pattern is well-known, the
  proof we publish anticipates it.
- Sector Ranking System: sectors saturated with competitor spam adjust
  their "outreach fit" score downward.

## 8. Saudi-specific notes

- Saudi B2B buyers have low tolerance for generic templates; brand-style
  spam reduces reply rates fast.
- Data residency, PDPL posture, and bilingual operating ability are
  meaningful differentiators we capture explicitly per competitor.
- Agency dynamics differ from typical SaaS markets — some agencies are
  partners; the system flags this with `partner_potential`.

## 9. Owners and approval

- Owner: Growth Strategist.
- Approver: Founder Console on category-tier changes.
- Auditor: Trust Guardian — verifies that no banned source is referenced.
- Reviewer: Performance Analyst — checks that competitor narrative aligns
  with actual pipeline data.

## 10. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Source cannot be re-attributed | Quarantine row; re-derive from clean source |
| Buyer evidence stale (>90 days) | Drop competitor to "watched" tier |
| Objection drift | Re-pull from last 30 days of buyer notes |
| Comparison drifts into "guarantee" | Brand Guardian rewrites; trust ledger entry |
| Competitor partners with Dealix | Move category to "partner"; out of this file |

## 11. Non-negotiables

- No competitor name is used in public Dealix material without a clear,
  factual claim and an approval entry.
- No "we guarantee what they cannot" language. Ever.
- Every claim that names a competitor carries a source reference.
- A3 is not used. Only A1 and A2 apply.

The point of competitor intelligence is not to attack alternatives. It is
to make sure Dealix offers a clearly different operating model — and to
make sure our drafts respect what buyers have already lived through.
