# CLAUDE.md — Dealix repository guide for Claude Code

This file is the durable instruction set for Claude Code working in
this repository. Read it before doing anything significant.

## 1. The non-negotiables

These eleven rules are enforced by the certification layer. Do not
weaken or remove any of them; the verifiers refuse to ship if you do.

1. No secrets in repo or logs. Never print a secret value, never log
   its prefix/suffix/hash, never include it in a commit message.
2. No external sending unless approval + policy + audit + live-send
   safety all pass.
3. No guaranteed revenue/sales/meetings claims in any user-facing copy.
4. No frontend code calls WhatsApp / SMTP / Moyasar / HubSpot APIs
   directly. All external calls go through
   `api/internal/integration_gate.py`.
5. No A3 (high-risk) action is ever automatic. Always requires founder
   escalation.
6. Internal APIs (`/api/v1/internal/*`) require
   `DEALIX_INTERNAL_TOKEN` in production. Constant-time compare.
7. Every system must be verified by `scripts/verify_everything.py`.
8. Final result must pass `make production-certification`.
9. Cold WhatsApp / LinkedIn automation / scraping is refused at the
   sales-agent level. Don't add it.
10. Frontend bundles must not embed any `NEXT_PUBLIC_*` variable whose
    name contains TOKEN / SECRET / KEY / PASSWORD.
11. Railway "Wait for CI" must be on. The CI workflow that satisfies
    it is `.github/workflows/dealix-production-certification.yml`.

## 2. The one command that decides

```bash
make production-certification
```

If it exits 0 with `RESULT: PRODUCTION-GATED READY`, the gate is
green. If not, the failure printed first is the one to fix.

## 3. Where to read first

| Question | File |
|---|---|
| Is it ready to deploy? | `docs/ops/DEALIX_FINAL_READINESS_REPORT.md` |
| How is Railway wired? | `docs/railway/RAILWAY_PRODUCTION_DEPLOYMENT.md` |
| Where do secrets live? | `docs/security/RAILWAY_SECRET_HANDLING.md` |
| How do kill switches work? | `docs/security/LIVE_INTEGRATION_KILL_SWITCHES.md` |
| How is live send gated? | `docs/trust/LIVE_SEND_SAFETY_GATE.md` |
| WhatsApp specifically? | `docs/trust/WHATSAPP_APPROVAL_GATE.md` |
| What's missing? | `docs/ops/DEALIX_MISSING_SYSTEMS.md` |
| What was actually built? | `docs/ops/DEALIX_IMPLEMENTATION_AUDIT.md` |

## 4. Directory map (certification layer only)

```
policies/dealix_control_policy.yaml      ← rules (10, 6 immutable)
registries/agent_registry.yaml           ← every agent
registries/machine_registry.yaml         ← every cron-like job
registries/integration_registry.yaml     ← every external integration
evals/gates/dealix_agent_eval_gate.yaml  ← eval thresholds
api/internal/                            ← auth/policy/audit/gate scaffold
api/routers/internal/founder_console.py  ← internal API endpoints
scripts/verify_*.py                      ← the 9 verifiers
scripts/generate_*.py                    ← read-only generators
scripts/bootstrap_private_ops_runtime.py ← bootstraps the private tree
.github/workflows/dealix-production-certification.yml
```

## 5. What you should never do

- Send anything externally directly from a script. Always go through
  `api/internal/integration_gate.request_external_send(...)`.
- Edit a policy rule's `result` field to soften it. Add a new, more
  specific rule instead — and add it to `immutable_rules` if it
  should stay forever.
- Mark an agent as `external_action_allowed: true` without also
  setting `requires_policy`, `requires_integration_gate`, and
  `requires_live_send_safety`.
- Add a `NEXT_PUBLIC_*` env var that contains a secret. The
  production-env verifier will fail and the safety verifier will fail.
- Commit anything to `private_ops/`. It is meant to live outside the
  repository on the Railway volume.

## 6. What you should always do

- Before any commit that touches policies/registries/scripts/api, run
  `make production-certification` locally.
- When in doubt about whether something is risky, add a WARN check to
  the right verifier so the next person sees it.
- Keep verifier output deterministic and offline. They must work in
  CI without any external network calls.
