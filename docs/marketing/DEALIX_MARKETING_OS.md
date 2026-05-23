# DEALIX Marketing OS

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Saudi B2B Revenue Operating System.
> Built on Trust · Driven by Growth · Closing Deals · Focused on
> Results · Global Mindset, Local Impact.

The Dealix Marketing OS is not a content calendar with a tagline. It
is an operating system that produces evidence-based marketing
artefacts, enforces brand voice, gates proof publication, and
queues all distribution for approval. This document defines the
operating system: its components, contracts, agents, and refusals.

## Operating Principles

- Marketing exists to shorten the time between a buyer's question
  and Dealix's evidence. It does not exist to manufacture demand.
- No marketing artefact promises revenue, sales, or meetings.
- No proof artefact (case study, screenshot, customer name) is
  published without recorded approval in the trust ledger.
- No external send happens automatically. Distribution is queued by
  the Distribution Operator; the founder approves; humans execute.
- Brand voice is enforced by the Brand Guardian agent on every
  draft, every campaign, every variant.
- A3 (autonomous external action) is banned. Marketing agents
  operate at A1 or A2 only.

## Components of the Marketing OS

The Marketing OS comprises seven components, each with an owning
agent and an evidence path.

| Component                  | Owning agent          | Evidence path                            |
|----------------------------|-----------------------|------------------------------------------|
| Brand voice and identity   | Brand Guardian        | `brand/brand_assets_registry.csv`        |
| Content calendar           | Content Strategist    | `marketing/content_calendar.csv`         |
| Founder-led content        | Content Strategist    | `marketing/founder_content_log.csv`      |
| Landing pages              | Content Strategist    | `marketing/landing_page_registry.csv`    |
| Outreach (email, LinkedIn, partner) | Distribution Operator | `outreach/*.csv`               |
| Sector reports / newsletters | Content Strategist  | `marketing/sector_reports.csv`, `marketing/newsletter_log.csv` |
| Case studies / social proof | Proof Safety Agent   | `proof/proof_library.csv`, `proof/proof_approval_queue.csv` |

Each component is documented in a separate file in this directory.

## Distribution Channels

The Marketing OS uses six channels, none of which act autonomously.

- **Email outreach** — drafted by Distribution Operator, approved by
  founder, sent manually.
- **LinkedIn outreach** — drafted by Distribution Operator, approved
  by founder, posted/messaged manually.
- **Contact form / sector landing pages** — drafted by Content
  Strategist, deployed only after Brand Guardian and Trust Guardian
  approval.
- **Founder content (long-form and short-form)** — drafted by
  Content Strategist, approved by founder, posted manually.
- **Newsletter** — drafted by Content Strategist, approved by
  founder, sent manually through the contracted provider.
- **Sector reports** — drafted by Content Strategist with sector
  research, approved by founder, published manually.

WhatsApp is allowed only for prior business relationships, never
for cold outreach. Paid advertising is allowed only after a defined
readiness state (see below).

## Content Loops

Every piece of content flows through one of three loops:

- **Objection loop.** A sales-call objection becomes a LinkedIn
  post, a short-video script, a newsletter section, an FAQ entry,
  an email-reply pattern, and a partner asset.
- **Governance loop.** A governance pattern (claims discipline,
  PDPL posture, approval-gated proof) becomes a teardown post, an
  internal memo, and a sector report excerpt.
- **Evidence loop.** An anonymised pattern from a sprint or pilot
  becomes a scorecard snippet, a sector report data point, and a
  newsletter section. Identifiable detail never leaves the trust
  ledger.

Loops are not pipelines; they are recurring cycles. A single
objection can power five different artefacts across two months.

## Brand Voice Contract

Brand voice is defined in `BRAND_VOICE_EXAMPLES.md` and enforced by
the Brand Guardian agent on every draft. The voice is sober,
evidence-based, free of hype, and PDPL-aware. The Marketing OS does
not ship a draft until the Brand Guardian eval is green.

Forbidden language patterns:

- "Guaranteed revenue", "guaranteed sales", "guaranteed meetings".
- "10x", "100x", "best in class", "world-class", "industry-leading"
  without evidence.
- Unapproved customer names, logos, or testimonials.
- "Up to N%" improvement claims without a written method and
  evidence.
- "Limited time", "act now", manufactured urgency.

## Trust Gates

The Marketing OS has three trust gates that every draft must clear.

- **Claims-safety eval.** Scans for guaranteed-outcome wording and
  unverifiable claims.
- **Brand-voice eval.** Scans for tone drift and forbidden language
  patterns.
