# Ultimate Trust Plane

The Dealix trust plane is the combination of:

1. **Policy-as-Code** (`policies/dealix_control_policy.yaml`).
2. **Approval gating** (`/api/v1/internal/approvals/*`).
3. **Audit log** (`trust/approval_decisions.csv` in private ops).
4. **Trust flags** (`trust/trust_flags.csv` in private ops).
5. **Eval gate** (`evals/gates/dealix_agent_eval_gate.yaml`).

External-impact actions must traverse the trust plane:

```
agent draft -> policy evaluation -> approval queue -> founder decision -> audit record -> queued action
```

If any step is skipped the action is blocked.

## Founder Console hooks

- `/approvals` page surfaces queued items.
- `/trust` page surfaces raised flags.
- `/audit` page surfaces decisions.
- `/control-plane` page summarizes policy + agents + eval gate.
