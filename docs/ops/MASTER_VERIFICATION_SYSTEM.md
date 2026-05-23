# Dealix Master Verification System

## Purpose

A single command (`make verify-all`) that answers every day:

- Is Dealix built correctly?
- Does it run?
- Is it safe?
- Does it produce leads / replies / samples / proposals?
- Does it follow up on payments?
- Are trust gates intact?
- Is the server healthy?
- Do prompts avoid dangerous claims?
- Are outputs usable?

The system **wraps existing tooling** — it does not duplicate it. The 75+ existing
`verify_*.py` / `*_verify.sh` scripts, 38 GitHub workflows, the 8 doctrine tests
(`tests/test_no_*.py`), the `dealix.classifications` system (A0-A3 / R0-R3 / S0-S3),
the `DecisionOutput` contract (`dealix/contracts/decision.py`), and the 5 YAML evals
(`evals/*.yaml`) all remain authoritative. This layer just composes them into one
verdict.

## Architecture

```
make verify-all
   └── python3 scripts/master_verify.py [--private-ops $PRIVATE_OPS] [--json-out report.json]
        ├── L1  verify_layer1_repo_structure.py        canonical artifacts present
        ├── L2  verify_layer2_code_health.sh           lint + type + security + alembic
        ├── L3  verify_layer3_data_contracts.py        pydantic + schemas + high-stakes
        ├── L4  verify_layer4_prompt_output_quality.sh evals + forbidden-claims
        ├── L5  verify_layer5_trust_security.sh        8 doctrine tests + secret sweep
        ├── L6  verify_layer6_revenue_runtime.sh       revenue OS + proof + quality
        ├── L7  verify_layer7_server_runtime.sh        compileall + Railway + app import
        ├── L8  verify_layer8_github_governance.py     workflows parseable + required present
        └── L9  verify_layer9_business_evidence.sh     readiness + $PRIVATE_OPS CSVs
```

Exit-code contract for every layer:

| Code | Meaning |
| --- | --- |
| 0 | PASS |
| 1 | FAIL (hard check failed) |
| 2 | PARTIAL (advisory check warned, or step skipped — e.g. `$PRIVATE_OPS` unset) |

Master aggregation: any `1` → overall `FAIL`; only `2` → overall `PARTIAL`; all `0` → overall `PASS`.

### Hard vs Advisory checks

Inside each layer, individual steps are classified as:

- **Hard** — fails the layer with exit 1. Reserved for things that the current
  `.github/workflows/ci.yml` actually enforces (compileall, alembic single-head,
  doctrine tests, evals, service-readiness matrix, secret scan).
- **Advisory** — emits a warning, returns exit 2. Reserved for tooling the repo
  has but does not yet enforce in main CI (`make lint` / `type-check` / `security`,
  `verify_company_ready.py`, `verify_railway_production_config.py`, revenue OS
  sub-checks, governance verifiers).

Promote advisory → hard per layer with the corresponding `DEALIX_STRICT_*=1` env
var (`DEALIX_STRICT_LINT`, `DEALIX_STRICT_TRUST`, `DEALIX_STRICT_REVENUE`,
`DEALIX_STRICT_SERVER`, `DEALIX_STRICT_BUSINESS`) or pass `--strict` to the layer.

## Layer-by-Layer Mapping

### L1 — Repository Structure (`verify_layer1_repo_structure.py`)

Pure `pathlib` check that 36 canonical artifacts exist (≥ 50 bytes for files). Includes
README, Makefile, AGENTS.md, the 4 JSON schemas in `dealix/contracts/schemas/`, the
10 doctrine + governance test files, the 5 YAML evals, and the existing master
verifiers we wrap (`scripts/v10_master_verify.sh`, `scripts/revenue_os_master_verify.sh`).

### L2 — Code Health (`verify_layer2_code_health.sh`)

Wraps `make lint` (ruff + black), `make type-check` (mypy), `make security`
(bandit + detect-secrets), and `python3 scripts/check_alembic_single_head.py`.
Honors `DEALIX_SKIP_MYPY=1` and `DEALIX_SKIP_RUFF=1` env vars.

### L3 — Data Contracts (`verify_layer3_data_contracts.py`)

Imports every Pydantic model in `dealix/contracts/`; verifies that
`DecisionOutput(approval_class=A2, evidence=[])` raises `ValueError`
(the high-stakes validator at `dealix/contracts/decision.py:118-127`);
runs `dealix/contracts/dump_schemas.py` and diffs against the checked-in
JSON schemas to detect drift.

### L4 — Prompt / Output Quality (`verify_layer4_prompt_output_quality.sh`)

Runs `python3 scripts/run_evals.py` over the 5 YAML eval suites in `evals/`
(governance, arabic_quality, outreach_quality, lead_intelligence, company_brain)
and `pytest tests/test_landing_forbidden_claims.py`. Matrix of required output
fields is in `docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md`.

### L5 — Trust & Security (`verify_layer5_trust_security.sh`)

Runs the 8 doctrine tests + `test_doctrine_guardrails.py` + `test_landing_forbidden_claims.py`,
then `scripts/verify_governance.py` and `scripts/verify_governance_rules.py`,
then secret regex sweep (same pattern as `scripts/v10_master_verify.sh:104`):
`sk_live_*`, `ghp_*`, `AIza*`. Imports `platform_core.governance.enforce_doctrine_non_negotiables`
to assert the function is present (the 11 non-negotiables in `.claude/agents/dealix-pm.md:31-43`).

### L6 — Revenue Runtime (`verify_layer6_revenue_runtime.sh`)

