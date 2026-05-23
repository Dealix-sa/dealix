# Production Security Gate

Dealix may only call itself production-ready when **all** of the
following are true:

- `DEALIX_INTERNAL_TOKEN` is set in the runtime environment.
- No secrets are present in the repo (`detect-secrets`, `gitleaks`).
- `make policy-check` passes.
- `make agent-registry` passes.
- `make eval-gate` passes.
- `python scripts/verify_prompt_output_quality.py` passes.
- `python scripts/verify_ultimate_operating_layer.py` passes.
- `npm --prefix apps/web run build` passes.
- `python scripts/smoke_internal_api.py` returns 200 for every probed
  endpoint when run against the deployed API.
- Branch protection on `main` enforces the required checks listed in
  `docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md`.

Any other state is **not** production-ready — even if the app boots and
the UI renders. State this explicitly when reporting status.
