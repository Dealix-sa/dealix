# Production Readiness Gates

The gates that must pass **before any release**. Each gate is enforced by a
script in `scripts/` and wired into `.github/workflows/dealix-everything.yml`
and `.github/workflows/dealix-production-certification.yml`.

## Owner
- **CI gates:** Engineering on-call.
- **Business gates:** Founder.

## Cadence
- Every PR to `main` (CI).
- Every release tag (production-certification workflow).
- Weekly local audit by the founder via `make audit`.

## Gates (in order)

| # | Gate | Command | What fails the release |
|---|------|---------|------------------------|
| 1 | **Repo skeleton** | `python scripts/verify_repo_completeness.py` | Missing canonical dir or entry file |
| 2 | **Non-empty files** | `python scripts/verify_non_empty_files.py` | Placeholder docs under threshold (warn → fail when count > tolerated) |
| 3 | **Wiring** | `python scripts/verify_wiring.py` | `/healthz` not exposed, FastAPI routers not mounted, Makefile targets missing, frontend has no `build` script |
| 4 | **Policy-as-code** | `python scripts/verify_policy_as_code.py` | `approval_policy.yaml` malformed, `roi_or_guarantee.allowed != false`, missing `requires_approval` on a gated action |
| 5 | **Agent registry** | `python scripts/verify_agent_registry.py` | Governance docs don't name owner / kill-switch / approval / audit / sprawl-prevention |
| 6 | **Eval gate** | `python scripts/verify_eval_gate.py` | `evals/*.yaml` invalid or `verify_ai_output_quality.py` doesn't compile |
| 7 | **Live-send safety** | `python scripts/verify_live_send_safety.py` | `WHATSAPP_ALLOW_LIVE_SEND` default ≠ false, provider doesn't consult flag, approval gate missing `request()` / `decide` / critical-action declaration |
| 8 | **Railway readiness** | `python scripts/verify_railway_readiness.py` | `railway.toml` not using `DOCKERFILE`, `/healthz` not health-checked, Dockerfile not running as non-root, `start.sh` HEREDOC missing |
| 9 | **Business OS** | `python scripts/verify_business_os.py` | Founder/CEO/commercial docs missing owner / cadence |
| 10 | **Master gate** | `python scripts/verify_everything.py` | Any manifest layer fails OR banned-claim phrase appears in customer-facing docs |
| 11 | **Frontend build** | `cd frontend && npm ci && npm run build` | Build fails — proves the deploy artifact actually compiles |

## Source of truth
- `dealix_manifest.yaml` — declarative contract.
- `scripts/verify_everything.py` — single judge.
- Reports written under `docs/ops/DEALIX_*`.

## Failure mode
A failing gate blocks merge to `main` (when wired as a required status check) and blocks the production deploy (when wired via Railway "wait for CI"). Do **not** bypass with `--no-verify` or by disabling the gate.

## Recovery path
1. Run the failing gate locally; read the named reason.
2. Fix the underlying file / wiring; commit; push.
3. Re-trigger CI.
4. If the gate itself is wrong (e.g. checks for a path that legitimately changed), update the manifest **with founder sign-off** and a note in the audit report explaining why.

## How to extend
- New layer to enforce? Add it to `dealix_manifest.yaml` under `layers:` and (optionally) write a focused `scripts/verify_*.py`.
- Never add a new gate that silently passes — every verifier must exit 0 only on real success.
