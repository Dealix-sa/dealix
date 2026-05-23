# Ultimate Security + Governance

Dealix follows NIST-AI-RMF-shaped governance: identify, measure, manage,
govern. Concrete controls live in:

- Policy-as-Code (`policies/dealix_control_policy.yaml`)
- Agent Registry (`registries/agent_registry.yaml`)
- Eval Gate (`evals/gates/dealix_agent_eval_gate.yaml`)
- Internal API auth gate (`api/internal/auth.py`)
- Audit log (private ops `trust/approval_decisions.csv`)

## Controls

| Control | Where | Verified by |
|---|---|---|
| Internal token enforced | `api/internal/auth.py` | `docs/security/INTERNAL_API_AUTH_GATE.md` |
| No secrets in repo | pre-commit + gitleaks | `.pre-commit-config.yaml`, `.gitleaks.toml` |
| Trust gate | `policy_adapter.py` | `scripts/verify_policy_as_code.py` |
| Kill switch per agent | registry + control plane | `scripts/verify_agent_registry.py` |
| Eval gate | gate YAML | `scripts/verify_eval_gate.py` |
| Audit log append-only | runtime reader | code review (no overwrite path) |
| Prompt/output safety | doc scanner | `scripts/verify_prompt_output_quality.py` |
| Master verifier | union of all | `scripts/verify_ultimate_operating_layer.py` |

## Reporting

`GET /api/v1/internal/security/status` surfaces the rows from
`security/security_status.csv` plus the `production_token_set` boolean
so the founder can confirm the token is present before promoting.
