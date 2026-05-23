# Revenue Factory Runtime v2

## Relationship to existing docs
This document is the operational master spec for the v2 commercial runtime layer. It builds on, and does not replace:
- `docs/00_constitution/NON_NEGOTIABLES.md` and `docs/institutional/CONSTITUTIONAL_PRINCIPLES.md` (the 7 non-negotiables that govern every machine below).
- `dealix/trust/approval.py` — the existing approval surface (A0–A3, R0–R3, S0–S3, `NEVER_AUTO_EXECUTE` safelist). Every "Human Approval Required" item below maps to that surface.
- `README.md` operating loop: AI explores/analyzes/recommends → deterministic workflows execute → humans approve.

## Purpose
Run Dealix as a 24/7 commercial operating machine that discovers, enriches, scores, drafts, routes, follows up, converts, delivers, retains, and learns.

## CEO Principle
Scale intelligence aggressively.
Scale outreach carefully.
Scale delivery with QA.
Scale automation with trust gates.
Scale SaaS only after repeated paid workflows.

## Runtime Machines

### 1. Market Intelligence Machine
Finds sectors, directories, competitors, public company lists, trigger events, buyer patterns, and partner ecosystems.

### 2. Lead Discovery Machine
Collects companies from approved public sources and sector search queues.

### 3. Enrichment Machine
Adds website, city, sector, offer, buyer titles, public contact path, source, and fit notes.

### 4. Scoring Machine
Scores every company by ICP fit, Saudi relevance, ticket potential, buyer clarity, and outreach readiness.

### 5. Suppression Machine
Prevents contact to opt-outs, bad-fit, duplicates, risky sources, and rejected leads.

### 6. Outreach Draft Machine
Creates safe personalized drafts in Arabic and English.

### 7. Approval Machine
Builds a daily approval queue for the founder (see `docs/control_plane/SALES_COCKPIT_V2.md` and the generated `docs/founder/approval_center.md`).

### 8. Send Queue Machine
Moves approved outreach to Gmail drafts, LinkedIn manual queue, or contact-form queue.

### 9. Follow-Up Machine
Schedules follow-ups by channel, reply state, and next action.

### 10. Reply Router
Routes replies into Sample / Proposal / Nurture / Lost / Manual Review.

### 11. Sample Factory
Creates 5-opportunity sample packs for positive replies.

### 12. Proposal Factory
Creates proposal drafts after sample or qualified reply.

### 13. Payment Capture Machine
Tracks payment, PO, or written approval follow-ups.

### 14. Delivery Trigger Machine
Starts client workspace only after payment / PO / written approval.

### 15. Retention Machine
Tracks feedback, health score, retainer ask, renewal, and referral.

### 16. Proof & Content Machine
Turns approved learning into safe posts, case studies, and sector insights.

### 17. CEO Command Machine
Generates daily cockpit, stoplight, KPI stack, risks, and one top action.

## Human Approval Required
- outbound sending
- proposal sending
- pricing / discount
- client delivery report
- public proof
- client name use
- contract / refund / legal action
- sensitive data export

Each of these maps to one or more entries in the existing `NEVER_AUTO_EXECUTE` set inside `dealix/classifications/__init__.py` (e.g., `pricing_offer_commit`, `contract_change`, `sensitive_data_export`, `market_facing_statement`).

## Never Automatic
- spam
- guaranteed revenue / sales claim
- scraping restricted platforms against terms
- legal or payment commitments
- public client claims
- ignoring opt-outs

## Operating Targets
- 500 researched leads in 30 days.
- 100 leads per priority sector.
- 25–50 approved sends/day during warmup.
- 3–5 samples/week.
- 1–3 proposals/week.
- 1 paid sprint / PO target as soon as possible.
