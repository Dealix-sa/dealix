# AI Unit Economics System

> Measure whether AI usage at Dealix improves revenue, speed, quality,
> or founder leverage — and shut it down when it doesn't.

## Purpose

AI is a cost line, not a free utility. Every agent invocation, every
embedding, every eval run shows up on the credit card. The Unit
Economics system answers a single question:

> Is each dirham of AI spend producing more dirhams of revenue, hours
> of founder time, or quality improvement than the next-best alternative?

If the answer is "no" for an agent, we shrink its scope, swap its
model, or remove it.

## Position in the Operating Layer

Unit Economics sits inside the Observability Layer and feeds the
Founder Control Layer (`/finance` and `/workers`).

```
Agents + Workers
     │  (cost events, outcome events)
     ▼
AI Unit Economics Aggregator
     │
     ├── /finance — cost per outcome panel
     └── /workers — per-agent cost row
```

## Metrics

| Metric | Numerator | Denominator | Owner |
|--------|-----------|-------------|-------|
| AI cost per lead | AI spend across research + scoring agents | New `lead_intelligence` rows | Lead Research Agent |
| AI cost per enriched lead | Spend on enrichment models | Leads enriched | Lead Research Agent |
| AI cost per approved outreach | Spend on outreach + guardian | Outreach rows reaching `approved` | Outreach Draft Agent |
| AI cost per positive reply | Outreach + classification spend | Replies labeled `positive` / `sample` / `proposal` | Reply Classifier |
| AI cost per sample sent | Sample drafting + guardian spend | Samples reaching `approved` | Sample Draft Agent |
| AI cost per proposal sent | Proposal drafting + guardian + pricing checks | Proposals reaching `approved` | Proposal Draft Agent |
| AI cost per paid client | Full AI spend in window | Customers with payment captured | Founder |
| Hours saved | Estimated manual time saved (per task class × volume) | — | Founder |
| Quality score improvement | Eval score Δ vs baseline | — | Eval System |

## Cost Event Schema

Every AI invocation emits a `cost_event`:

```json
{
  "event_id": "uuid",
  "ts": "ISO-8601",
  "agent_id": "string",
  "model_id": "string",
  "input_tokens": 0,
  "output_tokens": 0,
  "tool_calls": 0,
  "usd_cost": 0.0,
  "outcome_id": "optional id tying this call to a downstream outcome",
  "outcome_kind": "lead | outreach | reply | sample | proposal | payment | other"
}
```

Outcome events (`outreach.approved`, `payment.captured`, etc.) carry an
`outcome_id` that joins back to the cost events that produced them.

## Aggregation Window

- Default: rolling 7-day and 30-day windows.
- Pricing changes (model swap, prompt rewrite, new tool): reset the
  window for that agent, mark the cutover in the panel.

## Rule

> If AI cost rises without a matching improvement in conversion,
> speed, quality, or founder leverage, **reduce scope or reroute**.

Reroute options, in order of preference:

1. Smaller model with the same prompt.
2. Cached / templated path with no model call.
3. Deterministic logic that doesn't need AI at all.
4. Remove the agent.

## Failure Modes

| Mode | Detection | Response |
|------|-----------|----------|
| Cost spike per agent | 24h cost > 3× 7d median | Auto-throttle the agent, alert founder |
| No outcome attribution | Cost events lack `outcome_id` | Block the agent from production until fixed |
| Outcome without cost | Outcome events with no matching cost | Pipeline bug — open an incident |
| Quality drop with cost up | Eval Δ negative + cost Δ positive | Block model swap, revert |

## Implementation Notes

- Cost events are append-only.
- A small worker (`ai_cost_aggregator`) folds events into the
  per-agent / per-outcome panels every 5 minutes.
- The aggregator publishes a daily digest into `/finance` and
  `/workers`.

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`REVENUE_AGENT_SWARM`](../ai/REVENUE_AGENT_SWARM.md)
- [`WORKER_ORCHESTRATOR_V1`](../runtime/WORKER_ORCHESTRATOR_V1.md)
- [`CEO_COPILOT_SYSTEM`](../ai/CEO_COPILOT_SYSTEM.md)
