# Dealix Control Plane

The Control Plane is the single-pane founder view of:

- Policies (`policies/dealix_control_policy.yaml`)
- Agents (`registries/agent_registry.yaml`)
- Eval suites (`evals/gates/dealix_agent_eval_gate.yaml`)
- Operating scorecard (`<private_ops>/founder/operating_scorecard.md`)
- Open risks (`<private_ops>/trust/trust_flags.csv`)

Frontend: `apps/web/app/control-plane/page.tsx`.

Backend: `api/routers/internal/founder_console.py` —
`/api/v1/internal/control/*`.

Mutations supported:

- `POST /api/v1/internal/control/agents/{id}/disable`
- `POST /api/v1/internal/control/agents/{id}/enable`

Both append to `trust/agent_toggles.csv`.
