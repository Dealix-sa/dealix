# Dealix Scripts Guide

Complete reference for all automation scripts in Dealix. Scripts are organized by execution frequency and purpose.

## 🚀 Daily Operations

Scripts that should run automatically every day as part of the Daily Operator workflow.

### `dealix_micro_day.sh` — Morning CEO Pack
**When:** Daily at 09:00 UTC  
**Purpose:** Generate quick-win micro revenue opportunities and CEO daily summary  
**Prerequisites:** `.env` configured with API keys, database access  
**Output:** `company/runtime/` (CEO pack JSON/CSV), `company/reports/*MICRO_MASTER_CEO_REPORT.md`  
**Command:** `bash scripts/dealix_micro_day.sh`  
**Duration:** ~5 minutes  
**Dependencies:** `company/micro/micro_master.py`, Python 3.11+  
**Failure Recovery:** Check `.env` keys, restart database connection, re-run manually  

### `dealix_revenue_day.sh` — Daily Commercial Pack
**When:** Daily at 10:00 UTC (after micro day)  
**Purpose:** Run full revenue engine, generate daily lead list and approval queue  
**Prerequisites:** Micro day completed successfully, `.env.railway.txt` configured  
**Output:** `company/runtime/` leads, `company/outbox/*_MASTER_STABLE_APPROVAL_QUEUE.csv`  
**Command:** `bash scripts/dealix_revenue_day.sh`  
**Duration:** ~15 minutes  
**Dependencies:** `company/revenue_engine/revenue_engine_v2.py`, PostgreSQL  
**Failure Recovery:** Check database connectivity, verify lead source data, rerun  

### `dealix_intake_day.sh` — Client Intake Processing
**When:** Daily at 11:30 UTC (after revenue day)  
**Purpose:** Process intake forms, generate diagnostic session prep, schedule calls  
**Prerequisites:** Revenue day completed, Slack API token configured  
**Output:** `company/runtime/intake/` session plans, `company/reports/intake_summary.md`  
**Command:** `bash scripts/dealix_intake_day.sh`  
**Duration:** ~8 minutes  
**Dependencies:** `company/intake/intake_engine.py`, Slack SDK  
**Failure Recovery:** Verify Slack token, check intake form data sources, test API access  

### `dealix_followup_day.sh` — Post-Sales Follow-up
**When:** Daily at 15:00 UTC (after intake day)  
**Purpose:** Auto-generate follow-up WhatsApp/email messages for past leads  
**Prerequisites:** CRM database populated, messaging API keys active  
**Output:** `company/outbox/follow_ups_*.csv`, `company/reports/followup_summary.md`  
**Command:** `bash scripts/dealix_followup_day.sh`  
**Duration:** ~10 minutes  
**Dependencies:** `company/crm/`, WhatsApp Business API, SendGrid  
**Failure Recovery:** Test messaging credentials, check CRM data freshness, check date filters  

### `dealix_trust_day.sh` — Trust Pack Assembly
**When:** Daily at 16:00 UTC (end of day)  
**Purpose:** Assemble proof pack, update customer dashboards, generate trust metrics  
**Prerequisites:** All prior daily scripts completed  
**Output:** `company/runtime/trust/`, `company/reports/trust_metrics.md`  
**Command:** `bash scripts/dealix_trust_day.sh`  
**Duration:** ~12 minutes  
**Dependencies:** `company/proof_os/`, `company/trust/trust_engine.py`  
**Failure Recovery:** Verify proof asset locations, check ledger sync, test dashboard APIs  

---

## 📊 Weekly Operations

Scripts that run once per week for reporting and consolidation.

### `dealix_weekly_sync.sh` — Weekly Reporting
**When:** Mondays 08:00 UTC  
**Purpose:** Consolidate weekly metrics, generate board summary, sync to S3  
**Prerequisites:** All daily scripts from prior week completed  
**Output:** `company/reports/week_*.md`, S3 sync to `dealix-reporting/`  
**Duration:** ~20 minutes  
**Command:** `bash scripts/dealix_weekly_sync.sh`  

