# Dealix AI Stack — Eleven-Layer Overview / نظرة شاملة على ستاك الذكاء الصناعي

> Status: production-ready (Wave 15) · Default tier: free_diagnostic · Doctrine-clean by construction.

## 1. The Stack at a Glance — الستاك بنظرة سريعة

The Dealix AI Stack is the canonical eleven-layer execution path for every
customer-facing AI action the business runs. Every layer is governed,
hash-bound to an evidence chain, and translated bilingually (AR + EN).

```
[Customer Intake]
        ↓
L1  Source Passport         ←  data sovereignty gate
L2  Data Quality            ←  deterministic single-record DQ score
L3  Intelligence / RAG      ←  hybrid dense + BM25 retrieval
L4  Model Router            ←  task → quality / latency / cost class
L5  Agent Mesh              ←  15+ agents, governed handlers
L6  Governance Gate         ←  policy + approval + claim-safety
L7  Proof Pack v2           ←  bilingual 14-section artifact
L8  Value Ledger            ←  skipped until invoice_paid
L9  Capital Ledger          ←  Proof Pack registered as capital asset draft
L10 Adoption / Retainer     ←  recommendation only — no auto upsell
L11 Self-Evolving           ←  shadow-mode feedback, founder-gated proposals
        ↓
[Proof Pack + Decision Passports + Capital Draft + Recommendation]
```

عربياً: الستاك إحدى عشرة طبقة منضبطة. كل قرار محكوم، كل أداة تحمل جواز
مصدر، وكل مخرج عميل ثنائي اللغة بشكل قسري. لا إيراد قبل دفع الفاتورة،
ولا اتصالات خارجية بدون موافقة المؤسس.

---

## 2. Per-Layer Contracts — عقود الطبقات

| Layer | Module | Input | Output |
|-------|--------|-------|--------|
| **L1** Source Passport | `auto_client_acquisition.data_os.source_passport` | `SourcePassportInput` | (ok, errors) |
| **L2** Data Quality | `auto_client_acquisition.data_os.data_quality_score` | intake record | 0..100 score + breakdown |
| **L3** Intelligence / RAG | `auto_client_acquisition.intelligence_os.rag_pipeline` | query + tenant-scoped index | `RetrievedContext` |
| **L4** Model Router | `auto_client_acquisition.ai.model_router` | `ModelTask` | `ModelRoute` (quality, latency, cost) |
| **L5** Agent Mesh | `auto_client_acquisition.agent_os.agent_mesh` | `TaskPlan` | `MeshTrace` |
| **L6** Governance Gate | `auto_client_acquisition.governance_os.runtime_decision` | action + context | `RuntimeDecision` |
| **L7** Proof Pack v2 | `auto_client_acquisition.proof_os.proof_pack` | section content (AR + EN) | `ProofPackV2` + Markdown |
| **L8** Value Ledger | `auto_client_acquisition.value_os.value_ledger` | confirmed monetary event | `ValueEvent` (post-invoice_paid only) |
| **L9** Capital Ledger | `auto_client_acquisition.capital_os.capital_ledger` | reusable asset | `CapitalAsset` |
| **L10** Adoption / Retainer | `auto_client_acquisition.adoption_os.retainer_readiness` | adoption + proof scores | `RetainerReadiness` |
| **L11** Self-Evolving | `auto_client_acquisition.self_evolving_os` | feedback events | `ImprovementProposal` (pending approval) |

---

## 3. Hard Gates — الضمانات الصارمة

These are surfaced on every `GET /api/v1/ai-stack/status` response so
operators can verify the stack is wired correctly:

- `no_live_send` — no WhatsApp / LinkedIn / Gmail outbound; drafts only.
- `no_live_charge` — no Moyasar / Stripe charges initiated by the stack.
- `no_invented_kpis` — every metric originates from a known source.
- `no_revenue_before_invoice_paid` — value ledger remains advisory.
- `source_passport_required` — every AI use is gated by L1.
- `bilingual_required` — AR + EN mandatory on every customer artifact.
- `self_evolving_shadow_only` — L11 never auto-applies changes.

---

## 4. Public Endpoints — نقاط الوصول العامة

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/ai-stack/run` | `POST` | Execute the full L1..L11 stack |
| `/api/v1/ai-stack/status` | `GET` | Eleven-layer health snapshot |
| `/api/v1/ai-stack/layers` | `GET` | Descriptive map + hard gates |
| `/api/v1/ai-stack/run/{run_id}` | `GET` | Fetch a stored result |
| `/api/v1/ai-stack/proposals/{tenant}` | `GET` | List shadow-mode improvement proposals |

UI: `/ar/ai-stack` (Arabic primary, English fallback). The demo form
exercises the `free_diagnostic` tier and runs in <50ms with the
deterministic default handlers.

---

## 5. The Five Offer Tiers — مستويات العروض الخمس

| Tier | Price (SAR) | Task Plan |
|------|-------------|-----------|
| `free_diagnostic` | 0 | ICP → Pain |
| `sprint_499` | 499 | ICP → Pain → Qualification → Proposal |
| `data_pack_1500` | 1,500 | + Sector Intel (optional) |
| `managed_ops` | 2,999–4,999/mo | + Retainer recommendation |
| `custom_ai` | 5K–25K | bespoke handlers; identical L1..L11 path |

The orchestrator routes the agent mesh based on the `offer_tier` field of
the input. Higher tiers add agents; lower tiers short-circuit after
diagnostic agents.

---

## 6. Quick Start — البداية السريعة

```python
from auto_client_acquisition.ai_stack_os import (
    AIStackInput, AIStackOrchestrator, Offer, SourcePassportInput,
)

payload = AIStackInput(
    tenant_id="acme",
    customer_handle="acme",
    company_name="Acme Corp",
    sector="technology",
    challenge_ar="نحتاج تحسين عملية البيع",
    challenge_en="we need to improve our sales process",
    offer_tier=Offer.FREE_DIAGNOSTIC,
    source_passport=SourcePassportInput(
        source_id="intake_001",
        owner="acme",
        ai_access_allowed=True,
    ),
)
result = AIStackOrchestrator().run(payload)
print(result.proof_pack_markdown)
```

---

## 7. References — مراجع

- [LAYER_CONTRACTS.md](./LAYER_CONTRACTS.md) — full layer contracts (input/output/SLO).
- [RUNBOOK.md](./RUNBOOK.md) — operations, debugging, rollback.
- [`docs/AI_STACK_DECISIONS.md`](../AI_STACK_DECISIONS.md) — stack vendor / framework choices.
- [`docs/ARCHITECTURE_LAYER_MAP.md`](../ARCHITECTURE_LAYER_MAP.md) — canonical → folder mapping.
