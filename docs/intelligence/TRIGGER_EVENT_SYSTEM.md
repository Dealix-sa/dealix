# Trigger Event System

A trigger event is a dated, attributable change at a target account that
moves it from "interesting in theory" to "ready in time." This document
defines which triggers Dealix tracks, where they are sourced from, how they
expire, and how they enter the account scoring model.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Why triggers matter

A static "fit" score tells the team an account is worth thinking about; a
trigger tells the team when. In Saudi B2B, where decision cycles can stall
without a forcing function, triggers do a disproportionate amount of work.
Without a trigger, an account stays in the watch pile. With a trigger, it
enters the proactive Distribution War Machine rotation for a bounded
window.

## 2. Trigger catalogue

Each trigger has:

- `trigger_id` — slug.
- `name`.
- `category` — funding | hiring | product | expansion | regulatory |
  partnership | leadership | distress.
- `signal_source` — where we hear about it (named).
- `expected_pain` — what business pain typically follows.
- `dealix_offer_fit` — which offer in the ladder this trigger maps to.
- `half_life_days` — how long the trigger remains hot.
- `evidence_required` — minimum to record the trigger.
- `notes`.

### 2.1 Funding triggers

- Seed / Series A / Series B announcement (pain: hire revenue function,
  build go-to-market).
- Local government grant or program acceptance (pain: spend deployment
  with reporting).
- Strategic investor round (pain: governance and reporting maturity).

Half-life: 60 days. Evidence required: named source (founder post,
official announcement, sector report).

### 2.2 Hiring triggers

- New Head of Sales / CRO (pain: rebuild pipeline within 6 months).
- New Head of Marketing (pain: prove pipeline contribution fast).
- New Head of Revenue Operations (pain: revenue tech stack consolidation).
- New COO (pain: operating playbooks and audit posture).
- New CTO (pain: vendor portfolio and AI governance).

Half-life: 90 days. Evidence required: public profile change with date.

### 2.3 Product triggers

- New B2B product launch.
- Pricing / packaging change announced publicly.
- New tier or enterprise tier launched.

Half-life: 45 days. Evidence required: named announcement.

### 2.4 Expansion triggers

- Expansion to KSA from another GCC market or international.
- New office or HQ in Saudi.
- New industry vertical entered by the account.

Half-life: 120 days. Evidence required: official source.

### 2.5 Regulatory triggers

- New regulator requirement applicable to the sector (e.g. PDPL, ZATCA,
  sector-specific licensing).
- Audit finding made public.
- Saudisation threshold change for the sector.

Half-life: 60 days. Evidence required: regulator publication.

### 2.6 Partnership triggers

- Account announces a strategic partnership relevant to revenue or
  delivery.
- Account joins a sector consortium.

Half-life: 60 days. Evidence required: named announcement.

### 2.7 Leadership triggers

- CEO change.
- Board change.
- Public commitment to a growth or efficiency target with a date.

Half-life: 90 days. Evidence required: named source with date.

### 2.8 Distress triggers (handled with extra care)

- Layoff announcement.
- Loss of a major customer.
- Public regulatory finding.

Half-life: 45 days. Evidence required: named, factual source. Distress
triggers do NOT generate outreach drafts that exploit the situation; they
flag a need for sensitivity and may suppress outreach for a defined period.

## 3. Source rules

Allowed:
- Founder content on Dealix-owned channels.
- Public funding databases with named publication date.
- Official company posts or press releases.
- Regulator publications.
- Partner-introduced signals with named introducer.

Banned:
- Scraping personal pages without consent.
- Buying lists of "trigger feeds" without source attribution.
- Triggers without a date or an attributable source.
- Inference-only triggers (e.g. "must be hiring because they grew").

## 4. CSV output schema

`growth/trigger_events.csv`:

- `trigger_id`
- `account_id`
- `category`
- `name`
- `observed_at`
- `half_life_days`
- `expires_at`
- `source_ref`
- `evidence_ok` — true | false (Trust Guardian)
- `offer_fit_id`
- `recorded_by`
- `notes`

A trigger is excluded from account scoring if `evidence_ok = false` or
`now >= expires_at`.

## 5. Scoring integration

Triggers feed the Account Scoring Model as the "recency" feature with the
following bonus structure:

- 0–14 days since `observed_at`: +1.0
- 15–45 days: +0.6
- 46–90 days: +0.3
- 91+ days: 0 (drops off, regardless of category half-life)

Distress triggers do not add a score; they set a flag in the trust ledger
that may dampen outreach intensity.

## 6. Cadence

| Cadence | Activity |
|---|---|
| Daily | Trigger scan from sanctioned sources |
| Weekly | Trigger audit; re-check evidence |
| Monthly | Catalogue review; add or retire trigger types |

## 7. Saudi-specific overlays

- Funding triggers in Saudi often coincide with public-program timelines;
  the system tags the program when known.
- Leadership announcements may not appear on LinkedIn first; Arabic
  press and sector publications are explicit allowed sources.
- Distress triggers in Saudi require extra sensitivity due to relationship
  density; outreach intensity is reduced.

## 8. Owners and approval

- Owner: Growth Strategist.
- Auditor: Trust Guardian (evidence + sensitivity).
- Consumer: Distribution Operator (uses trigger-bound accounts only).

## 9. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Trigger with no source | Quarantine; do not score |
| Stale trigger fires repeatedly | Half-life enforced; trigger expires |
| Distress trigger exploited in copy | Brand Guardian blocks; trust entry |
| Trigger flood from one source | Source rate-limited; secondary source required |
| Trigger contradicts another | Both held until corroborated |

## 10. Non-negotiables

- No "guaranteed" language ever appears in a trigger-driven draft.
- A trigger is never the only justification for outreach — ICP + persona
  + trigger together drive a draft.
- A3 approval class is not used.

Triggers tell us when. ICPs tell us who. Personas tell us how to write.
The combination is what makes outreach feel like a thoughtful business
introduction rather than a templated push.
