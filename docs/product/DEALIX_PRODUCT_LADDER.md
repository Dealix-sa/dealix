# DEALIX Product Ladder

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Saudi B2B Revenue Operating System.
> Built on Trust. Driven by Growth. Closing Deals. Focused on Results.
> Global Mindset, Local Impact.

This document defines the seven-rung product ladder Dealix uses to move
prospects from a free diagnostic to a co-built revenue operating system.
Each rung is a discrete offer with its own scope, price band, trust
gate, evidence requirement, and ideal-customer profile. The ladder is a
working contract between Dealix and its buyers; it is not a marketing
deck.

## Operating Principles

- No rung promises guaranteed revenue, sales, or meetings. Outputs are
  described as evidence, decisions, queues, and drafts.
- No external send happens automatically at any rung. Distribution
  Operator queues; the founder approves; humans execute.
- No proof publication (case studies, customer names, screenshots)
  occurs without recorded approval in the trust ledger.
- Pricing bands below are reference SAR ranges. Any deviation
  (discount, contract change, payment-term change) requires explicit
  founder approval. The Founder Console is the only sanctioned origin
  for these approvals.
- Each rung lists the evals it must pass before the offer can be
  delivered, and the audit artifacts it must produce.

## Ladder Overview

| Rung | Offer                                  | Price band (SAR)  | Trust gate                            | Typical buyer                              |
|------|----------------------------------------|-------------------|---------------------------------------|--------------------------------------------|
| R1   | Free Sample / Diagnostic               | 0                 | Identity verified; no PII shared      | Founder evaluating Dealix                  |
| R2   | Revenue Sprint                         | 18,000 – 35,000   | Scope letter; suppression check       | Saudi SMB / mid-market with active pipe    |
| R3   | Managed Pilot                          | 45,000 – 90,000   | Pilot charter; eval gate green        | Mid-market with repeatable motion          |
| R4   | Revenue Desk Retainer (monthly)        | 25,000 – 55,000   | Retainer SLA; data scope agreed       | Founder-led revenue org, < 30 reps         |
| R5   | Founder Console (per-seat / annual)    | 60,000 – 180,000  | Console acceptance; PDPL posture      | Founder/CEO operating their own deal flow  |
| R6   | Enterprise Revenue Intelligence OS     | 250,000 – 1.2M    | Enterprise security review; sign-off  | Multi-BU enterprise; regulated sector      |
| R7   | Partner / White-label Revenue OS       | Bespoke + revshare| Partner agreement; brand carve-out    | Consultancies, integrators, sector bodies  |

Pricing bands are operational guidance. They are not published
externally without founder approval; sales conversations always quote
ranges, never single numbers, until scope is verified.

---

## R1 — Free Sample / Diagnostic

### Scope

A short, evidence-only diagnostic of the buyer's current revenue
posture. Inputs are limited to public information and what the buyer
chooses to share. Output is a 6–10 page Dealix Diagnostic Brief plus
a one-page Scorecard.

- Revenue posture snapshot (pipeline shape, conversion windows,
  proof-of-traction assets that already exist).
- Trust posture snapshot (claims discipline, public proof status,
  PDPL signals).
- Three named bottlenecks with the smallest reversible move for each.
- A list of what Dealix would *refuse* to do on this account, and why.

### Deliverables

- `diagnostic/<account>/dealix_diagnostic_brief.md`
- `diagnostic/<account>/dealix_scorecard.csv`

### Price band

Free. There is no commercial commitment from the buyer at this rung.

### Trust gate

- Identity of the requester verified through the contact form or a
  founder introduction.
- No customer PII collected. Buyer is told explicitly which fields
  are required and which are optional.
- No proof statements or testimonials from the buyer are published.

### Who it is for

- Saudi founders evaluating whether Dealix is a fit before any paid
  conversation.
- Sector partners scoping whether to co-introduce Dealix.

### Failure conditions

- Buyer requests guaranteed pipeline or meetings. Sample is declined
  with the reason recorded in the trust ledger.
- Buyer provides PII outside the agreed scope. The data is purged and
  the trust event logged.

---

## R2 — Revenue Sprint

### Scope

A 3–4 week engagement that turns the diagnostic into a working
revenue motion. Dealix builds the smallest defensible operating
loop: ICP definition, scored target list, message system, proof
library, weekly review rhythm.

