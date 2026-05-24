# AI Layers Doctrine Card — بطاقة الحوكمة للطبقات التسع

> الموقع التشغيلي: `auto_client_acquisition/ai_layers/` — الـ API: `/api/v1/ai-layers/*`.
> العقد التشغيلي: تأخذ `LayerContext` → تعيد `LayerResult` يحمل **دائماً** `governance_decision`.
> Pipeline: `run_pipeline(ctx)` يجمِّع 9 نتائج ويعيد `overall_decision = الأشد صرامة`.

## 1) خريطة الطبقات (Top-down)

| # | الطبقة | الوظيفة | الإدخال الإلزامي | حواجز إلزامية |
|---|---|---|---|---|
| 1 | `lead_scoring` | تقييم Lead من بيانات المؤسس فقط | `source_refs` | لا توجد بيانات → BLOCK |
| 2 | `account_scoring` | ترتيب الحسابات على ICP + readiness + deal size | `source_refs`, `account_name` | لا scraping |
| 3 | `content_generation` | مسودات ثنائية اللغة AR+EN | `topic`, `audience` | claim_safety + PII redaction → DRAFT_ONLY أو REDACT |
| 4 | `decision_passport` | جواز قرار بسلسلة أدلة قابلة للتدقيق | `action`, `evidence_refs` | لا أدلة → BLOCK؛ مخاطر L3+ → REQUIRE_APPROVAL |
| 5 | `compliance_reasoning` | استدلال PDPL/ZATCA/SAMA/NCA | `data_classification`, `processing_region` | منطقة غير SA → BLOCK؛ PII بلا lawful_basis → BLOCK |
| 6 | `proof_curation` | اختيار أفضل proof artifacts من المتوفر | `artifacts[]` (مع source_ref) | لا artifacts بمصدر → BLOCK |
| 7 | `customer_health` | درجة صحة عميل (adoption + usage + friction + tier) | إشارات مَلحوظة | لا اختراع إشارات؛ غياب الإشارة يخفض الثقة |
| 8 | `growth_signals` | ترتيب إشارات النمو (founder-supplied فقط) | `signals[]` | أنواع مسموحة فقط (warm_intro, referral, …)؛ الباقي ⇒ rejected |
| 9 | `executive_intelligence` | ملخَّص تنفيذي مركَّب من باقي الطبقات | مخرجات الطبقات | لا اختراع أرقام |

## 2) قواعد ثابتة على كل الطبقات

1. **كل output يحمل `governance_decision`** — إحدى السبع (`ALLOW`, `ALLOW_WITH_REVIEW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `ESCALATE`).
2. **No scraping.** أي طبقة تتطلب `source_refs` ترفض الاستدعاء بدونها.
3. **No PII in output.** `content_generation` تمر بـ regex redaction قبل العودة.
4. **No guaranteed claims.** AR + EN regex (`نضمن`, `guaranteed sales`) تفرض REDACT.
5. **No external action without approval.** `external_action_requested=True` يرفع القرار إلى REQUIRE_APPROVAL.
6. **No source-less knowledge.** `proof_curation` ترفض artifact بلا `source_ref`.

## 3) Pipeline aggregation rule

`run_pipeline(ctx)` تستخدم **strictness ladder**:

```
ALLOW (0) < ALLOW_WITH_REVIEW (1) < DRAFT_ONLY (2) < REQUIRE_APPROVAL (3)
       < REDACT (4) < BLOCK (5) < ESCALATE (6)
```

`overall_decision` = أعلى رتبة شوهدت بين الطبقات. إذا أي طبقة BLOCK → الـ pipeline BLOCK، لكن باقي النتائج تبقى متاحة للقراءة (نظراً لأن الأمر تشخيصي).

## 4) Capital Asset emission

- `account_scoring` ينتج `scoring_rule` عند tier ∈ {A, B}.
- `content_generation` ينتج `draft_template` عندما لا يُحظَر.
- `compliance_reasoning` ينتج `governance_rule` عند ALLOW.
- `proof_curation` ينتج `proof_example`.
- `growth_signals` ينتج `productization_signal` عند وجود قبول.

كل asset مرشَّح فقط — مهمة `capital_os.add_asset(...)` تبقى بيد المنسِّق.

## 5) أمثلة استدعاء (cURL)

### تشغيل طبقة واحدة

```bash
curl -X POST http://localhost:8000/api/v1/ai-layers/lead_scoring/run \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "acme_co",
    "payload": {"title_founder_exec": true, "b2b_company": true, "crm_or_pipeline": true, "uses_or_plans_ai": true, "saudi_or_gcc": true},
    "source_refs": ["founder://warm_list/2026-05-24/001"]
  }'
```

### تشغيل الـ pipeline الكامل

```bash
curl -X POST http://localhost:8000/api/v1/ai-layers/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "acme_co",
    "payload": {
      "action": "send_diagnostic_email",
      "evidence_refs": ["proof://pack/PP-001"],
      "data_classification": "internal",
      "processing_region": "sa",
      "contains_pii": false,
      "topic": "Revenue Intelligence Sprint",
      "account_name": "Acme",
      "icp_signals": {"saudi_b2b": true, "uses_crm": true},
      "readiness_signals": {"data_available": true, "owner_present": true},
      "sector": "saas",
      "stage": "diagnosis",
      "artifacts": [
        {"id": "PE-1", "type": "proof_example", "tier": "verified", "source_ref": "proof://1", "summary": "case-safe pattern"}
      ],
      "signals": [
        {"kind": "warm_intro", "timestamp": "2026-05-22T10:00:00Z", "account_hint": "Acme", "source_ref": "intro://founder/2026-05-22"}
      ]
    },
    "source_refs": ["founder://warm_list/001"],
    "external_action_requested": false
  }'
```

### الاستجابة المتوقَّعة

```json
{
  "result": {
    "customer_id": "acme_co",
    "layers_run": ["lead_scoring", "account_scoring", "...", "executive_intelligence"],
    "results": { "...": "..." },
    "overall_decision": "ALLOW",
    "blocked_layers": []
  },
  "hard_gates": {
    "no_live_send": true,
    "no_external_action_without_approval": true,
    "no_pii_in_logs": true,
    "no_scraping": true,
    "no_guaranteed_claims": true,
    "every_output_has_governance_decision": true
  }
}
```

## 6) ملاحظات للمطوِّرين

- لا تستدعي layer مباشرة — اِستخدم `run_layer(name, ctx)` أو `run_pipeline(ctx)` من `auto_client_acquisition.ai_layers`.
- لا تُعدِّل `_STRICTNESS` بدون RFC في `docs/transformation/rfcs/`.
- إضافة طبقة جديدة: ملف Python جديد + entry في `_REGISTRY` + entry في `AI_LAYERS` + ≥ 2 tests + entry في هذه البطاقة.
- لا تُسجِّل PII في الـ logs — استخدم `friction_log.sanitize_notes(notes)` إذا لزم.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
