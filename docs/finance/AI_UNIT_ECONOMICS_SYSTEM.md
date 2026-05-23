# AI Unit Economics System

The AI Unit Economics System measures the marginal cost of every AI action Dealix takes, so that pricing, agent design, and engagement scope reflect real inference economics rather than guesswork.

**Source of truth:** `$PRIVATE_OPS/ai_unit_economics.csv`
**Owner:** Founder + Engineering Lead
**Trust gate:** A1 — guardrails and budget changes are reviewed before activation.

## Units

| Unit | Definition |
|------|-----------|
| Run | One end-to-end agent invocation, from request to response |
| Token | LLM token (input + output) |
| Action | A discrete tool call (read, write, classify, generate) |
| Engagement-day | One day of active client work attributable to a client |

## Per-run cost record

Every run writes a row to `ai_unit_economics.csv`:

```
run_id, agent_id, client_id, started_at, ended_at,
input_tokens, output_tokens, tool_calls,
inference_cost_usd, gateway_cost_usd, infra_cost_usd,
total_cost_usd, total_cost_sar, approval_class, eval_passed
```

The LLM Gateway (`docs/06_llm_gateway/LLM_GATEWAY.md`) is the canonical source for token counts and inference cost.

## Per-client unit economics

A weekly job aggregates `ai_unit_economics.csv` into a per-client view:

- Runs per engagement-day.
- Cost per engagement-day.
- Cost per deliverable (sample, proposal, reply draft).
- Margin per engagement (revenue minus direct AI cost minus direct delivery cost).

If margin on any engagement drops below the floor defined in `docs/product/PRICING_GUARDRAILS.md`, the founder reviews scope or pricing.

## Guardrails

| Guardrail | Threshold | Action |
|-----------|-----------|--------|
| Per-run cost cap | 5.00 SAR | Run aborts with audit row |
| Per-client daily cap | configured per tier | Agent pauses; founder notified |
| Per-agent monthly cap | configured per agent | Agent pauses; founder notified |
| Inference outage | 3 failed calls in 60s | Agent fails closed; manual fallback |

Guardrails live in `policies/dealix_control_policy.yaml` and are enforced by the LLM Gateway COST_GUARD.

## Why this matters

Without per-run economics, an enthusiastic agent design can quietly burn the margin on a fixed-price engagement. The Unit Economics System makes the cost visible at the same cadence as revenue, so the founder can decide pricing, scope, and agent architecture with the same data the agents see.

## Failure modes

- **Missing cost field:** a run completes without a recorded inference cost. Detection: nightly job. Recovery: best-effort reconstruction from gateway logs; if unrecoverable, the engagement is flagged.
- **Cost spike:** per-run cost exceeds typical band by 5x. Detection: real-time alarm. Recovery: agent paused; founder reviews prompt and tool calls.
- **Allocation error:** a run is attributed to the wrong client. Detection: weekly reconciliation. Recovery: reattribute; audit row.

## Recovery path

If unit economics data becomes unreliable, the founder pauses non-essential agents until the data pipeline is restored. Pricing decisions revert to the published reference price; no custom pricing is issued without verified cost data.

## Metrics

- Median cost per run by agent.
- Median cost per engagement-day by tier.
- Margin by engagement (verified).
- Cost-spike incidents per week.

## Disclaimer

Unit economics are operational measurements. They are not financial-statement quality. Dealix does not guarantee any specific margin on any engagement. Estimated value is not Verified value.
