# Product Distribution OS

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> How each rung of the Dealix product ladder reaches a buyer:
> channels, content, sequence, evidence, refusal points.

The Product Distribution OS is not a marketing funnel. It is an
operating system that turns each rung of the ladder into a repeatable,
trust-gated sequence. No external send is automatic; the Distribution
Operator agent prepares and queues, the founder approves, and humans
execute.

## Operating Principles

- Distribution always begins with evidence, not with a pitch. The
  first contact carries something a buyer can use even if they never
  meet Dealix.
- Channels are explicit and bounded. Dealix uses email, LinkedIn,
  contact form, partner referral, founder-led content, and (where a
  prior business relationship exists) WhatsApp.
- Suppression hygiene is non-negotiable. The suppression list is
  reconciled before any draft is queued.
- No guaranteed-outcome wording in any channel. Claims pass the
  brand voice and claims-safety evals before queueing.
- All published proof is approval-gated. Logos, screenshots, and
  customer names never appear in distribution material without a
  recorded approval in the trust ledger.

## Channel Inventory

| Channel             | Owner agent           | Approval class | Primary motion |
|---------------------|-----------------------|----------------|----------------|
| Email outreach      | Distribution Operator | A2 (draft)     | Sample, sprint, retainer entry |
| LinkedIn outreach   | Distribution Operator | A2 (draft)     | Founder-led reach, partner intros |
| Contact form        | Distribution Operator | A2 (draft)     | Sector-targeted lead capture |
| Founder content     | Content Strategist    | A2 (draft)     | Long-arc trust building |
| Newsletter          | Content Strategist    | A2 (draft)     | Weekly evidence drumbeat |
| Partner referral    | Partner Revenue Agent | A2 (draft)     | Warm intros from partners |
| Sector report       | Content Strategist    | A2 (draft)     | Account-targeted gravity |
| Event / roundtable  | Founder (manual)      | n/a            | Trust-building, R5+ buyers |

A3 (autonomous external action) is banned. Every channel above has a
queue, a draft step, and a human approval step.

## Sequencing by Rung

### R1 — Free Sample / Diagnostic

- **Entry channels:** founder-led content; sector report download;
  partner intro; contact form.
- **First touch:** the buyer downloads or requests a sample; the
  sample carries a one-page Scorecard, a Diagnostic Brief outline,
  and a refusal list (what Dealix will not do).
- **Follow-up sequence:** 0/3/7 day cadence, all drafts queued for
  founder approval before send. No more than three follow-ups; the
  fourth touch is only sent if the buyer requested it.
- **Refusal point:** if the buyer asks for guaranteed pipeline or
  meetings, the sequence is closed with a polite decline and the
  reason is logged.

### R2 — Revenue Sprint

- **Entry channels:** R1 diagnostic outcome; founder-led content
  with a sprint case study (only published proof, fully approved);
  partner referral.
- **First touch:** scoping conversation booked via the Founder
  Console calendar (not via an external automation).
- **Follow-up sequence:** a scope letter, a sample sprint plan,
  references on request (only references that have approved being
  named).
- **Refusal point:** if the buyer demands external send automation
  or expects Dealix to operate without an evidence loop, the sprint
  is declined.

### R3 — Managed Pilot

- **Entry channels:** R2 outcome; sector report follow-up; partner
  co-introduction; founder-led content (objection teardown,
  governance teardown).
- **First touch:** a pilot charter conversation with the founder
  and the buyer's revenue lead.
- **Follow-up sequence:** weekly pilot review pack; mid-point
  decision memo; close memo. All artefacts written; nothing
  promised verbally.
- **Refusal point:** if the buyer wants the pilot delivered without
  a charter or without the eval gate, Dealix declines.

### R4 — Revenue Desk Retainer

- **Entry channels:** R3 outcome only by default. Direct entry is
  rare and requires a sprint pre-step.
- **First touch:** retainer SLA and data scope conversation.
- **Follow-up sequence:** monthly executive review pack, quarterly
  trust audit, renewal memo 60 days before each renewal.
- **Refusal point:** if the buyer cannot agree to the data scope
  or kill-switch ownership, the retainer is declined.

### R5 — Founder Console

- **Entry channels:** founder-led content (Founder Console teardown,
  policy-as-code teardown); R3 / R4 outcomes; partner referral
  where the partner is an integrator.
- **First touch:** a console acceptance walkthrough with the buyer's
  founder.
