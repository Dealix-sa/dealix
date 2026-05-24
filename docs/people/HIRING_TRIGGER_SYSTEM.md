# Hiring Trigger System

Hire when a quantitative trigger fires, not when it "feels" time. The
triggers below are the only acceptable reasons to start a hiring process
inside the CEO layer.

## Triggers

| Trigger | Threshold | Suggested role |
|---|---|---|
| Sustained CEO Make hours | ≥ 20 hrs/wk for 3 consecutive weeks | Contractor for the dominant task |
| Approval queue backlog | > 24 hours latency for 2 weeks | Trust / QA reviewer |
| Delivery handoffs missed | ≥ 1 in a 4-week window | Delivery coordinator |
| Active paid customers | ≥ 5 | Customer success operator |
| Sample throughput plateau | < target for 2 consecutive weeks | Sales asset designer |
| Pipeline data hygiene drift | Source-freshness SLA breach in 2 weeks | Data ops assistant |

## Process

1. Trigger fires → daily brief flags it
2. Walk [`docs/finance/HIRE_VS_AUTOMATE_VS_PARTNER.md`](../finance/HIRE_VS_AUTOMATE_VS_PARTNER.md)
3. If "hire" wins → write a 5-line role spec (existing format: [`docs/commercial/operations/DELIVERY_OPERATOR_HIRE_SPEC_AR.md`](../commercial/operations/DELIVERY_OPERATOR_HIRE_SPEC_AR.md))
4. Log the decision in [`docs/founder/DECISION_LOG_SYSTEM.md`](../founder/DECISION_LOG_SYSTEM.md) with `type: hire`
5. Source: contractor first, full-time after 60-day trial

## Cross-references

- [`docs/finance/HIRE_VS_AUTOMATE_VS_PARTNER.md`](../finance/HIRE_VS_AUTOMATE_VS_PARTNER.md)
- [DELEGATION_SYSTEM](DELEGATION_SYSTEM.md)
- [`docs/founder/DELEGATION_DECISION_TREE.md`](../founder/DELEGATION_DECISION_TREE.md)

## Non-negotiables

Hiring decisions are logged. Pay terms with hires are recorded but never
exposed externally. See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
