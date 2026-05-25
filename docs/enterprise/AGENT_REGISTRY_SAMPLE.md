# Agent Registry — Sample

The agent registry holds the canonical record for every agent operating
inside Dealix. Sample entries below; the live registry is exposed
through the `dealix.hermes.agent_lifecycle.AgentRegistry` API.

```json
[
  {
    "agent_id": "proposal_factory",
    "owner": "Sami",
    "origin": "dealix_internal",
    "stage": "approval_gated",
    "runs": 312,
    "successful_runs": 305,
    "critical_incidents": 0,
    "trust_pass_rate": 0.984,
    "correction_rate": 0.031,
    "outcomes_logged": 280,
    "tool_scope": ["read_approved_opportunity", "draft_proposal", "flag_risk"],
    "workspace_scope": ["dealix_internal"],
    "forbidden_capabilities": ["send_external", "approve_price", "sign_contract"],
    "risk_score": 0.18
  },
  {
    "agent_id": "market_radar",
    "owner": "Sami",
    "origin": "dealix_internal",
    "stage": "draft_only",
    "runs": 41,
    "successful_runs": 38,
    "critical_incidents": 0,
    "trust_pass_rate": 0.951,
    "correction_rate": 0.074,
    "outcomes_logged": 29,
    "tool_scope": ["read_public_data", "summarize_call"],
    "workspace_scope": ["dealix_internal"],
    "forbidden_capabilities": ["send_external", "export_data"],
    "risk_score": 0.09
  },
  {
    "agent_id": "value_report_builder",
    "owner": "Sami",
    "origin": "dealix_internal",
    "stage": "monitored",
    "runs": 612,
    "successful_runs": 605,
    "critical_incidents": 0,
    "trust_pass_rate": 0.988,
    "correction_rate": 0.018,
    "outcomes_logged": 540,
    "tool_scope": [
      "read_approved_opportunity",
      "read_internal_doc",
      "draft_proposal"
    ],
    "workspace_scope": ["dealix_internal", "customer_*"],
    "forbidden_capabilities": ["send_external", "modify_production_config"],
    "risk_score": 0.22
  }
]
```

## What the customer gets

For every engagement we ship a per-engagement registry snapshot
filtered to the agents that touched the workspace. Each snapshot
includes the lifecycle history, last 30 days of trust metrics, and the
list of approval requests routed through the approval gate.
