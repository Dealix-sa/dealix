# FILE OWNERSHIP AND NO-DUPLICATION MAP

## Canonical Owners

| Domain | Canonical Location | Owner | Notes |
|--------|---------------------|-------|-------|
| **Backend API** | `api/` | Backend team | `api/main.py` is entry point |
| **Frontend (Primary)** | `frontend/` | Frontend team | Next.js 15.1.3 — **canonical frontend** |
| **Frontend (Legacy)** | `apps/web/` | Legacy | Overlapping pages; consolidate into `frontend/` |
| **Business Logic** | `dealix/` | Product team | Revenue, payments, commercial engines |
| **Core Framework** | `core/` | Platform team | Config, LLM gateway, agents, tasks |
| **Auto Client Acquisition** | `auto_client_acquisition/` | Growth team | Lead pipeline, ICP matching |
| **Autonomous Growth** | `autonomous_growth/` | Growth team | Sector intel, content, distribution |
| **Integrations** | `integrations/` | Integrations team | HubSpot, payments, WhatsApp |
| **Tests** | `tests/` | QA team | All test categories |
| **Scripts** | `scripts/` | DevOps/Founder | Verification, automation |
| **Docs (Architecture)** | `docs/architecture/` | Tech lead | System design, API reference |
| **Docs (Commercial)** | `docs/commercial/` | Founder/GTM | Sales, GTM, pricing |
| **Docs (Compliance)** | `docs/compliance/` | Legal/Security | PDPL, ZATCA, security |
| **Docs (Ops)** | `docs/ops/` | Operations | Runbooks, deployment, playbooks |
| **CI/CD** | `.github/workflows/` | DevOps | All GitHub Actions |
| **DB Migrations** | `alembic/` | Backend team | Schema migrations |
| **Docker** | `Dockerfile*` | DevOps | Container definitions |

## Duplicate-Looking Docs/Scripts/Workflows

### 🔴 CRITICAL: Duplicate Numbered Doc Directories
The `docs/` directory has 44 numbered directories with significant duplication:

| Number | Count | Directories | Canonical Winner |
|--------|-------|-------------|-----------------|
| 00 | 2 | `00_constitution`, `00_foundation` | Keep both (different content) |
| 01 | 2 | `01_category`, `01_category_creation` | **01_category** wins |
| 02 | 2 | `02_saudi_positioning`, `02_strategy` | **02_strategy** wins |
| 03 | 2 | `03_commercial_mvp`, `03_saudi_positioning` | **03_commercial_mvp** wins |
| 04 | 2 | `04_data_os`, `04_product_strategy` | **04_data_os** wins |
| 05 | 2 | `05_client_os`, `05_governance_os` | Keep both (different domains) |
| 06 | 2 | `06_data_os`, `06_llm_gateway` | **06_llm_gateway** wins |
| 07 | 2 | `07_governance`, `07_proof_os` | Keep both |
| 08 | 2 | `08_responsible_ai`, `08_value_os` | Keep both |
| 09 | 2 | `09_capital_os`, `09_llm_gateway` | **09_llm_gateway** wins |
| 10 | 2 | `10_agents`, `10_tests` | **10_agents** wins |
| 11 | 2 | `11_client_os`, `11_secure_runtime` | **11_secure_runtime** wins |
| 12 | 2 | `12_adoption_os`, `12_auditability` | Keep both |
| 13 | 2 | `13_evidence_control_plane`, `13_workflow_os` | **13_evidence_control_plane** wins |
| 14 | 3 | `14_DAY_FIRST_REVENUE_PLAYBOOK.md`, `14_proof`, `14_trust_os` | Keep all (md file + 2 dirs) |
| 15 | 3 | `15_auditability`, `15_evidence_control_plane`, `15_value` | **15_evidence_control_plane** wins |
| 16 | 3 | `16_agents`, `16_capital`, `16_evidence_control_plane` | **16_agents** wins |
| 17-44 | 2 each | Various | Evaluate individually |

### 🔴 CRITICAL: Duplicate Frontend
| Location | Status | Action |
|----------|--------|--------|
| `frontend/` | ✅ **Canonical** | Keep — primary Next.js app with i18n, ops surfaces |
| `apps/web/` | ⚠️ Legacy/duplicate | Evaluate page-by-page; merge unique pages into `frontend/` then archive |

Unique pages in `apps/web/` to preserve:
- `/control-plane` → merge into `frontend/[locale]/ops/`
- `/data-room` → merge into `frontend/`
- `/proof-vault` → merge into `frontend/`
- `/war-room` → `frontend/` already has ops/war-room

### 🟡 Duplicate Scripts (same purpose)
| Script 1 | Script 2 | Status |
|----------|----------|--------|
| `scripts/verify_dealix_commercial_go_live.sh` | `scripts/verify_commercial_launch_ready.py` | Keep both (sh for founder, py for CI) |
| `scripts/dealix_smoke_test.py` | `scripts/production_smoke.py` (implied) | Consolidate |

### 🟡 Overlapping Workflows
| Workflow | Category | Status |
|----------|----------|--------|
| `daily-revenue-machine.yml` | Founder automation | Keep but mark optional |
| `founder_commercial_daily.yml` | Founder automation | Keep but mark optional |
| `founder_business_autopilot.yml` | Founder automation | Keep but mark optional |
| `governed-full-ops-daily.yml` | Founder automation | Keep but mark optional |
| `autonomous_executive_day.yml` | Founder automation | **Question value** — 40+ similar workflows |

## Files to Archive Later (do not delete now)

1. `DEALIX_Market_Launch_Bundle_v1.zip` — Archive artifact, not source code
2. `dealix_market_domination_pack_v12_part1_core_repo.tar.xz` — Archive artifact
3. `dealix_market_domination_pack_v12_part2_archive_history.tar.xz` — Archive artifact
4. `dealix_market_domination_pack_v4.zip` — Archive artifact
5. Duplicate numbered doc directories (after content extraction)
6. `apps/web/` (after merging unique pages)

## Naming Conventions
- Python: `snake_case.py`
- Tests: `test_*.py` or `*_test.py`
- Workflows: `kebab-case.yml`
- Docs: `UPPER_SNAKE_CASE_AR.md` for Arabic commercial docs
- Scripts: `snake_case.py` / `snake_case.sh`
