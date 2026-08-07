# 002 — Guard against a stale free-LLM provider registry

- **Finding:** `improve execute` selects a cheap model from
  `data/ai/free_llm_provider_registry.json`, but nothing fails when that registry
  goes stale. Free tiers, rate limits, and model IDs drift fast upstream
  (`cheahjs/free-llm-api-resources`); a stale registry risks dispatching an
  executor to a dead or changed endpoint. Registry carries `last_reviewed` and
  `upstream_readme_sha_observed` but no automated staleness check consumed them.
- **Category:** doctrine/DX   **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** 2ec6a6c
- **Status:** ✅ DONE — landed in the improve-integration PR.

## What shipped (worked example)
- `scripts/ops/check_provider_registry_freshness.py` — dependency-free, offline.
  Pure `evaluate()` returns a status dict; exit 1 when stale/malformed. Age
  threshold via `DEALIX_PROVIDER_REGISTRY_MAX_AGE_DAYS` (default 45).
- `tests/test_provider_registry_freshness.py` — 7 cases (fresh, stale, missing
  `last_reviewed`, missing drift anchor, no providers, future date, real registry).
- `Makefile` target `ai-provider-registry-check`.

## Done criteria (all verified)
- [x] `python3 scripts/ops/check_provider_registry_freshness.py` → `RESULT: FRESH`, exit 0
- [x] `make ai-provider-registry-check` → FRESH
- [x] `tests/test_provider_registry_freshness.py` → 7 passed, 0 failed

## Why it was safe to execute directly
Net-new file + net-new test + one additive make target. Touches no doctrine
guard, no outbound flag, no production secret path. Read-only over the registry.
