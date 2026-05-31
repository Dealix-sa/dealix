# AI Governance Model

Dealix governs agents through a fixed lifecycle. An agent never holds
more authority than it has demonstrated through measurable evidence.

## Lifecycle stages

```
Proposed
 → Registered
   → Risk Scored
     → Tool Scoped
       → Context Scoped
         → Tested
           → Draft-Only
             → Approval-Gated
               → Limited Autonomy
                 → Monitored
                   ↘ Restricted (downgrade)
                   ↘ Retired (terminal)
```

Implemented in
[`dealix/hermes/agent_lifecycle/registry.py`](../../dealix/hermes/agent_lifecycle/registry.py).

## Promotion gates

Stage transitions are only allowed when the runtime evidence meets the
codified thresholds (see
[`dealix/hermes/agent_lifecycle/evaluation.py`](../../dealix/hermes/agent_lifecycle/evaluation.py)).

| From | To | Required evidence |
| --- | --- | --- |
| Draft-Only | Approval-Gated | ≥50 runs, 0 critical incidents, ≥95% trust pass rate, ≤10% correction rate, outcomes logged for ≥50% of runs, owner set, tool scope declared |
| Approval-Gated | Limited Autonomy | ≥200 runs, ≥97% trust pass rate, 0 critical incidents over lifetime |
| Limited Autonomy | Monitored | ≥500 runs, ≥97% trust pass rate sustained |

Any critical incident downgrades the agent to `RESTRICTED` immediately
(`dealix.hermes.agent_lifecycle.restriction`).

## Identity model

Each agent carries an identity with:

- `capability_scope` — explicit whitelist
- `forbidden_capabilities` — explicit denylist (always wins)
- `workspace_scope` — which logical tenant/data boundary
- `revocable` flag — every identity is revocable at runtime by default
- `session_policy` — TTL, idle timeout, and per-session operation cap

The identity sample below is enforced as a dataclass in
[`dealix/hermes/identity/agent_identity.py`](../../dealix/hermes/identity/agent_identity.py).

```json
{
  "agent_id": "proposal_factory",
  "owner": "Sami",
  "origin": "dealix_internal",
  "capability_scope": [
    "read_approved_opportunity",
    "draft_proposal",
    "flag_risk"
  ],
  "forbidden_capabilities": [
    "send_external",
    "approve_price",
    "sign_contract",
    "export_data"
  ],
  "workspace_scope": ["dealix_internal"],
  "revocable": true,
  "status": "draft_only"
}
```

## Cross-agent security

A lower-privilege agent cannot delegate any externally-visible or
monetary action to a higher-privilege agent — the second-order
prompt-injection guard. Every cross-agent message passes through
`dealix.hermes.agent_comms.cross_agent_validator`:

```
sanitize → source trust → capability check → delegation policy →
output validator → audit
```

## Audit

Every promotion, restriction, and revocation appends to the immutable
audit trail in `dealix.trust.audit`. The audit entries carry the
`approved_by` identity, the reason, and the evaluation snapshot.