- **Proof-safety eval.** Scans for unapproved customer references,
  screenshots, or quotes.

A draft that fails any gate cannot be queued for approval. The
draft is returned to the relevant agent with the failure reason.

## Paid Advertising Readiness

Paid advertising does not start at zero. The Marketing OS requires
five readiness conditions before launching paid campaigns:

- At least three to five qualified meetings booked from organic
  content.
- At least two recurring objections documented in the objection
  loop with a defended response.
- At least one proof pack request from a buyer outside the founder's
  network.
- An ICP statement that has been used in at least three sales
  conversations without major rework.
- A retargeting policy that respects PDPL and the buyer's data
  scope.

Until all five are met, paid spend is bounded to brand awareness
inside a small audience and is reviewed weekly.

## Approval Flow for Marketing Artefacts

1. Content Strategist or Distribution Operator drafts the artefact.
2. Claims-safety, brand-voice, and proof-safety evals run.
3. Agent queues the artefact for founder review with all flags
   visible.
4. Founder approves or returns.
5. After approval, the artefact is filed in the appropriate evidence
   path (`marketing/...`, `outreach/...`, or `proof/...`).
6. The send / publish action is taken manually by a human. The
   action is recorded in the trust ledger.

## Suppression Hygiene

Outreach and sector report distribution honour the suppression list.
The list is reconciled before any draft is queued. Suppression
sources include:

- Inbound opt-outs.
- Buyer-requested suppression.
- Founder-flagged suppression (sectors, conflicts, sensitive
  accounts).
- Sector or jurisdiction policy.

The policy adapter denies any outreach action targeting a suppressed
identity (rule id `no_suppressed_outreach`).

## Localisation

Marketing is bilingual by default: Arabic and English. The Brand
Guardian evaluates both languages on equal footing; an Arabic draft
is not a translation but a peer artefact. Localisation is part of
the Local Impact pillar — it shows up in copy, in sector references,
and in the example data inside sector reports.

## Metrics That Matter

The Performance Analyst tracks:

- Drafts produced vs. approved vs. distributed.
- Approval latency.
- Reply-rate on approved outbound.
- Qualified conversation rate from organic content.
- Proof pack request volume.
- Refusal rate (drafts declined for claims, suppression, or scope).

Metrics that the Marketing OS does not optimise for: raw reach, raw
open rates, vanity engagement. These are observed, not chased.

## Anti-Patterns

- Producing content because the calendar says so, even when nothing
  new has happened. The calendar serves the loops; the loops do not
  serve the calendar.
- Publishing a case study because the buyer "won't mind". Approval
  is recorded or the case study does not ship.
- Posting a benchmark without evidence. Benchmarks are derived from
  the evidence loop, not borrowed from a deck.
- Running paid before readiness. Paid amplifies whatever exists; if
  the operating loop is not working, paid spend just makes the
  failure faster.
- Translating Arabic by machine. Arabic is a peer language; quality
  is part of the brand voice.

## Owning Agents

The Marketing OS lists every owning agent for every component in
the table at the top of this file. Each owning agent has:

- A maximum approval class (A1 or A2; A3 is banned).
- A kill switch (any operator can pause the agent).
- An eval requirement (the agent's outputs must clear the relevant
  evals).
- An audit requirement (every output is logged).
- A list of allowed write targets (the agent cannot write outside
  this list).

See `docs/ai/` for each agent's full contract.

## Cross-References

- Product ladder: `docs/product/DEALIX_PRODUCT_LADDER.md`.
- Distribution OS: `docs/product/PRODUCT_DISTRIBUTION_OS.md`.
- Positioning: `docs/product/PRODUCT_POSITIONING.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.
- Agent registry: `registries/agent_registry.yaml`.

## Review Cadence

The Marketing OS is reviewed quarterly. The review covers:

- Component health (artefact volume, refusal volume, approval
  latency).
- Brand-voice drift (Brand Guardian flag rate).
- Trust posture (proof publication approvals, suppression events).
- Channel mix.
- Paid readiness state.

Review output is recorded in `marketing/marketing_os_review.md` and
referenced in the founder operating scorecard.

## Why a Marketing OS

Most early-stage marketing collapses into "post more". Most
late-stage marketing collapses into "spend more". The Marketing OS
collapses neither. It produces artefacts that earn the right to be
distributed and refuses to distribute artefacts that do not. That
discipline, repeated weekly, is how Dealix earns trust at scale
without ever crossing the line into guaranteed-outcome marketing.
