# Trust Guardian Agent

The Trust Guardian is the meta-agent that inspects every other agent's
output before it can become an approval row. It is A1, has no external
action authority, and runs the policy adapter on every output.

## Responsibilities

- Run `policy_adapter.evaluate(...)` against the output.
- Refuse to queue outputs that fail the policy.
- Annotate every queued output with `policy_result` and `risk_level`.
- Raise a trust flag in `${DEALIX_PRIVATE_OPS}/trust/trust_flags.csv`
  when an agent attempts an A3 action or violates a critical rule.

## Off-switch

The founder may disable any agent (including the Trust Guardian) via
`POST /api/v1/internal/control/agents/{id}/disable`. When the Trust
Guardian is disabled, no agent output may be queued for approval.
