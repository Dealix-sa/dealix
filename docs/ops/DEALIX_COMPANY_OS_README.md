# Dealix Company OS — operating README

Single source of truth for the commercial, founder-facing operating system.

## Run order

```
make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private

make brand-system
make growth-system
make marketing-system
make product-distribution
make policy-check
make agent-registry
make machine-registry
make eval-gate
make prompt-output
make ai-governance

make execution-launch-layer
make market-attack-system
make scale-moat-system
make founder-management-system
make hypergrowth-ceo-layer
make founder-ceo-hypergrowth-layer

make company-os
make smoke-internal-api
make everything

npm --prefix apps/web ci
npm --prefix apps/web run build
```

## Reports

```
make ceo-daily-brief
make ceo-weekly-review
make founder-leverage
make capital-allocation
make strategy-scorecard
make revenue-forecast
make beachhead-scorecard
make offer-market-fit
make data-moat
make company-memory
make advisor-update
```

## Surface

- Founder Console at `apps/web/app/` — 36 internal pages over a single shell
  (`apps/web/components/founder-shell.tsx`).
- Internal API at `api/internal/` + `api/routers/internal/founder_console.py`.
- Policy-as-code at `policies/dealix_control_policy.yaml`.
- Agent + machine registries at `registries/`.
- Eval gate at `evals/gates/dealix_agent_eval_gate.yaml`.
- Generators under `scripts/generate_*.py`.
- Verifiers under `scripts/verify_*.py`.
- Master verifier `scripts/verify_everything.py` writes
  `docs/ops/DEALIX_FINAL_READINESS_REPORT.md`,
  `docs/ops/DEALIX_MISSING_SYSTEMS.md`, and
  `evals/eval_status.csv`.

## Private ops workspace

`DEALIX_PRIVATE_OPS` (default `/opt/dealix-ops-private`) holds CSVs and MD
documents that are read by generators and the internal API. Never commit this
workspace to git.

## Policy

AI prepares · founder approves · no guaranteed claims · no auto external send

Every output ends with the audit footer (source · freshness · actor · policy).
A3 tier agents never auto-send; every external action queues into
`approvals/approval_queue.csv` for founder review.
