# Dealix Canonical Map

_Last reviewed: 2026-06-07_

Cuts through repository sprawl (2,500+ markdown files, 170+ `auto_client_acquisition/*_os` dirs, 3 web surfaces) so the **real, operating company** is findable. This is an **index, not a demolition order** — almost every `*_os` module is cross-imported, so mass deletion would break the 535-test suite. Verify with `scripts/audit_module_imports.py` before touching anything.

> **How to re-audit:** `python3 scripts/audit_module_imports.py` (full table) or
> `--orphans` (zero-reference modules). NOTE: the absolute-import regex can
> under-count multi-line `from auto_client_acquisition import (\n  mod,\n …)`
> blocks — always cross-check with a bare-string grep before archiving
> (that is how `sandbox_os` was caught as *used*, see below).

## 1. CANONICAL — the operating company (the spine)

The minimum that makes Dealix a real, daily-operating business. Touch with care.

| Area | Path(s) |
|---|---|
| Public website (single canonical surface) | `frontend/` (Next.js 15) |
| Static SEO/marketing satellite | `landing/` (60+ HTML) |
| Backend API | `api/` (FastAPI, 90+ routers, 946 routes) |
| Core OS modules (implemented + tested) | `auto_client_acquisition/{data_os,governance_os,proof_os,value_os,capital_os,adoption_os,client_os,sales_os}/`, `friction_log` |
| Canonical offers/pricing source | `auto_client_acquisition/service_catalog/registry.py` |
| Daily lead engine | `scripts/dealix_daily_lead_prep.py`, `scripts/dealix_build_warmlist.py`, `.github/workflows/dealix_daily_lead_board.yml` |
| Lead capture + founder review | `api/routers/public.py`, `auto_client_acquisition/lead_inbox.py`, `api/routers/founder.py` (`/daily-board`, `/leads`) |
| Revenue ops store (war-room) | `dealix/revenue_ops_autopilot/` |
| Real prospect data (public business info) | `docs/ops/lead_machine/SAUDI_LEAD_GRAPH_MASTER.csv` |
| Persistence / migrations | `db/`, `alembic/` |
| Doctrine | `docs/OFFER_LADDER_AND_PRICING.md`, `dealix/registers/no_overclaim.yaml`, `tests/test_doctrine_guardrails.py` |

**Deprecated web surface:** `apps/web/` — superseded by `frontend/`. See `apps/web/DEPRECATED.md`. Do not add features.

## 2. IMPORTED-PERIPHERAL — keep, do not archive

~165 `auto_client_acquisition/*` submodules each referenced by ≥1 router/script/sibling. Examples (external ref counts from the auditor): `proof_ledger` 35, `approval_center` 35, `self_growth_os` 32, `governance_os` 29, `revenue_os` 24, `agents` 22, `customer_data_plane` 21, `data_os` 15, `value_os` 14, `delivery_os` 15. These are wired into the live app even if peripheral to the spine — **archiving them breaks imports/tests.**

Special cases the naive auditor mis-flags (verified *in use*):
- `sandbox_os` — included as a router in `api/main.py` (multi-line import, missed by the absolute-ref regex).
- `saudi_layer` — referenced as a string key in `auto_client_acquisition/dealix_master_layers/registry.py` and asserted by `tests/test_dealix_master_layers_registry.py`.

## 3. ARCHIVED — proven orphaned (moved this pass)

Zero occurrences anywhere in the repo (`*.py`, `*.tsx`, `*.json`, `*.yaml`, configs):

| Module | New location |
|---|---|
| `ai_estate_os` | `auto_client_acquisition/_archive/ai_estate_os/` |
| `business_ops` | `auto_client_acquisition/_archive/business_ops/` |

Moved via `git mv` (history preserved). App import verified clean afterward (`from api.main import app` → 946 routes). Not deleted — recoverable if ever needed.

## 4. Candidates for a future pass (NOT moved — need a human call)

The repo still carries many aspirational `*_os` scaffolds (`endgame_os`, `dominance_os`, `moat_os`, `sovereignty_os`, `operating_empire_os`, …). Most have low but non-zero ref counts (often only cross-referenced by other scaffolds). Consolidating them is **P2** and requires deciding whether the cross-references are load-bearing — out of scope for the activation spine. Re-run the auditor and grep bare strings before moving any.
