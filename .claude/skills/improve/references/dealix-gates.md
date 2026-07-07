# Dealix verification gates & safety boundaries

The `improve` skill cites **these commands** in plans — never invented ones.
An executor must be able to run the "expected output" mechanically.

## Verification gates (use as plan done-criteria)

| Gate | Command | Expected |
|------|---------|----------|
| Full launch matrix | `make full-repo-test` | all required gates PASS |
| Python compiles | `python3 -m compileall -q core api db dealix company auto_client_acquisition` | exit 0 |
| Env contract | `make env-check` | no duplicate keys, contract OK |
| Security smoke (CI-safe) | `python3 scripts/ops/security_smoke_ci.py` | exit 0, no secrets |
| No auto external send | `python3 scripts/verify_no_auto_external_send.py` | exit 0 |
| Launch readiness | `python3 scripts/verify_company_launch_ready.py` | READY |
| Railway env names | `python3 scripts/ops/check_railway_production_env.py` | names only, never values |
| Frontend | `npm --prefix apps/web run verify` | typecheck + build PASS |
| Targeted tests | `python3 -m pytest tests/<file> -q` | pass count matches plan |

Every plan step ends with one of these and its expected output. If a plan needs
a command not listed here, verify it exists (`grep` the `Makefile` / `scripts/`)
before writing it in.

## Required doctrine guard tests (must stay green — never propose removing)

```
tests/test_no_source_passport_no_ai.py
tests/test_pii_external_requires_approval.py
tests/test_no_cold_whatsapp.py
tests/test_no_linkedin_automation.py
tests/test_no_scraping_engine.py
tests/test_no_guaranteed_claims.py
tests/test_output_requires_governance_status.py
tests/test_proof_pack_required.py
```

## Outbound-safety env contract (must remain false — flag, never flip)

```
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Protected surfaces (a plan may reference but never weaken)

- `api/main.py:_validate_production_secrets` — production secret guard.
- `railway.toml` — builder=DOCKERFILE, `healthcheckPath=/healthz`. No NIXPACKS.
- The 11 non-negotiables in `CLAUDE.md` and `.claude/rules/dealix-safety.md`.

## Executor model selection (for `/improve execute`)

Repo code is non-confidential — a cheap/free executor is fine. Pick via the radar:

```bash
make ai-provider-registry-check                 # guard: fail if the registry is stale
make ai-provider-radar
python3 scripts/ops/free_llm_provider_radar.py --task coding --json
```

Registry: `data/ai/free_llm_provider_registry.json` (adopted from
`cheahjs/free-llm-api-resources`). **Never** send customer data, PII, secrets, or
production config to a free tier — every entry is marked `private data: do_not_send`.
