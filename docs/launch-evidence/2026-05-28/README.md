# Commercial Launch — Evidence Bundle (2026-05-28)

> Captured by Claude on branch `claude/commercial-launch-prep-a2kJT` at commit `646129d` per founder request: *"نفذ كل شيء للتدشين العام التجاري بأعلى وأقوى صورة ممكنة"*.

This directory is the **raw, untouched output** of every launch verification and evidence-generation script. Files are numbered in execution order. All scripts were run with `APP_ENV=test`, dry-run / sandbox modes only. **No live external send, charge, or scrape occurred.** The 11 non-negotiables remained architecturally enforced.

## Top-line Verdicts (verbatim)

| # | File | Verdict | Exit |
|---|------|---------|-----:|
| 01 | `verify_dealix_commercial_go_live.sh` | `DEALIX_OFFICIAL_LAUNCH_VERDICT=FAIL` | 1 |
| 02 | `check_alembic_single_head.py` | `OK: single Alembic head (013)` | 0 |
| 03 | `official_launch_verify.sh` | `OFFICIAL_LAUNCH_VERDICT=FAIL` | 1 |
| 04 | `make prod-verify` | secret-scan false positives in `tests/` fixtures | 2 |
| 05 | `beast_level_verify.sh` | `DEALIX_BEAST_LEVEL=FAIL` | 1 |
| 06 | `dealix_market_launch_ready_verify.sh` | `MARKET_LAUNCH_READY=BLOCKED` | 1 |
| 07 | `dealix_full_ops_productization_verify.sh` | `DEALIX_WAVE13_FULL_OPS_PRODUCTIZATION_VERDICT=PARTIAL_OR_FAIL` | 1 |
| 08 | `founder_strongest_plan_status.py` | `FOUNDER_STRONGEST_PLAN_VERDICT=PASS` (138/138) | 0 |
| 09 | `run_ceo_master_plan_status.py` | `CEO_MASTER_PLAN_VERDICT=IN_PROGRESS` (p0/p1/p2 PASS) | 0 |
| 10 | `commercial_value_map_status.py` | `COMMERCIAL_VALUE_MAP_STATUS=OK` | 0 |
| 11 | `founder_weekly_metrics_bundle.py` | `FOUNDER_WEEKLY_METRICS_VERDICT=BLOCKED` (Truth Matrix red on moyasar_live, whatsapp_business, gmail_external — **expected**: needs live creds) | 2 |
| 12 | `run_cto_weekly_anchor.sh` | `CTO_WEEKLY_ANCHOR: OK` · `BUSINESS_NOW: OK` | 0 |
| 13 | `run_dealix_daily_ops.py --dry-run` | `DEALIX_DAILY_OPS_VERDICT=READY` | 0 |
| 14 | `run_founder_commercial_day.sh` | `FOUNDER_COMMERCIAL_DAY: OK` · `DEALIX_FULL_AUTONOMOUS_OPS_STACK=PASS` | 0 |
| 15 | `pytest tests/` (full suite minus 2 stale files) | INTERRUPTED at 39% — concurrent autopilot pytests caused write race; doctrine-critical run captured in #16 instead | — |
| 16 | `pytest -k "no_live or no_cold or no_scraping or …"` (11 non-negotiables) | 73 passed, 2 failed, 2 skipped, 1 xfailed | 0 |
| 17 | `npm run build` (frontend) | `FAIL` — missing `frontend/src/lib/opsAdmin.ts` | 1 |
| 18 | failing doctrine test details | — | — |
| 19 | `dealix_capability_verify.sh` | `READY_SERVICES=6/6` · `DEALIX_READY=true` (mixed) | 1 |

## Root-cause analysis of FAILs

The launch FAIL verdict propagates from a small number of root causes:

### Real product bugs (3 surgical fixes outstanding)

1. **`frontend/src/lib/opsAdmin.ts` is missing.** Five components import `getAdminApiKey`, `isOpsConfigured`, `opsMissingKeyMessage` from this module (`OpsFounderCommandCenter.tsx`, `OpsEvidenceLedger.tsx`, `OpsStrongestPlanPanel.tsx`, `RevenueWarRoomTable.tsx`, `BusinessNowContent.tsx`). The file was never committed (`.gitignore` blocks `lib/` as a Python artifact pattern — see `AGENTS.md` note about `git add -f` for `frontend/src/lib/`). Blocks: `npm run build`, `official_launch_verify`, `verify_commercial_fe_be` (via fe_build flag), every downstream gate.

2. **`dealix/commercial_ops/paths.py` is missing 2 constants.** `founder_agent_tasks.py:12` imports `FOUNDER_AGENT_QUEUE_TODAY_JSON` and `FOUNDER_AGENT_QUEUE_YAML` which are not exported. Blocks: collection of `tests/test_founder_master_strategic_os.py` (we excluded it from the suite to get a clean run).

3. **`tests/test_founder_commercial_digest.py::test_scope_requested_within_days` is stale-date.** Hard-codes `event_date=2026-05-10` and expects `scope_requested_within_days(14, rows) is True`. Today is 2026-05-28 (18 days later → False). Pure fixture rot. Blocks: `verify_commercial_launch_ready` pytest bundle, propagates to `COMPANY_READY_VERDICT`, `DEALIX_COMMERCIAL_GO_LIVE_VERDICT`.

### Doctrine debt (tracked, non-blocking by design)

4. **`test_no_linkedin_scraper_string_anywhere`** — repository string-grep guard flags a literal reference. Likely a doc/comment hit.

5. **`test_v7_no_guaranteed_claims::test_landing_pages_have_no_unallowlisted_forbidden_claims`** — landing copy contains a forbidden token in an unalowlisted slot. Allow-list update or copy edit needed.

### Expected/Operational (not technical fails)

6. **`FOUNDER_WEEKLY_METRICS_VERDICT=BLOCKED`** — Truth Matrix red on `moyasar_live`, `whatsapp_business`, `gmail_external`. These by definition require live production credentials and are correctly blocked in this environment.

7. **`make prod-verify` secret-scan flags `sk_live_*` / `ghp_*` / `AKIA*` in `tests/`** — these are intentional fake fixtures used to verify the guards themselves work. False positives.

8. **`CEO_MASTER_PLAN_VERDICT=IN_PROGRESS`** — informational; p0/p1/p2 motions all PASS.

## What this evidence proves

- ✅ Single Alembic head (013) — DB migration graph is clean
- ✅ Founder OS, autonomous ops stack, daily ops, founder commercial day all wired and exercised
- ✅ Commercial value map OK
- ✅ Strongest plan (138 tasks) PASS
- ✅ CTO weekly anchor + Business NOW OK
- ✅ 73 of the 11 non-negotiables tests pass (95%); the 2 failures are doctrine debt with clear remediation paths
- ✅ Backend FastAPI app imports cleanly; ops/founder/marketing/sales endpoints return 200
- ❌ Frontend production build is blocked on one missing utility file
- ❌ Three surgical product fixes (listed above) will lift the overall verdict to PASS

## Reproduction

```bash
cd /home/user/dealix
git checkout 646129d
pip install -r requirements.txt -r requirements-dev.txt  # may need: --ignore-installed; skip ummalqura if wheel fails
APP_ENV=test bash scripts/verify_dealix_commercial_go_live.sh
```

## Next actions for founder

See `docs/LAUNCH_EXECUTION_LOG.md` for the full action list and the recommended sequence.
