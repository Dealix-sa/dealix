# Dealix — بطاقة جاهزية التدشين · Launch Readiness Scorecard

**الحالة / Status:** DRAFT — go/no-go gate
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `MASTER_LAUNCH_OS.md` · `FIRST_PILOT_PLAYBOOK.md` · `../../DEALIX_READINESS.md` · `../readiness/`

> هذه البطاقة هي بوابة go/no-go للتدشين. **لا أرقام مفبركة** — كل بند إمّا مقيس فعلياً، أو
> موسوم صراحةً بأنه يحتاج تقييم المؤسس أو تشغيل في بيئة CI كاملة (`no_fake_proof`).
>
> This scorecard is the launch go/no-go gate. **No fabricated scores** — every line is
> either really measured, or explicitly marked as needing founder assessment or a full CI run.

---

## 1. صحة المنصة الحية · Live platform health — ✅ MEASURED

تشغيل `python scripts/dealix_smoke_test.py` مقابل `https://api.dealix.me` بتاريخ
**2026-05-18T14:22 UTC**:

| المقياس / Metric | النتيجة / Result |
|---|---|
| فحوصات نقاط النهاية / Endpoint checks | **28 / 28 passed** |
| فحوصات مطلوبة فاشلة / Required checks failed | **0** |
| الحكم / Verdict | ✅ all required checks passed |
| نقاط حرجة شملها الفحص | `/health` · `founder/dashboard` · `delivery-factory/status` · `finance/pricing` · `proof-ledger/status` · `agent-governance/status` · `reliability/health-matrix` |

المنصة حية وسليمة. The platform is live and healthy.

---

## 2. جاهزية تسليم Tier 0–1 · Tier 0–1 delivery readiness — ✅ CODE COMPLETE

استكشاف مسار التسليم end-to-end أكّد عدم وجود stubs أو TODOs في المسار الحرج:

| الخطوة / Step | الحالة | المرجع البرمجي |
|---|---|---|
| Intake (التشخيص المجاني) | ✅ | `api/routers/diagnostic.py` |
| Qualification & scoring | ✅ | `auto_client_acquisition/sales_os/` · `icp_scorer.py` |
| Invoice intent | ✅ | `payment_ops/orchestrator.py::create_invoice_intent` |
| Payment confirmation (founder-initiated) | ✅ | `payment_ops/orchestrator.py::confirm_payment` |
| Delivery kickoff | ✅ | `payment_ops/orchestrator.py::kickoff_delivery` |
| 7-day sprint (8 خطوات) | ✅ | `delivery_factory/delivery_sprint.py::run_sprint` |
| Proof Pack (14 قسماً) | ✅ | `proof_os/` · `delivery_sprint.py::step6_proof_pack` |

التفصيل الكامل في `FIRST_PILOT_PLAYBOOK.md`.

---

## 3. بوابات الجاهزية · Readiness Gates 0–10 — ⚠️ FOUNDER ASSESSMENT REQUIRED

البوابات مُعرّفة في `../../DEALIX_READINESS.md` و`../readiness/`. الدرجات الفعلية **غير
مسجّلة** في الريبو — لا تُملأ بأرقام مُختلَقة. القرار لكل بوابة يحتاج تقييم المؤسس + تشغيل
`python scripts/verify_dealix_ready.py` في بيئة CI/Railway كاملة.

| Gate | الاسم | عتبة العبور | القرار |
|---|---|---|---|
| 0 | Founder Clarity | ≥ 85 | _قيد تقييم المؤسس_ |
| 1 | Offer Readiness | ≥ 85 لكل عرض | _قيد التقييم_ |
| 2 | Delivery Readiness | ≥ 85 | _الكود مكتمل (§2)؛ الدرجة قيد التقييم_ |
| 3 | Product Readiness | ≥ 80 MVP | _المنصة حية (§1)؛ الدرجة قيد التقييم_ |
| 4 | Governance Readiness | ≥ 90 | _قيد التقييم_ |
| 5 | Demo Readiness | ≥ 85 | _قيد التقييم_ |
| 6 | Sales Readiness | ≥ 85 | _قيد التقييم_ |
| 7 | Client Delivery Readiness | — | _قيد التقييم_ |
| 8 | Retainer Readiness | ≥ 85 | _غير مطلوب للتدشين — بعد أول pilot_ |
| 9 | Scale Readiness | ≥ 85 | _غير مطلوب للتدشين_ |
| 10 | World-Class Readiness | معيار طموح | _غير مطلوب للتدشين_ |

