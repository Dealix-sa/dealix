# AI Stack — Operations Runbook / دليل التشغيل

This document is the operational counterpart to
[AI_STACK_OVERVIEW.md](./AI_STACK_OVERVIEW.md) and
[LAYER_CONTRACTS.md](./LAYER_CONTRACTS.md). When something looks wrong in
the stack, start here.

---

## 1. Quick Health Check / فحص سريع

```bash
curl -s http://localhost:8000/api/v1/ai-stack/status | jq '.overall_healthy, .layers[] | {layer, healthy}'
```

Expected: `overall_healthy: true` and every layer `healthy: true`. If a
layer reports `healthy: false`, the `detail` field shows the import error.
The most common cause is a missing optional dependency in CI — install it
or set the module path to a stub.

---

## 2. Running the Tests / تشغيل الاختبارات

```bash
pytest tests/test_proof_os_v2.py \
       tests/test_intelligence_rag.py \
       tests/test_agent_mesh_orchestration.py \
       tests/test_self_evolving_shadow.py \
       tests/test_ai_stack_orchestrator.py \
       tests/test_ai_stack_router.py \
       tests/test_ai_stack_doctrine.py \
       --no-cov -v
```

All 127 tests should pass with no skips. The doctrine tests (last file)
are non-negotiable — a failure here is a Doctrine violation, not a flake.

---

## 3. Running the Demo UI / تشغيل واجهة العرض

```bash
# Backend
uvicorn api.main:app --reload --port 8000

# Frontend
cd frontend && pnpm dev
```

Then open <http://localhost:3000/ar/ai-stack> for the Arabic-primary view
or <http://localhost:3000/en/ai-stack> for the English view.

---

## 4. Common Failures / المشاكل الشائعة

### 4.1 `ai_access_denied` at L1

**Symptom:** every run returns `governance_blocked=True` at L1.
**Cause:** the source passport's `ai_access_allowed` field is `False`.
**Fix:** set `ai_access_allowed=True` on the Source Passport descriptor.

### 4.2 `pii_external_use_requires_approval_workflow` at L1

**Symptom:** L1 blocks with a PII / external-use mismatch.
**Cause:** the passport has `contains_pii=True` AND `external_use_allowed=True`.
**Fix:** Either set `external_use_allowed=False` or route the run through
the approval workflow (governance_os will queue the action).

### 4.3 `missing_handler:<agent_id>` at L5

**Symptom:** the mesh halts at L5 with a missing handler.
**Cause:** the agent registry has no handler bound for that agent_id.
**Fix:** in production, call `mesh.register(card=..., handler=...)` for
every agent_id listed in `agents_required_for_tier(<offer_tier>)`. The
default orchestrator ships with deterministic handlers for every required
agent, so this only fires after a custom mesh is injected.

### 4.4 Governance hard block on guaranteed claims

**Symptom:** the run completes but `governance_blocked=True` and
`doctrine_clean=False`.
**Cause:** the input or generated text contained a guaranteed-outcome
phrase ("100% guaranteed", "نضمن نتائج", "guaranteed revenue", …).
**Fix:** these are caught by design — DO NOT bypass. Re-phrase the
content. Founder review is required to publish anything from the run.

### 4.5 Empty RAG context

**Symptom:** L3 reports `0 hits` and `used_chars=0`.
**Cause:** no documents were indexed for the tenant + namespace.
**Fix:** call `RAGPipeline.index_documents(tenant_id, documents)` before
`retrieve()`, or pass `rag_documents` in the `AIStackInput`.

### 4.6 Self-Evolving proposals show no items

**Symptom:** `GET /api/v1/ai-stack/proposals/{tenant_id}` returns
`proposal_count: 0` even after many runs.
**Cause:** the learning store has no events meeting the severity
threshold. Doctrine-clean runs always settle at severity `info`, which is
the default minimum.
**Fix:** lower the threshold with `?minimum_severity=info` (the default),
or wait until a doctrine-dirty event lands in the store.

---

## 5. Rollback Procedures / إجراءات الاسترجاع

### 5.1 Roll back the migration

```bash
alembic downgrade 013
```

This drops `ai_learning_events` and `ai_improvement_proposals`. The
default orchestrator falls back to in-memory storage automatically.

### 5.2 Disable the AI Stack router

Comment out the registration line in `api/main.py`:

```python
# app.include_router(ai_stack_router.router)
```

Routes return 404; existing endpoints remain unaffected.

### 5.3 Reset orchestrator state in tests

```python
from api.routers.ai_stack import reset_orchestrator_for_tests
reset_orchestrator_for_tests()
```

Clears the in-memory result store + reinitializes the orchestrator. Tests
in `test_ai_stack_router.py` already do this in a fixture.

---

## 6. Observability / المراقبة

| Signal | Where |
|--------|-------|
| Layer health | `GET /api/v1/ai-stack/status` |
| Per-run duration | `AIStackResult.duration_ms` |
| Per-layer duration | `LayerResult.duration_ms` |
| Evidence chain head | `AIStackResult.evidence_head_hash` |
| Feedback events | `InMemoryLearningStore.list_events()` |
| Improvement proposals | `GET /api/v1/ai-stack/proposals/{tenant_id}` |
| Doctrine cleanliness | `AIStackResult.doctrine_clean` |

For production deployments, instrument the orchestrator's `run()` method
with the existing Langfuse / structlog adapters — emit a single span per
run with the run_id as the span id, and a child span per layer.

---

## 7. Adding a New Layer / إضافة طبقة جديدة

The eleven layers are the canonical set. Adding a twelfth is a major
change — it requires:

1. A constitution-level decision (see `dealix/masters/constitution.md`).
2. A new entry in `_LAYER_MODULES` in `ai_stack_os/layer_health.py`.
3. A new layer execution block in `ai_stack_os/orchestrator.py` with
   evidence chain link, status emission, and feedback event.
4. A new check constraint value in the
   `db/migrations/versions/20260525_014_ai_learning_events.py` CHECK clause
   (or a follow-up migration).
5. A new section in this runbook + the layer contracts doc.

Do not add a layer just to inject a side effect — wrap the side effect in
an agent handler that the mesh already understands.

---

## 8. Escalation / الإصعاد

Any of the following is a Doctrine incident, not a bug:

- Self-Evolving applies a change without `pending → approved → applied`.
- Value ledger records revenue without an `invoice_paid` webhook.
- A customer artifact ships without bilingual sections.
- An external action fires without governance approval.

Page the founder. Do not roll forward.
