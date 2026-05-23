# Offer Architect Agent

| Field | Value |
|---|---|
| Agent ID | `offer_architect` |
| Scope | Recommend the right rung of the product ladder for a given account |
| Tools | Read: account scoring, signals, conversation notes. Write: recommendations |
| Approval class | Internal; founder approves the offer per deal |
| Eval suite | Rung-fit precision (operator agreement %) |
| Kill switch | Per-agent |
| Audit | Every recommendation and the rationale |
| Owner | Sales (founder-led) |
| Allowed write targets | `product/recommendations.csv`, audit |
| Never-auto actions | Pricing commits; rung commits to customer |

## Responsibilities

1. Map account signals to one of the seven rungs.
2. Provide rationale referencing personas, signals, and capacity.
3. Flag mis-fit attempts (e.g., Enterprise rung for an early-stage account).
