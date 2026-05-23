# Founder Interface Architecture

## Purpose
Define the internal founder-facing interface that lets Sami operate Dealix without manually reading CSVs, logs, or scattered reports.

## P0 Founder Routes

### /ceo
The executive command center.

### /sales-cockpit
Revenue funnel and conversion state.

### /approvals
All pending critical actions.

### /distribution
Channel and sector performance.

### /workers
Worker health and runtime status.

### /trust
Trust flags, policy escalations, suppression issues, AI risk.

### /finance
Cash, pipeline, payment capture, MRR, expenses.

## Design Principle
The founder interface should show decisions, not raw data.

## Every Page Must Have
- purpose
- source endpoint
- owner
- freshness timestamp
- trust status
- next action
- failure state

## Rule
If a page does not help Sami approve, decide, collect, deliver, or reduce risk, it is not P0.
