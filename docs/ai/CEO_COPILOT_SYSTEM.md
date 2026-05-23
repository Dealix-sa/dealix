# CEO Copilot System

The CEO Copilot is the founder's view into Dealix runtime. It surfaces the day's decisions, the week's KPIs, and the open approvals that need the founder's eyes. It does not act on the founder's behalf.

**Source of truth:** `registries/agent_registry.yaml` entry `ceo_copilot`
**Owner:** Founder
**Trust gate:** A2 — the Copilot surfaces approvals; the founder approves.

## Spec

| Field | Value |
|-------|-------|
| `id` | `ceo_copilot` |
| `name` | CEO Copilot |
| `purpose` | Surface decisions, KPIs, and pending approvals for founder review |
| `approval_class_max` | A1 |
| `tools` | `read_factory_state`, `read_performance_reads`, `read_approval_queue`, `read_risk_register`, `write_brief` |
| `outputs` | `daily_briefing`, `weekly_digest`, `approval_summary` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | founder |
| `allowed_write_targets` | `$PRIVATE_OPS/copilot_briefs/` |

## Surfaces

| Surface | Cadence |
|---------|---------|
| Daily briefing | Mornings — 8 sections, 1 page total |
| Weekly digest | Mondays — KPI tree, top risks, decisions made |
| Approval summary | Real-time queue, scoped to founder-only decisions |

## Daily briefing structure

1. Headline movement of the day.
2. Cash position vs runway.
3. Active engagements with watch / at-risk Health Scores.
4. Open A2 approvals.
5. Eval failures in the last 24 hours.
6. Cost-guardrail breaches in the last 24 hours.
7. One recommended decision with supporting evidence.
8. One observation worth thinking about.

Bilingual: EN with AR summary for sections 1, 2, and 4.

## What the Copilot does not do

- It does not approve.
- It does not send.
- It does not change pricing, scope, contract, refund, payment terms.
- It does not publish.

## OWASP LLM Top 10 posture

- **Excessive agency (LLM08).** Tools list contains read-only and one write target (the brief file). No action tools.
- **Insecure plugin design (LLM07).** The Copilot does not have plugins. Tools are first-class registered.
- **Sensitive information disclosure (LLM06).** Briefs are written to a directory accessible only to the founder.

## Eval

- KPI accuracy: spot-checked against source.
- Approval coverage: every founder-only pending decision appears.
- No-guarantee language.
- Bilingual parity on flagged sections.

## Failure modes

- **Missed approval:** an A2 decision pending more than 48 hours does not appear. Detection: queue audit. Recovery: surface immediately; root cause filed.
- **KPI mismatch:** Copilot reports a number that differs from source. Detection: cross-check. Recovery: refresh; founder notified of stale state.
- **Action attempt:** the Copilot attempts a tool not in its allowlist. Detection: policy engine. Recovery: deny, audit.

## Recovery path

If the Copilot drifts from source data, the founder kills it and operates from raw dashboards until reconciliation.

## Metrics

- Briefings produced (target: 100% of operating days).
- Approval-queue coverage (target: 100%).
- Eval pass-rate.

## Disclaimer

The Copilot is a view, not a decision-maker. Every action remains a human decision. Estimated value is not Verified value.