Wraps `scripts/revenue_os_master_verify.sh` + `scripts/verify_proof_pack.py` +
`scripts/verify_quality_score.py`. Propagates `REVENUE_OS_VERDICT`.

### L7 — Server Runtime (`verify_layer7_server_runtime.sh`)

`python3 -m compileall` on `api/`, `auto_client_acquisition/`, `platform_core/`,
`dealix/`, `core/`. Runs `scripts/verify_railway_production_config.py` and
`scripts/verify_full_autonomous_ops_stack.py`. Best-effort `from api.main import app`
smoke (informational — won't fail the layer if production deps are missing).

### L8 — GitHub Governance (`verify_layer8_github_governance.py`)

Parses `.github/workflows/*.yml`; asserts every YAML loads and has `jobs.<id>.runs-on`
(or `uses`). Required workflows: `ci.yml`, `codeql.yml`, `verify-full-autonomous-ops.yml`,
`governed-full-ops-daily.yml`, `dealix-master-verify.yml`. Pure file parsing — no
GitHub API.

### L9 — Business Evidence + Private Ops (`verify_layer9_business_evidence.sh`)

Wraps `scripts/verify_company_ready.py` + `scripts/verify_service_readiness_matrix.py`.
If `$PRIVATE_OPS` is set and points to a directory, validates header contracts on
the 8 canonical CSVs (see below) plus commercial-motion sanity (suppression respected,
no sent-without-approval, proposals → payments). If `$PRIVATE_OPS` unset → exit 2
(PARTIAL).

#### Private Ops CSV Contract

| File | Required Headers |
| --- | --- |
| `growth/market_accounts.csv` | `account_id, company, website, country, city, sector, business_type, offer, source, discovered_at, status, next_action` |
| `intelligence/lead_intelligence_base.csv` | `account_id, company, sector, website, country, city, business_type, offer, buyer_titles, public_contact_path, source, fit_score, priority, why_fit, status, last_researched, last_contacted, reply_status, next_action` |
| `outreach/outreach_queue.csv` | `outreach_id, account_id, company, channel, recipient_or_contact_path, message, approval_status, send_status, sent_at, next_action` |
| `outreach/suppression_list.csv` | `company, contact, reason, source, date, status` |
| `outreach/conversation_log.csv` | `date, account_id, company, channel, reply_type, summary, routed_to, next_action` |
| `sales/proposal_queue.csv` | `date, account_id, company, trigger, proposal_type, amount_sar, status, due_date, next_action` |
| `finance/payment_capture_queue.csv` | `company, proposal_value, proposal_date, followup_stage, status, next_followup_date, next_action` |
| `client_success/retention_queue.csv` | `company, delivery_date, feedback_status, health_score, retainer_status, proof_status, referral_status, next_action` |

Extra columns are allowed; missing required columns fail the layer.

## Usage

### Local

```bash
make verify-all                                            # CI-style, no private ops
PRIVATE_OPS=/opt/dealix-ops-private make verify-all        # full check including L9 CSVs
python3 scripts/master_verify.py --layers 1,3,5 --json-out partial.json
python3 scripts/verify_layer1_repo_structure.py --json
```

### CI

`.github/workflows/dealix-master-verify.yml` runs on every PR and push to `main`,
uploads `master-verify.json` as an artifact.

### Branch protection

After the workflow's first green run on `main`, add `master-verify` as a required
status check in GitHub Settings → Branches → main → Require status checks. This
turns the verifier into a merge gate.

## Reading the JSON report

```json
{
  "overall": "PASS",
  "warnings": 1,
  "git_sha": "abc123…",
  "private_ops": null,
  "layers": [
    {"layer": 1, "name": "repo_structure", "verdict": "PASS", "exit_code": 0, "duration_s": 0.04, "summary": "36/36 required artifacts present"},
    {"layer": 9, "name": "business_evidence", "verdict": "PARTIAL", "exit_code": 2, "duration_s": 1.2, "summary": "PRIVATE_OPS not set; CSV contracts skipped"}
  ]
}
```

## Mapping to existing artifacts

| Layer | Wraps |
| --- | --- |
| L1 | (pure pathlib) |
| L2 | `Makefile` targets `lint`, `type-check`, `security`; `scripts/check_alembic_single_head.py` |
| L3 | `dealix/contracts/`, `dealix/classifications/`, `dealix/contracts/dump_schemas.py` |
| L4 | `evals/*.yaml`, `scripts/run_evals.py`, `tests/test_landing_forbidden_claims.py` |
| L5 | 8 `tests/test_no_*.py`, `tests/test_doctrine_guardrails.py`, `platform_core/governance.py`, `scripts/verify_governance{,_rules}.py` |
| L6 | `scripts/revenue_os_master_verify.sh`, `scripts/verify_proof_pack.py`, `scripts/verify_quality_score.py` |
| L7 | `api/main.py`, `scripts/verify_railway_production_config.py`, `scripts/verify_full_autonomous_ops_stack.py` |
| L8 | `.github/workflows/*.yml` |
| L9 | `scripts/verify_company_ready.py`, `scripts/verify_service_readiness_matrix.py`, `$PRIVATE_OPS/*.csv` |

## Definition of Correct

The system is correctly built **when** `make verify-all` exits `0` on `main`,
**and** `master-verify.json` shows `overall=PASS`, **and** removing any required
artifact from L1 flips overall to `FAIL`, **and** adding a banned claim
(e.g. `guaranteed revenue`) to `landing/*.html` flips L4/L5 to `FAIL`, **and**
the workflow is wired as a required status check on `main`.
