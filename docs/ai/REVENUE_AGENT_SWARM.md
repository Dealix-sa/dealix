# Revenue Agent Swarm

> The set of AI agents that prepare revenue work for Dealix and route
> it through the trust plane.

## Purpose

Move revenue work from "founder writes everything by hand" to "founder
approves everything by hand" without ever crossing into "founder approves
nothing".

Every agent in the swarm is a **preparer**, not an executor. None of
them place an external action on their own. They produce structured
drafts that land in the appropriate queue, attach the evidence and risk
classification, and wait.

## Position in the Operating Layer

```
Revenue Runtime Layer
    │
    ├── Lead Research Agent      ─── enriches lead_intelligence
    ├── Lead Scoring Agent       ─── ranks leads for approval
    ├── Outreach Draft Agent     ─── creates outreach_queue rows
    ├── Follow-Up Planner        ─── schedules next touch
    ├── Reply Classifier         ─── routes conversation_log replies
    ├── Sample Draft Agent       ─── prepares sample packs
    ├── Proposal Draft Agent     ─── prepares proposal_queue rows
    └── Payment Follow-Up Agent  ─── prepares payment_capture_queue
            │
            ▼
        Trust Plane (Policy + Guardian)
            │
            ▼
        Founder Approval Queue
            │
            ▼
        Worker Executes External Action
```

## Agents

### Lead Research Agent
- **Scope:** finds and structures Saudi companies that match ICP.
- **Inputs:** ICP definition, sector lists, public registries, web
  search.
- **Output:** structured `lead_intelligence` row (company, sector,
  buyer role, Saudi context, source URLs).
- **Tool level:** T2 (draft) + T1 (read public sources).
- **Approval class:** A1 (internal only).

### Lead Scoring Agent
- **Scope:** scores ICP fit, sector relevance, buyer clarity, Saudi
  presence.
- **Inputs:** enriched lead, account history, prior outreach.
- **Output:** numeric score + reason codes + risk flags.
- **Tool level:** T1.
- **Approval class:** A1.

### Outreach Draft Agent
- **Scope:** writes bilingual (AR + EN) first-touch outreach drafts.
- **Inputs:** scored lead, sector playbook, sample artifacts, prior
  conversations on this account.
- **Output:** draft row in `outreach_queue` with `state = pending_approval`.
- **Tool level:** T3 (queue write).
- **Approval class:** A2.
- **Hard constraints:**
  - No revenue guarantees.
  - No fabricated client logos.
  - No claims that have not been pre-approved.
  - Must include at least one piece of evidence (sample, sector report,
    case study).

### Follow-Up Planner
- **Scope:** decides when and how to follow up on a sent outreach with
  no reply.
- **Inputs:** outreach history, reply state, sector cadence.
- **Output:** scheduled follow-up draft in `outreach_queue`.
- **Tool level:** T3.
- **Approval class:** A2.

### Reply Classifier
- **Scope:** routes inbound replies into one of:
  positive / sample / proposal / objection / nurture / lost / manual.
- **Inputs:** conversation_log entry, account history.
- **Output:** route label + suggested next step + confidence.
- **Tool level:** T1.
- **Approval class:** A1.
- **Failure mode:** confidence below threshold → route = manual.

### Sample Draft Agent
- **Scope:** assembles a sample pack tailored to the prospect's
  sector/use case.
- **Inputs:** sample library, prospect context, prior conversation.
- **Output:** sample pack draft + cover note in `outreach_queue`.
- **Tool level:** T3.
- **Approval class:** A2.

### Proposal Draft Agent
- **Scope:** drafts a structured proposal (scope, deliverables, price,
  timeline, exclusions).
- **Inputs:** approved pricing matrix, reply history, sample pack,
  contract template.
- **Output:** proposal draft in `proposal_queue`.
- **Tool level:** T3.
- **Approval class:** A2.
- **Hard constraints:**
  - Price must come from the approved pricing matrix.
  - Discounts beyond matrix → A3 (manual only).
  - No verbal commitments → contract template only.

### Payment Follow-Up Agent
- **Scope:** prepares payment / PO / written approval follow-up.
- **Inputs:** proposal state, payment_capture_queue, prior reminders.
- **Output:** follow-up draft + suggested channel.
- **Tool level:** T3.
- **Approval class:** A2.

## Required Controls (All Agents)

Every agent in the swarm must declare and pass:

1. **Output contract** — JSON schema validated before queue write.
2. **Approval class** — set explicitly; never inferred at runtime.
3. **Evidence attached** — at least one source link or doc id.
4. **No-overclaim scan** — automated check for banned phrasing
   (guarantee, ensure ROI, fake metrics, fake logos).
5. **Suppression check** — recipient must not be on DNC/PDPL/bounce
   list at draft time *and* at approval time.
6. **Audit path** — every draft writes a `revenue_agent.draft` event.
7. **Kill switch** — each agent has a config-file flag that disables
   it without redeploy.

## Rule

> Agents prepare. Founder approves. Workers execute.

No agent in this swarm sends, posts, signs, charges, or publishes. The
nearest equivalent it can do is "request execution" by writing a row
into a queue that a human-approved worker drains.

## Failure Modes

| Mode | Detection | Response |
|------|-----------|----------|
| Output contract violation | JSON validation | Reject draft, log + alert |
| Banned phrasing | No-overclaim scanner | Reject draft, return to revise |
| Suppression hit | Suppression list lookup | Block, log, never re-attempt |
| Cost spike | AI Unit Economics monitor | Auto-throttle agent + alert |
| Eval regression | CI eval suite | Block deploy |

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`TRUST_GUARDIAN_AGENT`](TRUST_GUARDIAN_AGENT.md)
- [`EVAL_RED_TEAM_SYSTEM`](EVAL_RED_TEAM_SYSTEM.md)
- [`AI_UNIT_ECONOMICS_SYSTEM`](../finance/AI_UNIT_ECONOMICS_SYSTEM.md)
- [`POLICY_AS_CODE_SYSTEM`](../trust/POLICY_AS_CODE_SYSTEM.md)
