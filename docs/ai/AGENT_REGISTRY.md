# Agent Registry

All Dealix AI agents are registered here. Every agent declares:
scope, tools, data access, output contract, approval class, eval
suite, kill switch, audit path, owner, allowed write targets,
never-auto actions.

| Agent ID | Doc | Owner | Approval class |
|---|---|---|---|
| `brand_guardian` | [BRAND_GUARDIAN_AGENT.md](BRAND_GUARDIAN_AGENT.md) | content_strategist | Internal |
| `growth_strategist` | [GROWTH_STRATEGIST_AGENT.md](GROWTH_STRATEGIST_AGENT.md) | founder | Recommendation |
| `distribution_operator` | [DISTRIBUTION_OPERATOR_AGENT.md](DISTRIBUTION_OPERATOR_AGENT.md) | founder | per-message |
| `content_strategist` | [CONTENT_STRATEGIST_AGENT.md](CONTENT_STRATEGIST_AGENT.md) | founder | per-slot |
| `offer_architect` | [OFFER_ARCHITECT_AGENT.md](OFFER_ARCHITECT_AGENT.md) | founder | per-proposal |
| `performance_analyst` | [PERFORMANCE_ANALYST_AGENT.md](PERFORMANCE_ANALYST_AGENT.md) | founder | Recommendation |
| `ceo_copilot` | (uses growth + performance outputs) | founder | Recommendation |
| `trust_guardian` | [TRUST_GUARDIAN_AGENT.md](TRUST_GUARDIAN_AGENT.md) | founder + security | Block |
| `eval_guardian` | [EVAL_RED_TEAM_SYSTEM.md](EVAL_RED_TEAM_SYSTEM.md) | security_guardian | Gate |
| `finance_copilot` | (uses payment register + ZATCA) | finance | per-invoice |
| `delivery_copilot` | (uses delivery register) | founder | per-artifact |
| `security_guardian` | (red-team + policy-as-code) | security | Block |

## Universal agent contract

Every entry above MUST honour:

1. No external action without an approval row.
2. No write outside `allowed_write_targets`.
3. Eval suite executed before deploy.
4. Kill switch wired up.
5. Audit row per run.
6. Never-auto actions listed and enforced by trust_guardian.

## Registry verification

`scripts/verify_growth_system.py` and `scripts/verify_brand_growth_operating_layer.py`
load this file and check that each agent's doc exists and contains
the required sections.
