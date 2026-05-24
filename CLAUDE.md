# CLAUDE.md — Dealix Working Context

> هذا الملف يُعطي Claude (السياقات القادمة) فهماً سريعاً للمشروع. يُحدّث عند تغييرات استراتيجية.

## Project Identity
**Dealix** — Saudi B2B Revenue Engine: Lead Engine + Service Engine + Trust Engine.
PDPL-native, ZATCA Phase 2, Arabic-first, approval-first governance.

## Current Stage (2026-05-24)
- **Status:** LAUNCHED (technical) → 0 paid customers (Day 1 of commercial activation)
- **Active branch:** `claude/wonderful-thompson-DelTr`
- **Master plan:** `/root/.claude/plans/moonlit-leaping-lollipop.md`
- **Production URL:** https://api.dealix.me
- **Landing:** https://voxc2.github.io/dealix/

## Critical Blockers
1. **Moyasar account** — `account_inactive_error` (KYC pending). Tap.company being built as backup.
2. **First DM not sent** — 50 warm leads in `docs/ops/pipeline_tracker.csv`, all `status=pending`.

## What's WORKING (don't rebuild)
- 171 FastAPI routers (`api/routers/`)
- Multi-LLM router with 6 providers + cost tracking + prompt caching (`core/llm/`)
- 9-Layer OS Stack: `data_os`, `governance_os`, `proof_os`, `value_os`, `capital_os`, `adoption_os`, `client_os`, `sales_os`, `revenue_os`
- 5 Claude sub-agents in `.claude/agents/`: dealix-pm, dealix-engineer, dealix-content, dealix-sales, dealix-delivery
- 14 Alembic migrations applied
- Anthropic + GPT + Gemini + Groq + DeepSeek + GLM-4 routing
- Prompt caching (90% cost savings)
- Tool use / function calling
- Cost tracker (`dealix/observability/cost_tracker.py`) — Postgres + ring buffer fallback
- Value Ledger with L0-L5 evidence tiers
- 11 Non-Negotiables enforced in `api/routers/agent_os.py` + `dealix/commercial_ops/doctrine.py`

## What's PARTIAL (in progress)
- **RAG embeddings**: vectors generate, but `scripts/embeddings_pipeline_placeholder.py` blocks production upsert. Supabase pgvector not yet wired. **Track C.3** (Day 30-50).
- **Eval framework**: 5 YAML scaffolds exist, golden labels = STUB. **Track C.4** (Day 45-65).
- **Trust Plane (Approval/Audit/Policy)**: in-memory only, needs Postgres migration. **Track D** (Day 30-60).
- **DecisionOutput**: defined but not wired on every agent. **Track D.1** (Day 30-40).

## Active Work (Day 1 — Track A + B + E)
Currently being built by sub-agents (in parallel):
- **Track B.1:** Tap.company payment integration (`dealix/payments/tap.py`)
- **Track B.4:** Customer Portal Backend (`api/routers/customer_portal.py`)
- **Track B.3:** Proposal Renderer (`dealix/commercial_ops/proposal_renderer.py`)
- **Track E:** Day 1-7 Content Pack (`docs/ops/DAY1_TO_DAY7_CONTENT_PACK_AR.md`)
- **Track A:** Founder Sales Operating Playbook (`docs/sales/FOUNDER_SALES_OPERATING_PLAYBOOK_DAY1_14_AR.md`)

## The 11 Non-Negotiables (codified — NEVER break)
1. No agent without identity + owner
2. No project without Proof Pack (score ≥ 70)
3. No project without Capital Asset registration
4. No source-less knowledge answers
5. No PII in logs
6. No cold WhatsApp / LinkedIn automation
7. No fake claims
8. No guaranteed sales outcomes
9. No external action without approval
10. No scraping systems
11. Governance decision field on all outputs

Plus: PDPL-aware, ZATCA-ready, Saudi-native (SAR/Hijri/Riyadh), bilingual AR+EN, no revenue before paid (L5), no upsell before proof (≥70).

## Key Files (Don't Duplicate)
| What | Path |
|---|---|
| Pricing | `dealix/config/pricing.yaml` |
| No-Overclaim Register | `dealix/registers/no_overclaim.yaml` |
| 90-Day Matrix | `dealix/registers/90_day_execution.yaml` |
| Saudi Compliance | `dealix/registers/compliance_saudi.yaml` |
| Tech Radar | `dealix/registers/technology_radar.yaml` |
| Constitution | `dealix/masters/constitution.md` |
| LLM Router | `core/llm/router.py` |
| ICP Matcher | `auto_client_acquisition/agents/icp_matcher.py` |
| Moyasar Client | `dealix/payments/moyasar.py` |
| PDPL Helpers | `integrations/pdpl.py` |
| ZATCA | `integrations/zatca.py` |
| Pipeline tracker | `docs/ops/pipeline_tracker.csv` (50 warm leads) |
| Launch DMs | `docs/ops/launch_content_queue.md` |
| War Room | `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md` |

## How to Run / Test
```bash
# Tests (use python -m, NOT standalone pytest binary)
python -m pytest tests/test_model_router.py -q --no-cov

# Quick regression bundle (from AGENTS.md)
python -m pytest tests/test_pg_event_store.py tests/test_model_router.py tests/test_integrations.py -q --no-cov

# Verify scripts
bash scripts/verify_dealix_commercial_go_live.sh
bash scripts/founder_weekly_loop.sh
```

## Founder Identity
**Name:** Bassam M. Assiri  
**Email:** bassam.m.assiri@gmail.com  
**Role:** Founder/CEO — single decision-maker for everything

## When Working (rules for future Claude sessions)
1. **READ this CLAUDE.md first** + master plan at `/root/.claude/plans/moonlit-leaping-lollipop.md`
2. **NEVER** push to non-`claude/*` branches
3. **NEVER** send external messages (LinkedIn, WhatsApp, email) — drafts only, founder approves
4. **NEVER** add `--no-verify` to git commits
5. **NEVER** charge customers in code paths (test mode only until founder explicit go-live)
6. **ALWAYS** check no_overclaim register before adding new product claims
7. **ALWAYS** prefer existing code over new code (171 routers — search first!)
8. **ALWAYS** use bilingual AR+EN for customer-facing artifacts
9. **ALWAYS** use SAR + 15% VAT + Hijri-aware for Saudi context

## Architecture (one sentence)
Decision Plane (agents) → Trust Plane (policy/approval/audit) → Execution Plane (workflows) ↔ Data Plane (Postgres) ↔ Operating Plane (CI/CD), with multi-LLM routing, bilingual outputs, Saudi compliance wiring, and human-in-the-loop on all external commitments.
