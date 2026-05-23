# Autonomous Distribution Machines

**Owner:** Founder + Operations
**Source of truth:** This doc + `docs/growth/DISTRIBUTION_WAR_MACHINE.md`

## Purpose

This is the master index of Dealix's distribution machines and the orchestration rules that connect them. Each machine has its own doc with full operating spec. This index defines how they relate, where data flows between them, and what coordination rules prevent collision.

The word "autonomous" here means: the machine runs on a defined schedule without a human prompt to start each cycle. It does NOT mean the machine takes external action without approval. Every machine produces queued output that passes a trust gate before any external send.

## The 12 machines and their relationships

```
Intelligence Layer
   │
   ├─► Account Scoring → Trigger Event System
   │                          │
   │                          ▼
   │                    ABM Strategic Account Machine
   │                          │
   │                          ▼
   │   ┌──────────────────────┴──────────────────────┐
   │   │                                             │
   │   ▼                                             ▼
   │  Outbound Draft Machine             Partner Referral Machine
   │   │                                             │
   │   ├─► LinkedIn Queue Machine                    │
   │   ├─► Email Draft Machine                       │
   │   └─► Contact Form Queue Machine                │
   │           │                                     │
   │           ▼                                     ▼
   │       Approval Gate (A2) ◄──────────────────────┘
   │           │
   │           ▼
   │       Sanctioned Send
   │           │
   │           ▼
   │       Reply Router Machine
   │       ├─► Hot reply → Founder direct
   │       ├─► Warm reply → Follow-Up Machine
   │       └─► No-reply → Nurture Machine
   │
   └─► Content to Demand Engine ──► Proof to Demand Machine
                                    (feeds Nurture + Outbound)
```

## Machine roster

| Machine | What it produces | Approval class | KPI |
|---|---|---|---|
| Outbound Draft Machine | Persona-tailored outreach drafts | A2 | Drafts/day; approval rate |
| LinkedIn Queue Machine | Queued LinkedIn DMs | A2 | Queue throughput; send-to-reply ratio |
| Email Draft Machine | Queued warm emails | A2 | Draft-to-send ratio |
| Contact Form Queue Machine | Inbound triage + auto-acknowledge | A1 intake / A2 reply | Response time |
| Follow-Up Machine | Scheduled follow-up reminders + drafts | A2 | Follow-up completion rate |
| Reply Router Machine | Reply classification + routing | A1 | Routing accuracy; hot-reply latency |
| Nurture Machine | Long-cycle touchpoints | A2 | Nurture-to-meeting conversion |
| Partner Referral Machine | Inbound from partners | A1 intake / A2 reply | Partner-sourced sprint volume |
| ABM Strategic Account Machine | Per-account playbook orchestration | A2 | Account penetration depth |
| Proof to Demand Machine | Anonymized proof distribution | A2 | Proof-driven reply lift |
| Content to Demand Engine | Sector signal content production | A1 publish / A3 external | Content-to-inbound conversion |
| Channel Portfolio System | Channel-level health and capacity | — | Channel health score |

## Orchestration rules

### Rule 1 — One open thread per persona at a time

If the LinkedIn Queue Machine has an open thread with a persona, the Email Draft Machine does not open a new email thread with the same persona until the LinkedIn thread closes or stalls (no reply for 21 days). Saturation reads as spam and is forbidden.

### Rule 2 — Approval queue capacity gating

The Outbound Draft Machine generates no more drafts than the founder's approval throughput can absorb. If the queue exceeds 2x daily approval capacity, the machine slows to a sustainable rate.

### Rule 3 — Reply Router has right-of-way

When a reply lands, every other machine pauses outreach to that persona until the Reply Router classifies the reply and routes it. New drafts to a replying persona are blocked at the queue level.

### Rule 4 — Nurture and Outbound do not overlap

A persona in active Nurture cadence is not eligible for new Outbound Draft Machine output. The Nurture Machine is a separate motion with its own pacing.

### Rule 5 — Proof to Demand respects anonymization

The Proof to Demand Machine references Proof Pack outputs only after they have been anonymized and signed off by the Founder (A2/A3 per gate).

### Rule 6 — Channel Portfolio sets the capacity envelope

If a channel's health score (deliverability, response rate, account-flag rate) drops below threshold, the Channel Portfolio System pauses that channel and notifies the Founder. Other machines must adapt.

## Coordination on a single account

For a single Tier-A account in one quarter, the total Dealix touch volume is capped at:

- 2 Outbound first-touches (across all channels)
- 3 Follow-ups
- 1 Nurture touch every 30 days (if no active thread)
- 1 Partner-referred touch (independent)
- 1 Proof-driven touch (when relevant Proof Pack publishes)

Total cap: ~10 distinct touches per quarter, per account. Beyond this, the account is in Nurture-only mode.

## Trust gates summary

All distribution machines obey `docs/05_governance_os/APPROVAL_POLICY.md`. Approval classes:

- A0 — Self-approval (internal drafts only)
- A1 — Operator approval (intake, routing, internal publication)
- A2 — Founder + Operator approval (any customer-facing external action)
- A3 — Founder-only approval (press, public-facing claims)

## Failure mode

- Two machines fire on the same persona in the same week.
- The Reply Router fails to pause adjacent machines.
- Approval queue overflows; drafts age out.
- A machine adopts a channel not in the Portfolio whitelist.

## Recovery path

1. Pause the over-firing machines.
2. Audit and apologize where appropriate.
3. Re-enforce orchestration rules at the queue layer.
4. Re-train operators on the cap rules.

## Cross-links

Each machine has its own doc in `docs/growth/`:

- `OUTBOUND_DRAFT_MACHINE.md`
- `LINKEDIN_QUEUE_MACHINE.md`
- `EMAIL_DRAFT_MACHINE.md`
- `CONTACT_FORM_QUEUE_MACHINE.md`
- `FOLLOW_UP_MACHINE.md`
- `REPLY_ROUTER_MACHINE.md`
- `NURTURE_MACHINE.md`
- `PARTNER_REFERRAL_MACHINE.md`
- `ABM_STRATEGIC_ACCOUNT_MACHINE.md`
- `PROOF_TO_DEMAND_MACHINE.md`
- `CONTENT_TO_DEMAND_ENGINE.md`
- `CHANNEL_PORTFOLIO_SYSTEM.md`

## Disclaimer

Dealix does not guarantee meetings, replies, or revenue from any machine. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
