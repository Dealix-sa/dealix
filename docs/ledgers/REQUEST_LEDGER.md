# Request Ledger

Every inbound request gets a row **before** execution. IDs: `R-###`.

## Request types

```text
Sales
Client Change
Feature Request
Governance Question
Support Issue
Partnership
Enterprise
```

## Decision outcomes

```text
Accept
Qualify
Offer Diagnostic
Redirect
Add to Backlog
Reject
Block
```

| ID | Date | Source | Request | Type | Fit | Risk | Decision | Owner | Next Action |
|----|------|--------|---------|------|----:|------|----------|-------|-------------|
| _(empty — launch start: no inbound requests recorded yet)_ | | | | | | | | | |

**Rule:** no work without a **Decision** cell filled. Link to [`DECISION_LEDGER.md`](DECISION_LEDGER.md) when material.
