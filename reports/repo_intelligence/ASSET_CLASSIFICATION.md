# Dealix Asset Classification

**Date:** 2026-06-23

## Classification key

| Tag | Meaning |
|---|---|
| keep | Core startup system; keep, stabilize, improve |
| merge | Useful ideas but scattered; merge into canonical files |
| refactor | Has value but needs cleanup |
| archive | Superseded or experiment; move to archive/ later |
| ignore generated | Build/runtime output; do not commit |
| dangerous / review | Live-send, secrets, compliance-critical; always review |
| duplicate / superseded | Multiple versions of same concept; pick one |

## Top-level directory classification

| Directory | Tag | Rationale |
|---|---|---|
| api/ | keep | FastAPI backend, routers, dependencies |
| app/ | keep | Outbound policy gate and shared modules |
| auto_client_acquisition/ | keep + dangerous | Core revenue/email/WhatsApp engine; many modules need consolidation; live-send modules require strict review |
| autonomous_growth/ | merge | SEO/content/distribution engine; merge useful parts into GTM layer |
| brand/ | keep | Visual identity, logos, colors, images |
| business/ | keep | Product docs, proposals, contracts, playbooks |
| business_autopilot/ | archive | Older templates superseded by newer docs |
| clients/ | keep | Client intake, delivery, proof templates |
| company/ | keep | Company operating packs and reports |
| core/ | keep | Config, logging, errors, utilities |
| data/ | keep | Seed data and templates |
| db/ | keep | SQLAlchemy models |
| dealix/ | keep | Core dealix modules, registers, trust checks |
| demos/ | archive | Demo assets; may be reused for sales enablement later |
| design-skills/ | archive | Design skill templates; not runtime code |
| design-systems/ | archive | Superseded by brand/ and frontend/ design system |
| docs/ | keep + merge | Many useful operating docs; need consolidation |
| evals/ | refactor | Evaluation harness; possibly merge into tests/ |
| executive/ | merge | Executive docs; merge into Company Brain OS |
| founder_os/ | merge | Founder operating system; merge into canonical founder docs |
| frontend/ | keep | Primary Next.js dashboard and public website |
| apps/web/ | refactor | Lightweight Next.js app; evaluate if needed separately |
| integrations/ | keep + dangerous | Email/WhatsApp integrations; live-send review required |
| intelligence/ | merge | Intelligence assets; merge into Company Brain OS |
| intelligence_os/ | merge | Same as above |
| landing/ | archive | Old landing pages; likely superseded by frontend/ |
| ledgers/ | keep | Operating CSV ledgers |
| mcp_server/ | merge | MCP server; may be useful but not core now |
| memory/ | merge | Memory system; possibly core for Company Brain |
| observability/ | merge | Observability adapters; merge into ops docs |
| ops/ | keep | Operational scripts |
| os/ | merge | Generic OS folder; classify contents |
| outbox/ | ignore generated | Generated drafts |
| outreach-execution/ | keep | Outreach execution scripts |
| patches/ | archive | Patch files |
| platform/ | keep | Platform core |
| platform_core/ | merge | Overlaps with platform/ |
| presentations/ | archive | Presentation files |
| projects/ | archive | Project experiments |
| prompts/ | keep | LLM prompt library |
| qa/ | merge | QA docs; merge into tests/ and delivery |
| readiness/ | archive | Readiness framework; superseded by trust/compliance docs |
| reports/ | ignore generated | Generated reports except intentionally committed templates |
| sales/ | keep + merge | Sales playbooks and sector angles; need consolidation |
| schemas/ | keep | Data schemas |
| scripts/ | keep | Revenue, command room, server scripts |
| self_evolving_os/ | archive | Self-improvement experiments; not core launch |
| simulations/ | archive | Simulations; possibly useful for tests later |
| supabase/ | keep | Supabase migrations if any |
| templates/ | keep | Outreach, contract, scale templates |
| tests/ | keep | Test suite |
| token-optimizer/ | archive | Token optimization skills; not runtime |
| tools/ | keep | Utility tools |
| transformation/ | merge | Transformation assets |
| transformation_os/ | merge | Overlaps with client delivery and company brain |
| workflows/ | keep | Sales and delivery workflows |

## Important files

### Keep and protect
- `core/config/settings.py` — env-safe defaults
- `app/outbound/policy_gate.py` — live send policy gate
- `scripts/verify_no_auto_external_send.py` — safety scanner
- `tests/test_no_auto_send.py` — safety contract test
- `ledgers/*.csv` — operating ledgers
- `.gitleaks.toml` — secret detection
- `docker-compose.yml` — local infra
- `railway.toml` — production deployment

### Review before use
- `auto_client_acquisition/email/gmail_send.py`
- `auto_client_acquisition/whatsapp_safe_send.py`
- `auto_client_acquisition/email/transactional.py`
- `auto_client_acquisition/email/whatsapp_multi_provider.py`
- `api/routers/email_send.py`
- `api/routers/whatsapp_client_os.py`
- `integrations/email.py`
- `integrations/whatsapp.py`

### Consolidate / merge candidates
- `docs/DEALIX_COMPANY_OS_MAP_AR.md` and `docs/DEALIX_OPERATING_CONSTITUTION.md` into `docs/company/DEALIX_COMPANY_OS_AR.md`
- `docs/COMPANY_SERVICE_LADDER.md` into `business/products/SERVICE_LADDER_AR.md`
- `docs/COMMERCIAL_WIRING_MAP.md` into `business/products/REVENUE_COMMAND_ROOM_OS.md`
- `business/products/CONTROLLED_LIVE_OUTBOUND_OS.md` into trust and outbound code docs
- `founder_os/` into `docs/company/FOUNDER_OPERATING_SYSTEM_AR.md`
- `executive/` into `scripts/brain/` and `reports/brain/`

## Archive candidates (do not delete yet; classify first)

- `business_autopilot/`
- `landing/`
- `patches/`
- `presentations/`
- `demos/` (keep select demo scripts for sales)
- `projects/`
- `design-skills/`
- `design-systems/`
- `token-optimizer/`
- `readiness/`
- `self_evolving_os/`
- `simulations/`

## Generated / do not commit

- `.venv/`
- `.pytest_cache/`
- `node_modules/`
- `frontend/.next/`
- `outbox/`
- `reports/` (except `.gitkeep` and intentional templates)
- `dealix.egg-info/`
- `__pycache__/`
- `.env.production`

## Do-not-break contracts

1. `tests/test_no_auto_send.py` must always pass.
2. `scripts/verify_no_auto_external_send.py` must always pass before any commit.
3. Ledgers must keep canonical CSV headers.
4. `.env.example` must keep live-send flags false.
5. `app/outbound/policy_gate.py` must keep explicit opt-in/approval/rate-limit gates.
6. No fake clients, testimonials, or ROI numbers in any committed file.