### `dealix_dependency_check.sh` — Dependency Security Scan
**When:** Every Wednesday 09:00 UTC  
**Purpose:** Scan Python/Node dependencies for CVEs, generate SBOM, check licenses  
**Output:** `docs/SBOM.json`, `company/reports/dependency_audit.md`  
**Duration:** ~10 minutes  
**Command:** `bash scripts/dealix_dependency_check.sh`  

---

## 🚀 Deployment & Release

Scripts used during releases and production deployments.

### `dealix_deploy_staging.sh` — Deploy to Staging
**When:** Manual trigger on `feat/*` branches before PR merge  
**Purpose:** Deploy to Railway staging environment, run smoke tests  
**Command:** `bash scripts/dealix_deploy_staging.sh`  
**Duration:** ~8 minutes  
**Prerequisites:** Git branch pushed to origin, `.env.railway.staging` configured  

### `dealix_deploy_production.sh` — Deploy to Production
**When:** Manual trigger only, requires founder approval  
**Purpose:** Deploy to production Railway, run health checks, monitor first 5 minutes  
**Command:** `bash scripts/dealix_deploy_production.sh`  
**Duration:** ~12 minutes  
**Prerequisites:** Staging deployment successful, all CI checks green  
**Safety:** Requires git tag, founder confirmation, health monitoring enabled  

### `dealix_rollback.sh` — Production Rollback
**When:** Emergency only, if production deployment fails  
**Purpose:** Revert to previous stable Railway deployment  
**Command:** `bash scripts/dealix_rollback.sh --revision <PREVIOUS_COMMIT_SHA>`  
**Duration:** ~3 minutes  

---

## ✅ Verification & Health Checks

Scripts for testing setup, validating configuration, and checking system health.

### `dealix_health_check.sh` — System Health
**When:** Run before starting daily operations, or on-demand  
**Purpose:** Verify all systems operational: API, database, external services  
**Output:** Health report with all-green / any-failures status  
**Command:** `bash scripts/dealix_health_check.sh`  
**Duration:** ~2 minutes  
**Exit Code:** 0 if all healthy, 1 if any service down  

### `verify_python_syntax.sh` — Python Linting
**When:** Pre-commit, during CI, or before deployment  
**Purpose:** Check Python syntax, run pylint, verify no import errors  
**Output:** `company/reports/python_lint_check.txt`  
**Command:** `bash scripts/verify_python_syntax.sh`  
**Duration:** ~30 seconds  

### `verify_shell_scripts.sh` — Shell Script Validation
**When:** Pre-commit, during CI  
**Purpose:** Validate all shell scripts for syntax errors using `bash -n` and `shellcheck`  
**Output:** Error report, exit 0 if all valid  
**Command:** `bash scripts/verify_shell_scripts.sh`  
**Duration:** ~15 seconds  

### `verify_env_contract.sh` — Environment Variables Check
**When:** Pre-CI, startup, before deployment  
**Purpose:** Verify `.env.local` or `.env.railway.txt` has all required keys  
**Output:** Missing keys report, exit 1 if critical keys missing  
**Command:** `bash scripts/verify_env_contract.sh`  
**Duration:** ~2 seconds  

### `check.py` — Full System Check
**When:** During CI, or manual verification  
**Purpose:** Comprehensive setup validation (Python, .env, dependencies, API connectivity)  
**Output:** Check summary with [OK] / [WARN] / [FAIL] per category  
**Command:** `python3 scripts/check.py`  
**Duration:** ~5 seconds  

---

## 🔧 Manual Workflows (Legacy / Interactive)

Scripts that require manual interaction or are used for one-off tasks.

### `dealix_customer_credentials_check.py` — Wave 8 Credential Verification
**When:** Manual, during customer onboarding  
**Purpose:** Verify customer-provided API keys and credentials work  
**Input:** Customer credentials CSV  
**Output:** Pass/fail report per credential  
**Command:** `python3 scripts/dealix_customer_credentials_check.py --input <CSV_FILE>`  

### `generate_sample_*.py` — Sample Data Generation
**When:** Manual, for testing or demos  
**Purpose:** Generate synthetic test data (leads, customers, transactions)  
**Examples:**
- `python3 scripts/generate_sample_leads.py --count 100 --sector IT`
- `python3 scripts/generate_sample_customers.py --count 50`  

