# Dealix Control Plane

The Control Plane is the founder's view into "what does the AI think is
happening?" It's intentionally a thin renderer over the source-of-truth
artifacts:

* `policies/dealix_control_policy.yaml`
* `registries/agent_registry.yaml`
* `evals/gates/dealix_agent_eval_gate.yaml`
* `<private_ops>/founder/operating_scorecard.md`
* `<private_ops>/founder/sovereign_readiness.md`

## UI

[`apps/web/app/control-plane/page.tsx`](../../apps/web/app/control-plane/page.tsx).

## API

| Endpoint | Returns |
|---|---|
| `GET /api/v1/internal/control/summary` | counts + scorecard + sovereign readiness + auth mode |
| `GET /api/v1/internal/control/policies` | policy class / rule counts |
| `GET /api/v1/internal/control/agents` | agent list from registry |
| `GET /api/v1/internal/control/scorecard` | operating scorecard markdown |
| `GET /api/v1/internal/control/risks` | open trust flags |
| `POST /api/v1/internal/control/agents/{id}/disable` | kill switch |
| `POST /api/v1/internal/control/agents/{id}/enable` | re-enable |
