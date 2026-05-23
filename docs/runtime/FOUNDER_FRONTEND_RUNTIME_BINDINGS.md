# Founder Frontend Runtime Bindings

## Purpose

Map founder frontend pages to backend workers and data sources.

Every metric shown to the founder must be backed by:

1. A worker that computes it.
2. An endpoint that serves it.
3. A source of truth (database table, JSONL ledger, or audited file).

## `/ceo`

Source:

- CEO Summary Worker
- Certification Worker
- Trust Flags Worker

## `/sales-cockpit`

Source:

- Sales Funnel Worker
- Revenue Runtime Worker

## `/approvals`

Source:

- Approval Queue Worker
- Trust Policy Evaluator

## `/workers`

Source:

- Worker Health Worker
- Server Logs

## `/trust`

Source:

- Trust Flags Worker
- Suppression Worker
- Prompt/Output Verifier

## `/finance`

Source:

- Finance Summary Worker
- Payment Capture Worker

## `/distribution`

Source:

- Distribution Portfolio Worker
- Sector Scorecard Worker
- Experiment Engine

## Rule

Every frontend metric must have a worker, endpoint, and source of truth.

If a metric has no source of truth, it must not be rendered. A page may
render a `Connect data source` placeholder instead of fabricating a
value.
