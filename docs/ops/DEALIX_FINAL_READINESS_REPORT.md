# Dealix Final Readiness Report

This document is the single human-readable answer to:

> Is Dealix ready to deploy to production?

The answer is "yes" only if `make production-certification` exits 0
**and** every required Railway variable + GitHub branch protection
listed below is in place. Nothing else.

## 1. The one command that decides

```bash
make production-certification
```

Roll-up output must read `RESULT: PRODUCTION-GATED READY`. If it
doesn't, fix the failure printed above the rollup and re-run. Never
ship by editing the gate.

## 2. What the gate covers

| Layer                  | Verifier                                | Purpose |
|------------------------|------------------------------------------|---------|
| Policy-as-Code         | `scripts/verify_policy_as_code.py`       | Immutable rules cannot be removed/weakened |
| Agent Registry         | `scripts/verify_agent_registry.py`       | Every agent declares approval class, kill switch, audit, eval |
| Machine Registry       | `scripts/verify_machine_registry.py`     | Cron-like jobs cannot take external action |
| Eval Gate              | `scripts/verify_eval_gate.py`            | Every registered agent has eval thresholds + cases |
| Prompt/Output Safety   | `scripts/verify_prompt_output_quality.py`| No "guaranteed revenue/sales/meetings" in user-facing copy |
| Live Send Safety       | `scripts/verify_live_send_safety.py`     | Frontend has no secret tokens / direct external URLs |
| Railway Readiness      | `scripts/verify_railway_readiness.py`    | railway.toml / Dockerfile / healthcheck / predeploy clean |
| Production Env         | `scripts/verify_production_env.py`       | Required env vars present, no NEXT_PUBLIC_* secrets |
| AI Company OS          | `scripts/verify_ai_company_os.py`        | Founder Console + internal API surfaces |

The roll-up runs them in this order and writes a green marker before
Production Env reads it, so `WHATSAPP_ALLOW_LIVE_SEND=true` is only
ever accepted after Live Send Safety has just passed.

## 3. Railway settings that must be on

1. **Source → Branch**: `main`
2. **Source → Wait for CI**: ON — wait for
   `.github/workflows/dealix-production-certification.yml`
3. **Variables** (set; never printed by any script):
   - `APP_ENV=production`
   - `DEALIX_INTERNAL_TOKEN` (long random)
   - `JWT_SECRET_KEY`
   - `DEALIX_PRIVATE_OPS=/app/private_ops` (or a volume mount)
   - `DATABASE_URL`
   - `WHATSAPP_MOCK_MODE=true`
   - `WHATSAPP_ALLOW_LIVE_SEND=false`
   - `WHATSAPP_DAILY_LIMIT=10` (raise only after the safety gate)
4. **Healthcheck**: `/healthz` (already in `railway.toml`)
5. **Predeploy**: `sh /app/scripts/railway_predeploy.sh`

## 4. GitHub branch protection (one-time)

`Settings → Branches → main → Branch protection rule`:

- Require status check: **Dealix Production Certification / Production Certification Gate**
- Require status check: **Dealix Production Certification / Frontend Build (apps/web)**
- Require pull request review: 1
- Do not allow bypass

This stops anyone (including the founder) from merging to `main`
before the gate is green, which in turn stops Railway from deploying
a broken build.

## 5. Flipping a live integration on (manual, never automatic)

Live external sending stays off until ALL of these are true:

1. `make production-certification` is green.
2. `make live-send-safety` (run on its own) is green.
3. A founder approval flow has been smoke-tested end-to-end with a
   real approver in the loop.
4. Daily-limit env (`WHATSAPP_DAILY_LIMIT`) is set to a number you'd
   accept as the *worst-case* mistake.
5. Suppression list is populated for any contact who hasn't opted in.

Only then flip `WHATSAPP_ALLOW_LIVE_SEND=true` in Railway. The
Production Env verifier refuses the combo unless the Live Send Safety
marker is fresh from the same CI run.

## 6. What's intentionally NOT in the gate

- LLM evaluations against live providers (cost + flakiness). They're
  declared in `evals/gates/dealix_agent_eval_gate.yaml`; running them
  is a separate command that the founder triggers on demand.
- End-to-end browser tests against production. Smoke is via
  `scripts/smoke_internal_api.py` with `BASE_URL=...`.

## 7. When the gate fails, the playbook is short

1. Read the FIRST failure (others are usually downstream).
2. Run the named verifier directly: `python scripts/<name>.py`.
3. Fix the underlying issue. Do NOT delete the failing check.
4. Re-run `make production-certification`.

If you're tempted to weaken or remove a rule, stop. The whole point of
this layer is that it is the same on every machine, every PR, every day.
