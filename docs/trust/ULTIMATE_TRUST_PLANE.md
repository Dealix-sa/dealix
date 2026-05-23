# Ultimate Trust Plane

The Trust Plane is the union of:

- **Policy-as-Code** (`policies/dealix_control_policy.yaml`)
- **Agent Registry** (`registries/agent_registry.yaml`)
- **Eval Gate** (`evals/gates/dealix_agent_eval_gate.yaml`)
- **Audit log** (`${DEALIX_PRIVATE_OPS}/trust/approval_decisions.csv`)
- **Suppression list** (`${DEALIX_PRIVATE_OPS}/outreach/suppression_list.csv`)
- **Trust flags** (`${DEALIX_PRIVATE_OPS}/trust/trust_flags.csv`)

## Invariants

1. No agent owns external action authority by default.
2. A3 actions are never agent-initiated.
3. Every approval is policy-checked before it is recorded.
4. Every recorded approval includes the rule that matched and whether
   external action is allowed.
5. The internal API refuses to expose itself without an internal token in
   production (`DEALIX_INTERNAL_TOKEN`).
6. Every shipping agent must pass the eval gate's critical suites.

## How a proposed action flows

```
agent_output → trust_guardian → policy_adapter.evaluate → approval_queue.csv
       founder reviews in /approvals → approve/reject/edit/escalate
       internal API writes approval_decisions.csv (audit)
       downstream worker picks up only externally-allowed approved rows
```
