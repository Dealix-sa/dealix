# Dealix AI Governance

Governance is the layer that lets Dealix sell into regulated Saudi
enterprises without losing speed. Every agent, every output, every
external action passes through this layer.

## Core principles

1. **Every agent has an identity.** Registered in `registries/agent_registry.yaml`.
2. **Every output carries a `governance_decision` field.** Allowed values:
   `auto_approved`, `pending_approval`, `denied`, `approved_by_<user>`.
3. **No external action without approval_center.** `dealix/governance/approvals.py`
   gates outbound email, WhatsApp, SMS, CRM bulk ops, payment events.
4. **Every claim has a `source_ref`.** Sources must be founder-submitted or
   licensed, NEVER scraped.

## Modules

| Module | Role |
|---|---|
| `dealix/governance/approvals.py` | Approval center — request, decide, audit. |
| `policies/dealix_control_policy.yaml` | Policy-as-Code — 11 non-negotiables. |
| `registries/agent_registry.yaml` | Identity for every agent. |
| `registries/machine_registry.yaml` | Identity for every long-running machine. |
| `evals/gates/dealix_agent_eval_gate.yaml` | Eval coverage gate per agent. |
| `evals/governance_eval.yaml` | Behavioral eval for governance compliance. |

## The 11 non-negotiables

See `CLAUDE.md` for the full enumeration. All eleven are enforced by tests
in `tests/test_no_*.py` plus runtime guards in `dealix/governance/`.

## Approval thresholds

| Trigger | Threshold |
|---|---|
| Outbound recipients in a single send | > 50 -> requires approval |
| Risk score on a draft | > 0.7 -> requires approval |
| Amount at stake (SAR) | > 5,000 -> requires approval |
| Pending approval TTL | 24h then auto-expire |

## Critical actions (always require approval)

`outbound_email_campaign`, `outbound_whatsapp_broadcast`,
`outbound_sms_broadcast`, `crm_bulk_update`, `crm_bulk_delete`,
`pricing_change`, `refund_issue`, `production_config_change`,
`moyasar_live_mode_flip`.

## Verifier

`make ai-governance` runs `scripts/verifiers/verify_ai_governance.py`.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
