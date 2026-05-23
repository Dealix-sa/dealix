# Revenue KPI Tree

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Driven by Growth.

This document is the canonical KPI tree from raw pipeline through to
cash collected. It is the reference structure that the Performance
Analyst, the Growth Strategist, the Finance Copilot, and the founder
use to reason about the revenue motion. Each node names a metric, the
source data, and the agent responsible for keeping the number
honest.

## The tree

```
Cash Collected (SAR)
└── Invoiced Revenue (SAR)
    └── Won Deal Value (SAR)
        ├── Pipeline Value (SAR)
        │   ├── Qualified Opportunities (count, SAR)
        │   │   ├── Engaged Conversations (count)
        │   │   │   ├── Replies (count)
        │   │   │   │   └── Drafts Sent After Approval (count)
        │   │   │   │       └── Drafts Queued (count)
        │   │   │   │           └── Targets Reached (count)
        │   │   │   │               └── Accounts in ICP (count)
        │   │   │   │                   └── Sector Targets (count)
        │   │   │   └── Reply Quality Index (0..1)
        │   │   └── Qualification Rate (engaged → qualified)
        │   └── Proposal Sent (count, SAR)
        ├── Win Rate (proposal → won, %)
        └── Average Deal Size (SAR)
└── Cash Conversion Days (days from invoice to cash)
```

## Node-level reference

Each node lists:

- **Metric**: the precise definition.
- **Source**: the runtime CSV or API surface.
- **Owner**: the accountable agent.
- **Cadence**: refresh frequency.
- **Diagnostic moves**: what to look at when this node moves.

### Sector Targets

- Metric: count of active sector priorities in the portfolio.
- Source: `growth/sector_targets.csv`.
- Owner: growth_strategist.
- Cadence: monthly.
- Moves: rebalance based on win rate and AI unit economics by sector.

### Accounts in ICP

- Metric: count of accounts that pass the ICP filter.
- Source: `growth/account_scores.csv` filtered by `score >= threshold`.
- Owner: growth_strategist.
- Cadence: weekly.
- Moves: tighten the ICP, add or remove a sector, rescore accounts.

### Targets Reached

- Metric: count of targets that received any contact attempt in the
  period.
- Source: `outreach/conversation_log.csv` distinct on `lead_id`.
- Owner: distribution_operator.
- Cadence: daily.
- Moves: review channel mix; check suppression hit rate.

### Drafts Queued

- Metric: count of outreach drafts written to the queue.
- Source: `outreach/outreach_queue.csv`.
- Owner: distribution_operator.
- Cadence: daily.
- Moves: check eval gate pass rate; check Brand Guardian rejections.

### Drafts Sent After Approval

- Metric: count of drafts that received a founder approval and were
  released to the external worker.
- Source: `trust/approval_decisions.csv` filtered to
  `action: approval_approve` and `target` prefix matching draft ids.
- Owner: founder.
- Cadence: daily.
- Moves: bottleneck analysis; the founder is the limit by design.

### Replies

- Metric: count of replies recorded against drafted contacts.
- Source: `outreach/conversation_log.csv` filtered to reply events.
- Owner: distribution_operator.
- Cadence: daily.
- Moves: review hook quality, reply playbooks, sample relevance.

### Reply Quality Index

- Metric: a 0..1 score based on intent classification of replies.
- Source: `outreach/reply_routing_queue.csv` enriched with intent.
- Owner: performance_analyst.
- Cadence: weekly.
- Moves: improve qualification questions; rewrite the hook.

### Engaged Conversations

- Metric: count of distinct conversations that progressed past the
  reply stage.
- Source: `outreach/conversation_log.csv` filtered to
  `stage in [engaged, qualified, proposal_sent, negotiation, won]`.
- Owner: distribution_operator.
- Cadence: daily.

### Qualified Opportunities

- Metric: count and pipeline value of qualified opportunities.
- Source: `outreach/conversation_log.csv` joined with `sales/proposal_queue.csv`.
- Owner: performance_analyst.
- Cadence: daily.
- Moves: tighten qualification criteria; review proposal time-to-send.

