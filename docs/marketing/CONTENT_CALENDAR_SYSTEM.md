# Content Calendar System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Dealix content calendar is not a schedule of posts. It is a
> queue of evidence-bearing artefacts produced by named loops and
> distributed through gated channels.

This document defines the content calendar system: how the calendar
is structured, how items enter it, how they are reviewed, and how
they exit (published or declined). The Content Strategist agent
owns the calendar; the Brand Guardian agent checks it; the founder
approves it.

## Operating Principles

- The calendar is a queue, not a clock. Items move when they are
  ready, not when the day says they should.
- Every item traces to one of the three content loops (objection,
  governance, evidence).
- No item is queued for distribution without passing the
  claims-safety, brand-voice, and (where relevant) proof-safety
  evals.
- A week with three reviewed posts is preferred to a week with five
  rushed ones.
- No item promises revenue, sales, or meetings.
- No item references an unapproved customer, logo, or screenshot.

## Calendar Structure

The calendar is a single CSV (`marketing/content_calendar.csv`)
with these columns:

| Column                 | Description                                      |
|------------------------|--------------------------------------------------|
| `item_id`              | Stable id (e.g. `CC-2026-W19-001`)               |
| `loop`                 | One of `objection`, `governance`, `evidence`     |
| `channel`              | `linkedin`, `newsletter`, `blog`, `sector_report`, `short_video`, `email_template` |
| `format`               | `post`, `long_form`, `teardown`, `data_point`, `template`, `script` |
| `title`                | Working title                                    |
| `evidence_links`       | File paths to backing evidence                   |
| `claims_flags`         | Output of claims-safety eval                     |
| `brand_voice_flags`    | Output of brand-voice eval                       |
| `proof_safety_flags`   | Output of proof-safety eval (if applicable)     |
| `approval_state`       | `idea`, `draft`, `queued_for_review`, `approved`, `published`, `declined` |
| `target_date`          | Earliest possible publication date              |
| `owner`                | Content Strategist or founder                   |
| `trust_ledger_ref`     | Reference id after publication                  |

## How Items Enter the Calendar

There are five sanctioned sources:

- **Objection inbox.** A sales-call objection (or a recurring
  prospect question) is recorded by the founder or by the Sales
  Scripts loop. The Content Strategist turns it into one or more
  calendar items.
- **Governance teardown queue.** A new governance pattern (policy
  update, eval gate change, refusal-marker addition) becomes a
  teardown post.
- **Evidence digest queue.** An anonymised pattern from an active
  engagement becomes a scorecard snippet or sector report data
  point.
- **Sector research queue.** A new sector observation that crosses
  a defensibility bar becomes a sector report excerpt.
- **Founder direct ideas.** Founder-flagged ideas enter as `idea`
  state with a manual loop tag.

Items entering outside these five sources are flagged by the
Content Strategist and require a written reason before they can
progress to `draft`.

## Calendar Cadence

The default cadence is intentionally conservative:

- **LinkedIn:** five posts per week, Sunday through Thursday, with
  a hard quality gate; missed days are not back-filled.
- **Newsletter:** weekly, on a fixed day. Missed weeks are
  acknowledged in the next issue and not back-filled.
- **Sector reports:** quarterly, with named contributors only after
  approval.
- **Blog / long-form:** monthly minimum, more if a governance or
  evidence pattern warrants it.
- **Short video:** one per week tied to the LinkedIn loop.
- **Email templates:** updated when the objection loop surfaces a
  new pattern.

The calendar is not optimised for posting volume. It is optimised
for evidence ratio: the percentage of items that carry traceable
evidence beyond opinion.

## Weekly Operating Rhythm

| Day      | Action                                                                 |
|----------|------------------------------------------------------------------------|
| Sunday   | Calendar review: items at `idea` are triaged; items at `draft` move forward. |
| Monday   | Drafts written; evals run; items move to `queued_for_review`.         |
| Tuesday  | Founder review window. Approved items move to `approved`.             |
| Wed–Thu  | Manual publication of approved items per channel.                     |
| Friday   | Calendar audit: refusal rate, approval latency, evidence ratio.       |
| Saturday | Quiet (no automated activity).                                        |

The Content Strategist agent runs the calendar; humans publish.

