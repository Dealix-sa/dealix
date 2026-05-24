# Distribution War Machine

> The unified view of every distribution machine. Every machine produces drafts, queues, scores, or recommendations — never autonomous external action.

## 1. Why "war machine"

Saudi B2B is a high-trust market. Volume kills brand. The Distribution War Machine wins by **signal density** and **execution discipline**, not blast volume.

## 2. Architecture

```
Intelligence layer
    ↓
Account scoring + trigger events
    ↓
Per-machine draft generation
    ↓
Queue (CSV / Postgres)
    ↓
Approval gate (/approvals)
    ↓
Manual operator action
    ↓
Reply router
    ↓
Outcome events → audit + learning loop
```

## 3. Machines

| Machine | Purpose | Queue |
|---|---|---|
| Outbound Draft | Personalised email drafts | `outreach_queue.csv` |
| LinkedIn Queue | Connect notes + InMail drafts | `linkedin_queue.csv` |
| Email Draft | Sequenced cadences | (subset of outbound) |
| Contact Form Queue | Human-completed inbound forms | `contact_form_queue.csv` |
| Follow-up Planner | Time- and event-based reminders | `followup_queue.csv` |
| Reply Router | Classifier + next-best-action recommender | `reply_routing_queue.csv` |
| Nurture | Long-cycle warming | `nurture_queue.csv` |
| Partner / Referral | Co-sell, intro requests | `partner_referral_queue.csv` |
| ABM Strategic Account | Bespoke top-tier plays | `abm_account_queue.csv` |
| Proof-to-Demand | Route approved proofs to demand triggers | `proof_to_demand_queue.csv` |

Detailed specs in the per-machine files alongside this one.

## 4. Trust contract

- **No external send happens here.** Every queue is review-only.
- **Suppression list honoured.** A suppressed account is dropped before the queue.
- **Bilingual.** AR + EN drafts produced together.
- **Brand-checked.** Brand Guardian validates every draft against `DEALIX_BRAND_VOICE.md`.

## 5. KPIs

| KPI | Target |
|---|---|
| Reply rate per sector | tracked, no fixed target |
| Cash-to-send ratio (SAR per draft sent) | tracked weekly |
| Suppression honour rate | 100 % |
| Draft brand-pass rate | ≥ 95 % |
| Approval latency (founder) | ≤ 24 h |

## 6. Failure modes & recovery

| Failure | Recovery |
|---|---|
| Brand check fails | Draft rejected, returned to agent with diff |
| Suppression list breached | Draft blocked at queue; audit event |
| Approval latency exceeded | Daily brief escalation |
| Reply router mis-classifies | Operator override, fed back to learning loop |

## 7. Owners

- **Distribution Operator** agent — orchestration.
- **Brand Guardian** — copy gate.
- **Trust Guardian** — suppression and consent.
- **Founder** — final approval.
