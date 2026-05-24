# AI Stack — Per-Layer Contracts / عقود الطبقات

Each layer in the Dealix AI Stack publishes a strict contract: input shape,
output shape, side effects (if any), latency budget, and the failure modes
the orchestrator knows how to handle. This document is the source of truth
for handler authors and reviewers.

---

## L1 — Source Passport (data_os) / جواز المصدر

**Module:** `auto_client_acquisition.data_os.source_passport`

| Field | Type |
|-------|------|
| Input | `SourcePassport` (canonical institutional record) |
| Output | `(ok: bool, errors: tuple[str, ...])` |
| Side effects | none |
| Latency budget | < 1ms |

**Failure modes:** missing `source_id`, missing `allowed_use`,
`ai_access_allowed=False`, PII flagged for external use without an approval
workflow. Each is a discrete machine-stable error key.

**Doctrine guarantee:** if L1 returns `ok=False`, the orchestrator **MUST
NOT** progress to L2..L11. The run is short-circuited and a feedback event
of kind `blocked_by_governance` is recorded.

---

## L2 — Data Quality (data_os) / جودة البيانات

**Module:** `auto_client_acquisition.data_os.data_quality_score`

| Field | Type |
|-------|------|
| Input | a single intake record (`Mapping[str, Any]`) |
| Output | `(score: 0..100, breakdown: dict)` |
| Side effects | none |
| Latency budget | < 1ms |

The orchestrator computes completeness against the canonical required keys
(`company_name`, `sector`, `challenge_ar`, `source`) plus a +10 bilingual
bonus when `challenge_en` is provided.

---

## L3 — Intelligence / RAG (intelligence_os)

**Module:** `auto_client_acquisition.intelligence_os.rag_pipeline`

| Field | Type |
|-------|------|
| Input | `RAGPipeline.retrieve(tenant_id, query, top_k, max_context_chars)` |
| Output | `RetrievedContext(hits, context_text, used_chars, truncated, ...)` |
| Side effects | upsert vectors into the in-memory store on `index_documents()` |
| Latency budget | < 10ms for top-k ≤ 10, dimension ≤ 1024 |

**Dimensional invariants:**

- The embedder and store MUST share the same dimension or the pipeline
  raises `ValueError` at construction time.
- All vectors are L2-normalized; cosine similarity == dot product.

**Hybrid retrieval blend:** default `0.7 dense + 0.3 sparse (BM25)`.

---

## L4 — Model Router (ai/) / موجّه النموذج

**Module:** `auto_client_acquisition.ai.model_router`

| Field | Type |
|-------|------|
| Input | `ModelTask` enum |
| Output | `ModelRoute(quality_tier, latency, cost_class, fallback_task, guardrail_required, eval_metric)` |
| Side effects | none |
| Latency budget | constant time (table lookup) |

Doctrine: the router is **never** mutated by L11; only an approved
proposal can swap routing weights.

---

## L5 — Agent Mesh (agent_os) / شبكة الوكلاء

**Module:** `auto_client_acquisition.agent_os.agent_mesh`

| Field | Type |
|-------|------|
| Input | `TaskPlan` (from `plan_for_offer()`) |
| Output | `MeshTrace(offer_tier, runs, halted, halt_reason)` |
| Side effects | invokes registered handler callables |
| Latency budget | sum of handler runtimes; default handlers < 5ms each |

**Halt behavior:**

- Required task error → halt + `halt_reason` set.
- Optional task error → recorded, mesh continues.
- Missing handler → halt.
- Killed agent card → halt.

The mesh produces a Decision Passport per OK run, sealing the per-agent
output with a content hash.

---

## L6 — Governance Gate (governance_os) / بوابة الحوكمة

**Module:** `auto_client_acquisition.governance_os.runtime_decision`