## Approval States and Transitions

- `idea → draft` — the Content Strategist writes the first draft.
- `draft → queued_for_review` — claims, brand-voice, and proof
  safety evals pass.
- `queued_for_review → approved` — founder approves.
- `queued_for_review → declined` — founder returns or declines.
- `approved → published` — human publishes; trust ledger entry
  recorded.
- `published → archived` — after 12 months, items are archived.

A transition from `draft` to `queued_for_review` is invalid if any
eval flag is unresolved.

## Refusal Catalogue (Calendar-Specific)

Items the calendar declines to schedule:

- Items with guaranteed-outcome wording (rule
  `no_guaranteed_revenue_claims`).
- Items that name a customer without approval.
- Items that depend on data outside the buyer's data scope.
- Items that mimic competitor marketing language ("we do everything
  X does, but better"). Dealix positioning is its own; comparisons
  are limited to anti-positioning statements grounded in evidence.
- Items promoted by the calendar's "engagement bait" pattern
  detector — controversy-mining, manufactured outrage, or rage-bait
  rephrasings.

## Evidence Ratio

Each calendar item is scored for evidence presence on a simple
trinary:

- `evidence_strong` — points to a working artefact, a sector data
  point with method, or an audit ledger entry.
- `evidence_partial` — points to a pattern observed across
  engagements but without a single citable artefact.
- `evidence_absent` — opinion only.

The Marketing OS targets at least 60% `evidence_strong` and 30%
`evidence_partial` across any rolling 30-day window. Items at
`evidence_absent` are rare and require founder rationale.

## Localisation in the Calendar

Each calendar item is tagged with `lang: ar`, `lang: en`, or
`lang: ar+en`. Arabic items are peer-quality, not translations.
The Content Strategist budget is split intentionally so Arabic does
not become an afterthought. Sector reports default to bilingual
publication.

## Calendar Anti-Patterns

- "Calendar pressure" — posting because the calendar says so.
  Quality gate dominates schedule.
- "Trend-chasing" — riding a viral pattern that has no evidence
  loop behind it. The objection loop is preferred to the trend
  loop.
- "Hot takes" — opinion posts without a defensible governance or
  evidence backing.
- "Back-fill" — pretending a missed cadence didn't happen.
- "Cosmetic refreshes" — re-posting the same item with new emoji.
  Items are rewritten when the evidence changes; not for cosmetic
  refresh.

## Auditing the Calendar

The Performance Analyst audits the calendar weekly:

- Approval rate by loop.
- Refusal rate by reason code.
- Evidence ratio.
- Approval latency.
- Channel mix vs. target.

Calendar audits are filed in `marketing/calendar_audit.csv`. A
quarterly review consolidates the weekly audits and feeds the
Marketing OS review.

## Integration with the Outreach Calendar

The outreach queue is separate from the content calendar but the
two interact:

- An approved newsletter section may seed an outreach email
  template.
- An approved LinkedIn post may seed an outreach LinkedIn opener.
- An approved sector report excerpt may seed an outreach attachment.

Cross-seeding is recorded in both calendars so the lineage of an
artefact is visible.

## Failure Modes

- The calendar receives no new items for a week. Failure: the loops
  are not feeding the calendar. The Content Strategist raises a
  flag and the founder reviews the loops.
- The calendar contains too many items but few approvals. Failure:
  drafts are not meeting the quality bar. The Brand Guardian flags
  patterns and the Content Strategist re-prioritises.
- A published item is later found to contain an unapproved
  reference. Failure: the proof-safety eval missed it. Item is
  retracted; trust ledger entry records the retraction.
- A published item is later found to contain a guaranteed-outcome
  phrase. Failure: the claims-safety eval missed it. Item is
  retracted; the eval is upgraded.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Brand voice: `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- Copywriting rules: `docs/marketing/COPYWRITING_RULES.md`.
- Founder-led content: `docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md`.

## Why a Queue, Not a Clock

A clock-driven calendar produces content because the day demands
it. A queue-driven calendar produces content because the evidence
demands it. The Marketing OS uses a queue so that the bar for
publication is "we have something worth saying", not "it is
Tuesday". Over time, this discipline compounds: buyers learn to
trust that Dealix only ships when there is evidence behind the
words.
