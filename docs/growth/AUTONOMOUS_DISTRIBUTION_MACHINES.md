# Autonomous (and Semi-Autonomous) Distribution Machines

Dealix runs **15 named distribution machines**. Each machine is:

- **Trust-gated** — it can prepare, score, draft, schedule, queue, recommend. It cannot send externally or commit on behalf of Dealix without explicit founder approval.
- **Documented** — every machine has a one-page spec: purpose, input, output, data source, approval class, owner, KPI, failure mode, recovery path.
- **Owned** — a named worker (and a named human owner) is accountable.
- **Auditable** — every run writes to an internal log.

> A machine may be **autonomous** in the sense that it runs on a schedule without prompting. It is **never autonomous** in the sense that it externally sends or commits without human approval.

## 1. The 15 machines

| #  | Machine                          | One-line purpose                                                 |
|----|----------------------------------|------------------------------------------------------------------|
| 1  | Market Intelligence Machine      | Pulls sector signals (jobs, posts, press) into a scored feed.     |
| 2  | Lead Discovery Machine           | Identifies candidate accounts that match ICP.                    |
| 3  | Lead Enrichment Machine          | Adds firmographic, behavioural, and trust fields.                |
| 4  | Lead Scoring Machine             | Applies the deterministic scoring model.                         |
| 5  | Outreach Draft Machine           | Drafts AR/EN outreach using persona-fit + evidence.              |
| 6  | Approval Queue Machine           | Surfaces drafts to the founder; tracks decision + edit history.  |
| 7  | Follow-Up Machine                | Schedules approved follow-ups based on previous reply state.     |
| 8  | Reply Router Machine             | Classifies inbound replies; recommends next action.              |
| 9  | Sample Factory Machine           | Assembles bilingual Proof / Sample artefacts on demand.          |
| 10 | Proposal Factory Machine         | Renders bilingual proposals from the offer ladder.               |
| 11 | Payment Capture Machine          | Prepares invoices and tracks SAR-denominated payment events.     |
| 12 | Content Engine                   | Drafts content per persona × pillar × week.                      |
| 13 | Partner Referral Engine          | Tracks partner contracts, queues warm intro drafts.              |
| 14 | Proof-to-Demand Engine           | Converts delivered work into shareable proof + warm-list.        |
| 15 | Retention Expansion Engine       | Detects expansion signals in delivered accounts; drafts upsell.  |

## 2. Machine spec template

Every machine in `data/growth/distribution_machines.csv` carries these fields:

```
machine_id, name, purpose,
input, output, data_source,
approval_class, trust_gate,
owner, worker_name,
kpi, failure_mode, recovery_path,
last_review_at
```

### Approval class (mirrors the agent governance system)

| Class | Meaning                                                                         |
|-------|---------------------------------------------------------------------------------|
| A0    | No human interaction needed; read-only operations only                          |
| A1    | Draft / queue / recommend; founder must approve before external action          |
| A2    | Same as A1 but with additional gate (e.g. partner co-sign) before approval      |
| A3    | High-risk; double approval required (founder + customer-executive)              |

Machines cap at **A2** by default. Anything that touches external sending or commitments is A1+ and requires explicit founder approval per run.

## 3. Machine details

See per-machine docs:

- `OUTBOUND_DRAFT_MACHINE.md` — drafts; never sends.
- `INBOUND_CONTENT_MACHINE.md` — drafts content per persona × pillar.
- `PARTNER_REFERRAL_MACHINE.md` — partner tracking and warm intros.
- `ABM_STRATEGIC_ACCOUNT_MACHINE.md` — strategic account orchestration.
- `PRODUCT_MARKETING_MACHINE.md` — drives launches, sector reports.
- `NURTURE_MACHINE.md` — B/C account nurture stream.
- `PROOF_TO_DEMAND_MACHINE.md` — turns proof into demand.

## 4. Doctrine: what machines may NOT do

- May NOT send email, LinkedIn, SMS, WhatsApp, or any external message without founder approval per item.
- May NOT make pricing, discount, contract, or refund commitments.
- May NOT publish content to a public surface without approval.
- May NOT alter customer-facing systems (CRM, ATS, ERP) without approval.
- May NOT use scraped data or any source outside our documented `DATA_SOURCES_POLICY.md`.

## 5. KPI roll-up

Each machine contributes to the revenue KPI tree (see `docs/performance/REVENUE_KPI_TREE.md`). Examples:

| Machine                          | KPI                                                 |
|----------------------------------|-----------------------------------------------------|
| Lead Discovery                   | new ICP-matching accounts added / week              |
| Lead Scoring                     | A-priority accounts produced / week                 |
| Outreach Draft                   | drafts queued per A-account / week                  |
| Approval Queue                   | median draft-to-decision time (hours)               |
| Follow-Up                        | follow-up coverage % (no A-thread left silent > 7d) |
| Sample Factory                   | samples assembled / week                            |
| Proposal Factory                 | proposals rendered / week                           |
| Payment Capture                  | invoiced SAR / week                                 |
| Proof-to-Demand                  | proof artefacts published / week                    |
| Retention Expansion              | expansion drafts queued / month                     |

## 6. Failure modes & recovery

Every machine documents both. Examples:

- **Outreach Draft Machine** — failure: produces a draft with no evidence citation. Recovery: machine refuses to emit the draft and escalates to the founder.
- **Reply Router Machine** — failure: misclassifies a reply. Recovery: founder reclassifies, machine learns the rule (manually appended to ruleset; no auto-learning in v1).
- **Payment Capture Machine** — failure: invoice number conflict. Recovery: pause and escalate; never overwrite.

## 7. Kill switch

A founder-level kill switch halts **all** distribution machines simultaneously. The kill switch is one click in the Founder Console and is documented as a hard requirement; see `docs/ai/BRAND_GUARDIAN_AGENT.md` and `docs/ai/GROWTH_STRATEGIST_AGENT.md`.
