# Engineering Architecture

## Purpose
Define how Dealix engineering evolves from scripts and internal tools to productized software.

## Current Stage
Founder-led internal operating system.

## Current Architecture
- Python scripts
- CLI commands
- private ops files
- CSV/Markdown data
- local dashboard
- GitHub Actions checks

## Later Architecture
Only after SaaS readiness:
- apps/web
- api
- db
- worker
- auth
- billing
- customer portal
- admin dashboard

## Current Repo Layers
| Layer | Purpose |
|---|---|
| dealix_cli | command center |
| ops_runtime | metrics, reports, finance, assurance |
| control_plane | CEO decisions, priority routing |
| execution_engine | stage, evidence, advancement |
| internal_dashboard | local visual dashboard |
| scripts | runnable operations and verifiers |
| docs | operating systems and policies |
| schemas | data contracts |

## Rules
- CLI first.
- Scripts before services.
- Local dashboard before hosted dashboard.
- Internal automation before customer-facing product.
- API only after stable data model.
- SaaS only after repeated paid workflow.

## Evidence
- GitHub checks
- DORA metrics later
- productization candidates
- repeated workflow logs