- **Follow-up sequence:** policy mirror review, agent registry
  review, eval gate review.
- **Refusal point:** if the buyer wants to disable the eval gate or
  the kill switch, the console seat is not provisioned.

### R6 — Enterprise Revenue Intelligence OS

- **Entry channels:** founder-direct conversations (Dealix does not
  cold-prospect enterprises); sector body referrals; existing R5
  expansions.
- **First touch:** enterprise security and architecture briefing.
- **Follow-up sequence:** master agreement, data processing
  agreement, sector overlay scoping; multi-stakeholder review with
  security, data, and compliance teams.
- **Refusal point:** unresolved high-severity findings in the
  security review pause the engagement until remediation.

### R7 — Partner / White-label Revenue OS

- **Entry channels:** founder-direct conversations only.
- **First touch:** partnership scoping with the partner's principals.
- **Follow-up sequence:** partner agreement, brand carve-out, eval
  gate certification of partner-side agents.
- **Refusal point:** any attempt to publish proof, commit pricing,
  or enable A3 automation outside the agreement pauses the
  partnership.

## Content Loops Feeding Distribution

The Content Strategist runs three loops that feed every channel:

- **Objection loop:** an objection raised in a sales call becomes a
  LinkedIn post, a short video script, a newsletter section, an
  FAQ article, an outbound email reply pattern, and a partner asset.
- **Governance loop:** a governance pattern (claims discipline,
  PDPL posture, approval-gated proof) becomes a teardown post, an
  internal memo, and a sector report excerpt.
- **Evidence loop:** an anonymised pattern from a sprint or pilot
  becomes a scorecard snippet, a sector report data point, and a
  newsletter section. Identifiable detail never leaves the trust
  ledger.

## Queueing Contract

Every draft produced by the Distribution Operator must include:

- `channel`
- `target_id` (matched against suppression list)
- `target_relationship_status` (cold, warm, existing relationship)
- `draft_body`
- `claims_flags` (output of claims-safety eval)
- `brand_voice_flags`
- `evidence_links` (to sample, sector report, content)
- `human_review_notes`
- `approval_state` (`draft`, `queued_for_review`, `approved`,
  `declined`)

The founder approves or declines the draft in the Founder Console.
Sending happens manually after approval; the Distribution Operator
does not execute the send.

## Suppression and Reconciliation

The suppression list lives in the private ops runtime. It is
reconciled before any draft is queued. Sources include:

- Inbound opt-outs (email, LinkedIn).
- Buyer-requested suppression (closed accounts, lost deals).
- Founder-flagged suppression (out of scope, conflict, sensitive
  sectors).
- Sector or jurisdiction policy.

A draft targeting a suppressed identity is denied at the policy
adapter with rule id `no_suppressed_outreach`.

## Pacing

- Outbound (email + LinkedIn): bounded daily caps per sender; never
  more than the founder can review the same day.
- Newsletter: weekly cadence; missed weeks are acknowledged, not
  back-filled.
- Founder content: five posts a week target; quality gate dominates
  cadence. A week with three reviewed posts is preferred to a week
  with five rushed ones.
- Sector reports: quarterly, with named contributors only after
  approval.

## Metrics That Matter

Distribution is measured by the Performance Analyst on:

- Drafts queued vs. approved vs. sent.
- Approval latency (founder review time).
- Reply-rate on approved sends.
- Qualified conversation rate.
- Refusal rate (drafts declined for claims, suppression, or scope).

Metrics that are not optimised for: total sends, raw open-rate,
vanity reach. These are observed, not chased.

## Refusal Catalogue

Distribution refuses to act on:

- Targets without a defensible relationship signal.
- Drafts containing guaranteed-outcome language.
- Drafts referencing customers without approval.
- Targets on the suppression list.
- Sectors outside the founder-set allow-list.
- Channels not in the channel inventory above.

## Audit and Eval

- Every queued draft is logged with the eval result.
- Every approval/decline is logged in the trust ledger.
- The Performance Analyst publishes a weekly channel scorecard.
- The Trust Guardian raises a flag whenever the refusal rate spikes
  above the rolling baseline or whenever a draft is approved with
  an outstanding claims flag.

## Distribution and the Ladder

Distribution is not the goal. The goal is to keep buyers on the rung
where the evidence justifies the spend. Distribution exists to
shorten the time between a buyer's question and Dealix's evidence.
When that loop tightens, every rung delivers more honestly.