### `revenue_engine_debug.sh` — Revenue Engine Debugging
**When:** Manual, when revenue_engine_v2 has errors  
**Purpose:** Run revenue engine with verbose logging, test specific modules  
**Command:** `bash scripts/revenue_engine_debug.sh --mode dry-run --verbose`  

---

## ⚠️ Deprecated / Legacy Scripts

Scripts that are no longer actively used but kept for reference.

| Script | Status | Why | Alternative |
|--------|--------|-----|-------------|
| `*.ps1` (PowerShell) | Legacy | Windows-specific, no longer needed | Use `.sh` or Python |
| `dealix_v1_migrator.py` | Deprecated | V1 migration complete | N/A |
| `old_revenue_machine.py` | Replaced | Superseded by revenue_engine_v2 | Use `dealix_revenue_day.sh` |

---

## 🔐 Environment Setup Required

Before running scripts, ensure:

1. **`.env.local` is configured** with:
   - `OPENROUTER_API_KEY` (or your LLM provider key)
   - `OPENROUTER_MODEL`, `LIGHT_MODEL`, `FALLBACK_MODEL`
   - Database connection strings (`DATABASE_URL`, `POSTGRES_*`)
   - API keys for external services (Slack, WhatsApp, SendGrid, etc.)

2. **Python 3.11+** installed
   ```bash
   python3 --version
   ```

3. **Dependencies installed**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database ready**
   ```bash
   bash scripts/verify_env_contract.sh  # checks all prereqs
   ```

---

## 📋 Scheduling (Cron Examples)

Add these to crontab for automated daily operations:

```bash
# Morning: CEO pack
0 9 * * * cd /home/dealix && bash scripts/dealix_micro_day.sh >> logs/dealix_micro_day.log 2>&1

# Mid-morning: Revenue engine
30 10 * * * cd /home/dealix && bash scripts/dealix_revenue_day.sh >> logs/dealix_revenue_day.log 2>&1

# Late morning: Intake processing
30 11 * * * cd /home/dealix && bash scripts/dealix_intake_day.sh >> logs/dealix_intake_day.log 2>&1

# Afternoon: Follow-up generation
0 15 * * * cd /home/dealix && bash scripts/dealix_followup_day.sh >> logs/dealix_followup_day.log 2>&1

# End of day: Trust pack assembly
0 16 * * * cd /home/dealix && bash scripts/dealix_trust_day.sh >> logs/dealix_trust_day.log 2>&1

# Weekly sync: Mondays 08:00 UTC
0 8 * * 1 cd /home/dealix && bash scripts/dealix_weekly_sync.sh >> logs/dealix_weekly.log 2>&1
```

---

## 🆘 Troubleshooting

### Script fails with "command not found"
- **Check:** Is it executable? `chmod +x scripts/script_name.sh`
- **Check:** Are you in the dealix root directory? `pwd` should show `.../dealix`
- **Check:** Does Python path include company module? `echo $PYTHONPATH`

### Script fails with ".env key missing"
- **Fix:** Copy `.env.example` to `.env.local` and fill in all required keys
- **Verify:** Run `python3 scripts/check.py` to validate .env setup

### Script hangs or times out
- **Check:** Is database reachable? Try: `nc -zv <DB_HOST> 5432`
- **Check:** Are API keys valid? Test manually: `curl -H "Authorization: Bearer $API_KEY" https://api.example.com/health`
- **Workaround:** Kill process and re-run with `--mode dry-run` first

### Output files not created
- **Check:** Does `company/runtime/` directory exist? Create: `mkdir -p company/runtime`
- **Check:** Do you have write permissions? Test: `touch company/runtime/test.txt && rm company/runtime/test.txt`

---

## 📞 Support

For issues or questions:
1. Check logs in `logs/` or output from failed script
2. Run `python3 scripts/check.py` for full system diagnostics
3. Review script source (docstring has more details): `head -20 scripts/script_name.sh`
4. See `docs/DEVELOPMENT_TROUBLESHOOTING.md` for common problems
