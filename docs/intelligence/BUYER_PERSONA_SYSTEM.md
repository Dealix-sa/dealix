# Buyer Persona System

The persona library is the third layer of Dealix market intelligence. It
sits below the sector ranking and the ICP, but above any actual outreach
draft. Personas are not avatars; they are decision-making profiles that
drive offer language, objection handling, and proof selection.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Why personas exist as a separate layer

Two people with the same title can run different decision processes. The
persona layer is what stops the team from writing the same message for a
founder-led SME and an enterprise-CRO at a regulated firm. Each persona
declares:

- Authority shape (decides, signs, blocks, influences).
- Motivations and counter-motivations.
- Common objections and their root cause.
- KPIs they are measured on.
- Trust signals that move them.
- Channels they actually open.
- Failure modes they have learned to avoid.

This layer feeds the `OBJECTION_LIBRARY_SYSTEM.md` and the
`OUTBOUND_DRAFT_MACHINE.md`. It is never a creative document — it is a
checklist for whether a draft is aimed at the right decision shape.

## 2. The five core personas

### 2.1 CEO / Founder

- Motivations: ownership of growth narrative, optionality, capital
  efficiency, board readiness.
- Counter-motivations: distraction, vendor sprawl, hidden lock-in.
- Common objections: "we already tried this", "the CRO will own it",
  "show me a Saudi reference", "I do not want another tool".
- KPIs: net new revenue, gross margin, sales velocity, runway.
- Trust signals: named operator behind the work, dated proof, plain
  pricing, founder-to-founder voice.
- Channels: warm intros, founder content, partner referral, considered
  email.
- Failure modes the persona avoids: opaque pricing, hand-wavy projections,
  generic SaaS pitch.

### 2.2 CRO / Head of Sales

- Motivations: hitting the number, pipeline coverage, rep ramp, win-rate
  stability, forecast accuracy.
- Counter-motivations: tool overload, attribution debates, training cost.
- Common objections: "my team will not adopt", "we already have HubSpot",
  "the lead quality is the problem, not the system", "show me cost per
  meeting".
- KPIs: quota attainment, pipeline coverage, win rate, sales cycle.
- Trust signals: real outcome math, side-by-side with current CRM,
  rep-level evidence, retention math.
- Channels: LinkedIn, structured email, in-person founder dinners,
  partner-introduced calls.
- Failure modes: tool sprawl, lead-quality blame loop, dashboard theatre.

### 2.3 COO

- Motivations: process reliability, operating leverage, audit posture,
  cost-to-serve, partner orchestration.
- Counter-motivations: shadow systems, manual workarounds, opaque vendors.
- Common objections: "this is sales' problem", "we need it to integrate",
  "what about PDPL and data residency", "do not break our reporting".
- KPIs: cost per delivery, on-time rate, NPS, audit findings closed.
- Trust signals: documented playbooks, integration realism, audit trail,
  named owners.
- Channels: structured email, partner referrals, ops community signals.
- Failure modes: integration hand-waving, undocumented behaviour,
  unmaintained vendor tools.

### 2.4 CTO / Head of Engineering

- Motivations: secure, observable, low-cost, low-toil systems; AI
  governance posture.
- Counter-motivations: black boxes, "AI magic", proprietary lock-in.
- Common objections: "how is data handled", "show me the eval evidence",
  "where is the audit trail", "what is the rollback plan".
- KPIs: incident frequency, MTTR, eval pass rate, audit closure rate.
- Trust signals: published eval results, policy-as-code, kill switches,
  documented agent registry.
- Channels: technical content, founder content, technical references.
- Failure modes: marketing-led AI claims, unverifiable autonomy claims.

### 2.5 Head of Marketing

- Motivations: pipeline contribution, brand consistency, content velocity,
  attribution clarity.
- Counter-motivations: vendor over-promise, generic content templates,
  black-box automation that hurts brand.
- Common objections: "this competes with my agency", "brand voice is a
  concern", "what is the attribution model".
- KPIs: SQL contribution, content velocity, retention of brand voice,
  CAC payback.
- Trust signals: drafts that pass brand review on the first pass,
  bilingual ability, named operator behind the engine.
- Channels: founder content, content swaps, partner referrals.
- Failure modes: generic AI content, attribution fog, brand drift.

## 3. Persona structure (CSV)

`growth/personas.csv` columns:

- `persona_id`
- `name`
- `authority_shape` — decides | signs | blocks | influences
- `motivations`
- `counter_motivations`
- `objections` — pipe-delimited
- `kpis`
- `trust_signals`
- `channels`
- `bilingual_default` — ar | en | both
- `last_reviewed_at`
- `reviewed_by`

## 4. Persona-to-ICP binding

Personas are bound to ICPs in `growth/icp_persona_matrix.csv` with:

- `icp_id`
- `persona_id`
- `authority_shape` — context-specific override
- `priority` — primary | secondary
- `notes`

A draft outreach never targets a persona without a bound ICP. This is the
forcing function that prevents "send to all CEOs in the list" behaviour.

## 5. Saudi context overlays

- Authority concentration: in many Saudi B2B firms, the CEO or chairman
  retains final say even when a CRO or COO appears to lead. Persona entries
  flag this with `authority_concentration: high`.
- Bilingual operating reality: persona entries declare default operating
  language; outreach drafts respect it.
- Relationship density: warm path is often required even for high-authority
  personas; the persona entry records whether a warm path is mandatory.
- Procurement: enterprise procurement can be slow even after the buyer
  says yes; persona objections include procurement realism.

## 6. Cadence

| Cadence | Activity |
|---|---|
| Monthly | Persona library review |
| Quarterly | Persona re-interview cycle (3 buyers per persona) |
| Ad hoc | Update when reply rates drift outside band |

## 7. Owners and approval

- Owner: Growth Strategist.
- Approver: Founder Console on additions or deletions.
- Auditor: Trust Guardian.

## 8. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Persona-titles-as-truth | Re-validate via 3 buyer interviews |
| Same draft for two personas | Outreach draft machine blocks; re-bind ICP |
| Persona drift | Reset; pull objections from the last 30 days of replies |
| Authority shape ignored | Distribution operator returns draft for rewrite |

## 9. Non-negotiables

- No persona narrative contains guaranteed-outcome language.
- No persona is used to justify external action without an approval.
- A3 is not used. Only A1 (drafting) and A2 (assist with approval).

Personas are the difference between writing to a job title and writing to
a decision. Dealix writes to the decision.
