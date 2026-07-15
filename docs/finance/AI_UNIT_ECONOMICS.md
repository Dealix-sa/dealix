# AI Unit Economics

## Doctrine Anchor
- Non-negotiables touched: #2 (no value claim without source evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: control-plane verification scripts as release blockers.

## Purpose

Track whether AI usage creates profitable leverage. Every LLM call, embedding, retrieval, vector store write, and tool invocation costs money. This system measures cost per outcome — per lead, per enriched lead, per draft, per sample, per proposal, per qualified reply, per paid client — and forces a reroute or reduction when AI cost rises without conversion improvement.

## Cost Buckets

| Bucket | Description | Source |
|--------|-------------|--------|
| LLM input tokens | Tokens sent to the model | provider usage logs |
| LLM output tokens | Tokens received | provider usage logs |
| Embedding tokens | Vectorization of leads / documents / replies | embedding provider logs |
| Vector store ops | Writes, queries, retrievals | vector store logs |
| Tool / API calls | External enrichment, lookup, scraping providers | per-provider logs |
| Worker compute | ARQ + Redis + scheduled Action minutes | infra logs |
| Storage | DB rows + JSONL stores | DB / storage usage |

## Cost-per-Outcome Metrics

| Outcome | What we measure |
|---------|-----------------|
| LLM cost per lead in intelligence base | tokens × price ÷ leads added |
| Enrichment cost per lead | enrichment provider $ + LLM $ ÷ enriched leads |
| Scoring cost per lead | scoring run $ ÷ scored leads (deterministic scoring is nearly free) |
| Draft generation cost | LLM $ for outreach drafts ÷ drafts produced |
| Sample generation cost | LLM $ + retrieval $ for sample artifacts ÷ samples produced |
| Proposal draft cost | LLM $ for proposal generation ÷ proposals produced |
| Cost per positive reply | total AI $ in funnel ÷ positive replies received |
| Cost per paid sprint / client | total AI $ in funnel ÷ paid engagements |

## Core Rules

- If AI cost rises across a week without a matching improvement in conversion or quality, reduce, reroute, or downgrade the model.
- Prefer deterministic and retrieval-augmented paths over high-token freeform generation where conversion data shows parity.
- Per-tenant cost attribution is required; cross-tenant cost smearing is not allowed (doctrine #3).
- Public claims about "cost saved" or "automation savings" delivered to clients must reference a measured baseline and a measured post-change number — no estimates.
- A model upgrade is a pricing decision: it must be justified by either measurable quality lift or a cost reduction.

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Daily | Cost dashboard reviewed during the daily digest |
| Weekly | Cost-per-outcome review against last week |
| Monthly | Model and provider routing decision |

## Runtime Wiring

- Provider usage telemetry (logged per request): structlog JSON logs and provider usage metrics per `docs/OBSERVABILITY_ENV.md`.
- Optional tracing: Langfuse (per existing observability docs).
- Background job cost attribution: `db/models.py::BackgroundJobRecord`.
- Revenue events (denominator for cost-per-outcome): `auto_client_acquisition/revenue_memory/event_store.py`.
- Dashboard Costs page: `dashboard/pages/` (Costs page exists in the Streamlit shell).

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| LLM cost per lead | tracked, trending down per quarter | logs / events |
| LLM cost per paid client | tracked, target gross-margin contribution improves quarterly | logs / events |
| Spend per provider per week | tracked, model routing reviewed monthly | provider logs |
| Cross-tenant cost leakage | 0 | attribution checks |
| Public client claims without measured baseline | 0 | overclaim eval |

## Cross-Links

- `docs/UNIT_ECONOMICS_AND_MARGIN.md`
- `docs/company/UNIT_ECONOMICS.md`
- `docs/finance/PRICING_YIELD_MANAGEMENT.md`
- `docs/finance/BILLING_RECEIVABLES_OS.md`
- `docs/AI_OBSERVABILITY_AND_EVALS.md`
- `docs/OBSERVABILITY_ENV.md`
- `docs/engineering/OBSERVABILITY_SLO_SYSTEM.md`
- `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`

## Open Items

- A per-tenant cost-attribution view does not yet exist as a first-class dashboard panel.
- Cost-per-outcome metrics depend on each outcome being a recorded event; outcomes for samples and proposals are partial (lifecycle stages 5–6).
- Model routing decisions are made qualitatively today; a documented routing policy file is open.
