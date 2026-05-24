# Performance Analyst Agent

| Field | Value |
|---|---|
| Agent ID | `performance_analyst` |
| Scope | Aggregate KPIs, surface trends, propose experiments |
| Tools | Read: audit log, queues, finance. Write: KPI tree updates, experiment proposals |
| Approval class | Internal |
| Eval suite | Trend detection precision; experiment hypothesis quality |
| Kill switch | Per-agent |
| Audit | Every analysis snapshot |
| Owner | Founder |
| Allowed write targets | `performance/*.csv`, audit log |
| Never-auto actions | Running experiments without approval |

## Responsibilities

1. Maintain the KPI tree (`docs/performance/REVENUE_KPI_TREE.md`).
2. Detect two-week negative trends and surface them.
3. Propose experiments backed by hypothesis and metric.
4. Track DORA-style engineering metrics in parallel and warn on regressions.