> **إجراء مطلوب:** شغّل `python scripts/verify_dealix_ready.py` في CI أو على Railway،
> وسجّل المخرجات هنا وفي `DEALIX_READINESS.md`. تعذّر تشغيله في بيئة الإعداد المؤقتة هذه
> (فشل بناء عجلة `ummalqura` — يحتاج سلسلة أدوات بناء كاملة). The verify script must be run
> in a full CI/Railway environment; it could not run in this ephemeral sandbox.

---

## 4. الـ11 non-negotiables · enforced by guard tests — ✅ ENFORCED IN CODE

| القاعدة | اختبار الحراسة |
|---|---|
| no_live_send | `tests/test_no_live_send.py` |
| no_live_charge | `tests/test_no_live_charge.py` · gate `_enforce_no_live_charge` في `payment_ops/orchestrator.py` |
| no_cold_whatsapp | `tests/test_no_cold_whatsapp.py` |
| no_scraping | `tests/test_no_scraping*.py` |
| no_fake_proof | `tests/test_*no_fake_proof.py` |
| no_unconsented_data | `tests/test_no_unconsented_data.py` |
| no_unverified_outcomes | `tests/test_no_guaranteed_claims.py` |
| no_hidden_pricing | `tests/test_no_hidden_pricing.py` |
| no_silent_failures | `tests/test_no_silent_failures.py` |
| no_unbounded_agents | `tests/governance/test_agent_boundaries.py` |
| no_unaudited_changes | `tests/governance/test_audit_chain.py` |

> **إجراء مطلوب:** شغّل `pytest -k "no_live or no_cold or no_scraping or no_fake or no_hidden"`
> في CI وسجّل النتيجة. The full suite (3,881 tests) runs in CI.

---

## 5. معرقلات التدشين · Launch blockers

| # | المعرقل | المالك | الحالة |
|---|---|---|---|
| 1 | تفعيل حساب Moyasar (سكة الدفع) | المؤسس | مفتوح — انظر `MOYASAR_ACTIVATION_RUNBOOK.md`. تحصيل التحويل البنكي/النقد متاح الآن. |
| 2 | مصالحة الرواية في الأصول Tier 1 | محتوى | جزئي — `launch_content_queue.md` تمت مصالحته؛ الباقي في backlog `CANONICAL_NARRATIVE_AND_PRICE.md`. |
| 3 | تشغيل `verify_dealix_ready.py` + guard tests في CI وتسجيل النتائج | هندسة/CI | مفتوح |

---

## 6. معايير Go / No-Go · Go/No-Go criteria

**GO للتدشين عندما:**

- [x] المنصة الحية: smoke test 28/28 ✅
- [x] كود تسليم Tier 0–1 مكتمل بلا stubs ✅
- [x] الرواية والسعر الرسميان موثّقان (`CANONICAL_NARRATIVE_AND_PRICE.md`) ✅
- [ ] سكة الدفع جاهزة: Moyasar مُفعّل **أو** التحويل البنكي مؤكّد كمسار أول pilot
- [ ] أصول Tier 1 المواجهة للعميل خالية من رواية «45 ثانية / 1 ريال»
- [ ] `verify_dealix_ready.py` + guard tests خضراء في CI ومسجّلة هنا
- [ ] dry-run تسليم Tier 0–1 ناجح (`FIRST_PILOT_PLAYBOOK.md`)

**NO-GO إذا:** أي اختبار non-negotiable أحمر · أي ادعاء نتيجة مضمونة في أصل مواجه للعميل ·
سعر غير متطابق مع `../COMMERCIAL_WIRING_MAP.md`.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
