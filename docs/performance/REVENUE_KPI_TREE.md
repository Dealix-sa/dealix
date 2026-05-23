# Revenue KPI Tree

The Revenue KPI Tree is the single hierarchical view of how revenue is produced. Every node is measured. Every parent equals (approximately) the sum or product of its children. A node that does not connect to a parent does not belong on the tree.

**Source of truth:** `$PRIVATE_OPS/kpi_tree_state.csv`
**Owner:** Founder
**Trust gate:** A1 — node definition changes are reviewed monthly.

## Tree (top-down)

```
Cash collected (verified)
└── Invoices cleared
    └── Invoices issued
        └── Contracts signed
            └── Proposals accepted
                └── Proposals sent
                    └── Replies received
                        └── Conversations held
                            └── Outreach sent
                                └── Targeted contacts
                                    └── Sourced signals
```

## Node specifications

| Node | Definition | Source CSV | Cadence |
|------|-----------|------------|---------|
| Sourced signals | Inbound or sourced opportunities entering the factory | `signals.csv` | Daily |
| Targeted contacts | Signals where a named contact has been identified | `signals.csv` | Daily |
| Outreach sent | Approved sends through allowed channels | `email_outreach_log.csv` + `linkedin_outreach_log.csv` | Daily |
| Conversations held | A live exchange (call, DM thread) with two-way response | `conversations_log.csv` | Daily |
| Replies received | Inbound replies tied to outreach | `reply_routing_log.csv` | Daily |
| Proposals sent | Proposals at Proposal Factory stage 5 | `proposal_factory_state.csv` | Daily |
| Proposals accepted | Proposals at Proposal Factory stage 6 | `proposal_factory_state.csv` | Daily |
| Contracts signed | Executed contracts | `revenue_factory_state.csv` | Daily |
| Invoices issued | Per `docs/finance/PAYMENT_CAPTURE_OS.md` | `payments_ledger.csv` | Daily |
| Invoices cleared | Cleared payments | `payments_ledger.csv` | Daily |
| Cash collected | Verified cash | `finance_ledger.csv` | Daily |

## Read pattern

Each node reports:

- Current value (this week).
- Prior value (last week).
- Trailing 7-day median.
- Conversion to parent (child / parent ratio, estimated).
- Outliers (rows that disproportionately moved the number).

## Connection to the Conversion Diagnostics

When a parent moves, the Diagnostics layer (`docs/performance/CONVERSION_DIAGNOSTICS.md`) traces which child explains most of the movement. The combination of Tree + Diagnostics is the closed-loop measurement system.

## Failure modes

- **Node drift:** a node's definition changes without source update. Detection: weekly diff. Recovery: source update or revert definition.
- **Phantom node:** a node exists in the tree but no CSV writes to it. Detection: source audit. Recovery: implement source or remove node.
- **Double counting:** a row counts in two nodes. Detection: cross-check. Recovery: deduplicate; root cause filed.

## Recovery path

If tree integrity is in doubt, the founder freezes new performance reads and reconciles each node against its source.

## Metrics about the tree

- Node coverage (each node has a source).
- Computation lag (median hours from source row to tree value).
- Discrepancy incidents per quarter.

## Disclaimer

The Tree describes the factory. It does not promise that the factory will produce a specific number. Cash is Verified; all upstream nodes are Estimated. Estimated value is not Verified value.
