---
description: Run the real Dealix verification gates (build/lint/types, env, security, prod-verify, positioning) plus launch-safety checks, and give a launch-readiness verdict.
---

Use `qa-verifier` and `proof-governance-reviewer`.

Run (quote exact output; never hide failures):
```bash
cd frontend && npm ci && npm run build && npm run lint && npm run typecheck; cd ..
make env-check
make security-smoke
make prod-verify
python scripts/verify_website_positioning.py
```

Also check (launch safety):
- no guaranteed-revenue claims
- no fake proof / fake testimonials / fake scarcity
- no auto-send or cold-automation language
- exactly one primary CTA per page
- module statuses exist (`docs/00_platform_truth/MODULE_STATUS_MAP.md`)
- Claims Register exists (`docs/03_governance/CLAIMS_REGISTER.md`)

## Output
- PASS / FAIL per command (with exact failure logs)
- likely cause + proposed fix per failure
- overall launch-readiness verdict
- next fixes (prioritized)