- ICP sheet (sector, size, role, signal).
- Account scoring model with explicit weights.
- Outreach drafts (email, LinkedIn, contact form) queued only — no
  external send.
- Founder-led content kit (5 posts, one long-form, one objection
  teardown).
- Trust posture upgrades (claims rewrites, proof approval queue).

### Deliverables

- `sprint/<account>/icp.md`
- `sprint/<account>/account_scoring.csv`
- `outreach/queue.csv` (all drafts, no sends)
- `marketing/content_calendar.csv` (sprint window only)
- `trust/approval_decisions.csv` (claims rewrites)

### Price band

SAR 18,000–35,000 fixed. 50% on signed scope letter, 50% on sprint
close. Payment-term variation requires founder approval.

### Trust gate

- Signed scope letter recording the sprint's named outputs.
- Suppression list reconciled before any outreach is drafted.
- Eval gate green for claims safety and brand voice.

### Who it is for

- Saudi SMB and mid-market with an active but inconsistent pipeline.
- Founders who want to see Dealix work end-to-end on their own
  account before considering a retainer.

### Failure conditions

- Dealix cannot reach a defensible ICP from the data provided.
  Sprint is paused; refund logic is recorded in the proposal.
- Buyer demands external send automation. Dealix declines and the
  refusal is logged.

---

## R3 — Managed Pilot

### Scope

A 6–10 week pilot where Dealix runs the Revenue Sprint loop on a
defined slice of the business and operates the queues alongside the
buyer's team. All execution remains human-approved.

- Sprint outputs maintained week over week.
- Distribution Operator runs the queue; founder (buyer-side) signs
  off on each batch.
- Performance Analyst surfaces conversion bottlenecks; recommended
  fixes are returned to the buyer with evidence.
- Pilot charter records what is in scope, what is out of scope, and
  what the explicit kill conditions are.

### Deliverables

- All Sprint deliverables, refreshed weekly.
- `pilot/<account>/pilot_charter.md`
- `pilot/<account>/weekly_pilot_review.md`
- `distribution/channel_scorecard.csv`
- `evals/eval_status.csv` (per pilot week)

### Price band

SAR 45,000–90,000 for the pilot window. 40% on charter, 40% at
mid-point, 20% on close. Mid-point payment can only release if the
eval gate is green and the trust posture has not regressed.

### Trust gate

- Pilot charter signed by buyer and Dealix founder.
- Eval gate green at week 0 and at every weekly review.
- Proof publication remains gated; nothing about the pilot is
  externalised without buyer approval.

### Who it is for

- Mid-market companies with a repeatable motion that is
  under-instrumented.
- Buyers who want to see weekly evidence before committing to a
  retainer.

### Failure conditions

- Two consecutive weekly reviews flag the same unaddressed
  bottleneck. The pilot pauses and the founder owns the next step.
- A trust event (claim breach, suppression breach) triggers the
  kill switch on the relevant agent.

---

## R4 — Revenue Desk Retainer

### Scope

A monthly retainer where Dealix operates the buyer's revenue loop as
an extension of their team. Same trust principles as the pilot, but
the rhythm is steady-state.

- Weekly ops cadence (account scoring refresh, queue grooming,
  proof library refresh).
- Monthly executive review (scorecard, decisions taken, decisions
  pending).
- Quarterly trust posture audit (claims discipline, proof approval
  state, suppression hygiene).

### Deliverables

- `retainer/<account>/monthly_review.md`
- `retainer/<account>/quarterly_trust_audit.md`
- All Sprint/Pilot operational CSVs, maintained continuously.

### Price band

SAR 25,000–55,000 per month. 3-month minimum. Cancellation requires
30-day notice. Payment-term variation requires founder approval.

### Trust gate

- Retainer SLA signed.
- Data scope agreement covering what Dealix may read and write.
- Suppression list synced on day one and reconciled monthly.

### Who it is for

- Founder-led revenue organisations with fewer than 30 reps.
- Companies that prefer an embedded operator over hiring a Head of
  Revenue Ops.

### Failure conditions

- Buyer requests Dealix execute external action automatically.
  Retainer is paused; refund logic kicks in.
- Trust audit fails two consecutive quarters. Dealix exits the
  retainer per the SLA.

---

## R5 — Founder Console

### Scope

A licensed seat in the Dealix Founder Console — the same surface
Dealix uses internally. The buyer's founder operates their own deal
flow, with Dealix agents in assist mode (A1/A2 only).

