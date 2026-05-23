# Ultimate Data Platform

The data platform has three tiers:

1. **Operational** (`$DEALIX_PRIVATE_OPS/...csv`) — single-tenant runtime.
2. **Analytical** (`data/`, `analytics/`) — read-mostly aggregates.
3. **Audit** (`trust/approval_decisions.csv`) — immutable append-only.

The Founder Console reads from tier 1 directly. Tier 2 and 3 are fed
by workers and never written from the UI.
