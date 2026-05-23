# Ultimate Security Governance

Security in Dealix is a property of the architecture, not a separate
team. Three lines of defence:

## 1. Internal API auth gate

Documented in [`INTERNAL_API_AUTH_GATE.md`](INTERNAL_API_AUTH_GATE.md).
Every `/api/v1/internal/*` request requires
`X-Dealix-Internal-Token` in production.

## 2. Policy-as-code at the runtime boundary

`api/internal/policy_adapter.py` evaluates every approval before the
audit log records a decision. The adapter fails closed.

## 3. Eval gate on agent output

`evals/gates/dealix_agent_eval_gate.yaml` defines 15 mandatory suites,
including `sensitive_data_leakage` and `prompt_injection`. The Eval
Guardian agent runs them before any draft reaches the founder.

## Threat model snapshot

* **Compromised AI vendor key** — limited blast radius: the key never
  touches the private runtime; agents call the LLM through a single
  gateway and only see scoped inputs.
* **Prompt injection from researched data** — caught by the eval gate.
* **Insider risk on the deploy box** — bounded by the private-ops
  directory permissions and the audit log; restoring from backup is
  documented.