- Console seats (founder + chosen operators).
- Agent assist for CEO Copilot, Growth Strategist, Distribution
  Operator, Content Strategist, Performance Analyst, Trust
  Guardian, Finance Copilot.
- Policy-as-code mirror so the buyer's own claims, suppression, and
  approval rules govern the agents.

### Deliverables

- Console access with role-scoped permissions.
- `console/<tenant>/policy_mirror.yaml`
- `console/<tenant>/agent_registry.yaml`

### Price band

SAR 60,000–180,000 per year, banded by seat count and sector. Annual
billing default. Multi-year commitments require founder approval.

### Trust gate

- Console acceptance checklist signed (PDPL posture, retention
  windows, kill-switch ownership).
- Tenant policy reviewed by Dealix Trust Guardian.

### Who it is for

- Founders and CEOs who want to operate their own revenue motion
  with AI assist rather than hand it off.

### Failure conditions

- Tenant disables the eval gate or the kill switch. Console seat is
  paused until restoration.
- Tenant attempts to enable A3 (autonomous external action). Action
  is blocked at the policy adapter and the founder is notified.

---

## R6 — Enterprise Revenue Intelligence OS

### Scope

A multi-business-unit deployment of the Founder Console with
enterprise-grade controls: SSO, audit export, sector overlays,
sandboxed integrations. Dealix delivers alongside the buyer's
security, data, and compliance teams.

- Tenant isolation with documented data boundaries.
- Sector overlay packs (e.g. financial services, healthcare, public
  sector readiness).
- Quarterly enterprise readiness review.
- Optional on-premise or sovereign-cloud deployment under partner
  agreement.

### Deliverables

- Enterprise console deployment.
- Documented architecture decision record per tenant.
- Quarterly trust and security review pack.

### Price band

SAR 250,000–1,200,000 per year, banded by tenant count and overlays.
All commercial terms require founder approval; nothing is shipped
verbally.

### Trust gate

- Enterprise security review complete (covering identity, data
  residency, retention, kill-switch governance).
- Signed master agreement, data processing agreement, and any
  sector-specific addenda.

### Who it is for

- Saudi and GCC enterprises with multiple revenue-bearing business
  units and regulated data.

### Failure conditions

- Security review surfaces unresolved high-severity findings.
  Deployment is paused until remediation.
- Sector overlay requires a capability Dealix does not yet provide.
  Scope is reduced or the engagement is declined.

---

## R7 — Partner / White-label Revenue OS

### Scope

A bespoke arrangement where Dealix licenses portions of the Revenue
OS to a partner (consultancy, integrator, sector body) who delivers
under their own brand or co-brand.

- Carved scope of agents and tools, with explicit allow-listing.
- Brand carve-out: partner brand may front the engagement but
  Dealix retains policy-as-code authority.
- Revenue share recorded in the partner agreement.

### Deliverables

- Partner enablement pack (operating playbook, eval gate, audit
  protocol).
- Co-branded delivery templates.
- Joint review rhythm with the partner.

### Price band

Bespoke. Setup fee plus revenue share. All terms require founder
approval and a written partner agreement before any engagement.

### Trust gate

- Partner agreement signed with brand carve-out and policy mirror.
- Partner agents pass the Dealix eval gate before they operate on a
  buyer.
- All proof publication remains gated by Dealix Trust Guardian.

### Who it is for

- Consultancies that want a Dealix-grade operating layer.
- Sector bodies that want to lift the trust posture of their
  member companies.

### Failure conditions

- Partner attempts to publish proof, change pricing, or enable A3
  automation without approval. Partnership is paused.
- Partner deliverables drift from the Dealix eval gate. Remediation
  plan or contract exit.

---

## Cross-Ladder Contracts

- Every rung has an entry artifact (sample, scope letter, charter,
  SLA, acceptance, agreement, partner agreement).
- Every rung has an exit artifact (close memo) that records what
  was delivered, what was refused, and what was learned.
- Every rung writes to the audit ledger; no rung is allowed to
  publish proof, send externally, or commit pricing without recorded
  approval.

## Movement Between Rungs

Movement is buyer-initiated. Dealix does not upsell automatically.
The Offer Architect surfaces candidates for promotion based on
repeated patterns across engagements; promotion is gated by founder
review. The aim is not to maximise rung escalation; the aim is to
keep the buyer on the rung where the evidence justifies the spend.