| Field | Type |
|-------|------|
| Input | `action_type`, `context` (text + risk_score + external_use), `actor` |
| Output | `RuntimeDecision(decision, reason, risk_level, approval_required, safe_alternative, evidence)` |
| Side effects | none (caller persists evidence) |
| Latency budget | < 2ms |

**Decisions:** `allow` · `allow_with_monitoring` · `escalate` · `block`.

Hard block triggers (orchestrator-level redundant scan): any of
`100% guaranteed`, `نضمن نتائج`, `guaranteed revenue` in the rendered
proof pack body sets `doctrine_clean=False` and `governance_blocked=True`.

---

## L7 — Proof Pack v2 (proof_os) / حزمة الإثبات

**Module:** `auto_client_acquisition.proof_os.proof_pack`

| Field | Type |
|-------|------|
| Input | accumulated section content (AR + EN) per the 14 canonical sections |
| Output | `ProofPackV2` + Markdown + JSON |
| Side effects | none |
| Latency budget | < 2ms render |

Bilingual completeness is enforced: `is_complete()` returns `False` if any
section is missing in either language.

---

## L8 — Value Ledger (value_os) / سجل القيمة

**Module:** `auto_client_acquisition.value_os.value_ledger`

| Field | Type |
|-------|------|
| Input | `customer_id`, `kind`, `amount`, `tier`, `source_ref`, `confirmation_ref` |
| Output | `ValueEvent` |
| Side effects | append-only ledger (JSONL or Postgres) |
| Latency budget | < 5ms |

**Doctrine:** the orchestrator does NOT write to the value ledger during
a run. L8 is advisory-only until an external `invoice_paid` webhook fires.

---

## L9 — Capital Ledger (capital_os) / سجل الرأسمال

**Module:** `auto_client_acquisition.capital_os.capital_ledger`

| Field | Type |
|-------|------|
| Input | `customer_id`, `engagement_id`, `asset_type` |
| Output | `CapitalAsset` |
| Side effects | append-only ledger |
| Latency budget | < 5ms |

In the AI Stack the proof pack is **registered as a draft asset only**;
persistence to the durable ledger waits for governance clearance + invoice.

---

## L10 — Adoption / Retainer (adoption_os) / التبني والاحتفاظ

**Module:** `auto_client_acquisition.adoption_os.retainer_readiness`

| Field | Type |
|-------|------|
| Input | `customer_id`, `adoption_score`, `proof_score`, `workflow_owner_present`, `governance_risk_controlled` |
| Output | `RetainerReadiness(eligible, recommended_offer, gaps)` |
| Side effects | none |
| Latency budget | < 1ms |

The orchestrator surfaces the recommendation but **never** auto-upgrades
the customer's tier.

---

## L11 — Self-Evolving (self_evolving_os) / التحسين الذاتي

**Module:** `auto_client_acquisition.self_evolving_os`

| Field | Type |
|-------|------|
| Input | `FeedbackEvent` (from L8 / L10 / governance / doctrine) |
| Output | shadow-mode `ImprovementSuggestion`s + `ImprovementProposal`s |
| Side effects | append to learning store; submit pending proposals |
| Latency budget | < 5ms per event |

**Shadow-mode invariants:**

- `SELF_EVOLVING_SHADOW_ONLY == True` at module level.
- No `apply_now`, `auto_apply`, or `force_apply` functions exist.
- A proposal must pass `pending → approved → applied` via the repository
  state machine; illegal transitions raise `IllegalProposalTransition`.

---

## Cross-Layer SLOs / اتفاقيات مستوى الخدمة

| Metric | Budget |
|--------|--------|
| Full run (free_diagnostic) | < 100ms |
| Full run (managed_ops) | < 250ms (default handlers); LLM-backed handlers may extend |
| Layer health snapshot | < 50ms |
| Evidence chain verify | linear in number of links; < 5ms for 100 links |

Production deployments with real LLM handlers should push the orchestrator
behind a job queue and surface `run_id` to the client immediately.