### Qualification Rate

- Metric: engaged → qualified conversion.
- Source: derived from `outreach/conversation_log.csv`.
- Owner: performance_analyst.
- Cadence: weekly.

### Proposal Sent

- Metric: count and aggregate proposal value.
- Source: `sales/proposal_queue.csv` filtered to `status: sent`.
- Owner: delivery_copilot.
- Cadence: daily.

### Pipeline Value

- Metric: SAR sum of open proposals weighted by stage.
- Source: `sales/proposal_queue.csv`.
- Owner: delivery_copilot.
- Cadence: daily.

### Win Rate

- Metric: won / proposal_sent.
- Source: `sales/proposal_queue.csv` over a 30/60/90 day window.
- Owner: performance_analyst.
- Cadence: weekly.
- Moves: pricing review, sample sprint scope review, objection
  pattern review (see `OBJECTION_ANALYTICS.md`).

### Average Deal Size

- Metric: SAR mean of won deal values in window.
- Source: `sales/proposal_queue.csv` filtered to `status: won`.
- Owner: performance_analyst.
- Cadence: weekly.

### Won Deal Value

- Metric: SAR sum of `status: won`.
- Source: `sales/proposal_queue.csv`.
- Owner: founder.
- Cadence: weekly.

### Invoiced Revenue

- Metric: SAR sum on `finance/payment_capture_queue.csv` (issued).
- Source: `finance/payment_capture_queue.csv`.
- Owner: finance_copilot.
- Cadence: weekly.

### Cash Collected

- Metric: SAR sum on `finance/cash_collected.csv`.
- Source: `finance/cash_collected.csv`.
- Owner: finance_copilot.
- Cadence: daily.

### Cash Conversion Days

- Metric: median days between invoice issue and cash collection.
- Source: joined `finance/payment_capture_queue.csv` and
  `finance/cash_collected.csv` on invoice number.
- Owner: finance_copilot.
- Cadence: weekly.
- Moves: review payment terms; review collection cadence.

## Cross-cuts: cost and unit economics

Two cross-cut nodes apply at every level:

| Cross-cut                | Metric                                                  | Source                          |
| ------------------------ | ------------------------------------------------------- | ------------------------------- |
| AI cost per deal         | USD AI spend / deals supported                          | `finance/ai_unit_economics.csv` |
| Gross margin per deal    | (won value SAR - delivery cost SAR - AI cost SAR) / won | derived                         |

The AI cost cross-cut is documented in detail in
`AI_UNIT_ECONOMICS_SYSTEM.md`.

## Sector and channel cuts

The same tree is cut by sector and by channel.

| Cut       | CSV                                          |
| --------- | -------------------------------------------- |
| Sector    | `distribution/sector_scorecard.csv`          |
| Channel   | `distribution/channel_scorecard.csv`         |
| Offer rung| `product/product_distribution.csv`            |

## Diagnostic walk

A monthly performance review walks the tree top down:

1. Is cash collected on plan?
2. If not, is invoiced revenue on plan?
3. If not, are won deal value and cash conversion days on plan?
4. Is the win rate stable? If it dropped, look at proposal_sent
   quality, sample sprint outcomes, and pricing pressure.
5. Is pipeline value stable? If it dropped, walk into qualification
   rate and reply quality.
6. Is targets reached on plan? If not, look at suppression hit rate
   and eval gate rejections.
7. Is ICP stable? Is sector portfolio rebalancing required?

The diagnostic moves at each level are documented in
`CONVERSION_DIAGNOSTICS.md`.

## Founder Console exposure

The KPI tree is not surfaced as a single endpoint today. The four
pillar scorecard (`/control/scorecard`) is the founder-facing view;
the sales funnel (`/sales/funnel`), distribution summary, finance
summary, and finance-ops summary each cover a subset.

## Discipline

- No KPI is reported without a source CSV. No source CSV, no KPI.
- No KPI is celebrated without a hypothesis. Numbers that move
  unexpectedly are diagnosed, not bragged about.
- No KPI is reported externally. The tree is operational. External
  claims must trace to the proof library, not to the tree.
