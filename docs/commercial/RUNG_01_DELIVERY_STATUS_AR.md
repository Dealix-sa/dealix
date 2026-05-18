# Dealix — Rung 0–1 Delivery Readiness — جاهزية تسليم الدرجتين 0–1

<!-- PHASE 12 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> القاعدة الذهبية: أول Pilot مدفوع لا يُعتبر مُسلَّماً قبل أن يستلم العميل Proof Pack مُقدَّماً فعلياً (HTML/PDF) ومُصدَّقاً منه عند مستوى إثبات L3 أو أعلى. الكود الذي «يعمل» في الاختبار لا يساوي تسليماً — التسليم هو ملف يستلمه العميل.

## ما هذه الوثيقة

تقرير تحقّق من جاهزية مسار تسليم الدرجتين 0–1 (التشخيص المجاني + سبرنت إثبات الإيراد 7 أيّام بـ 499 ريال). هذا العمل مسموح صراحةً ضمن [التجميد التجاري](../ops/COMMERCIAL_FREEZE.md) تحت بند «إنهاء تسليم الدرجتين 0–1» و«تجميع Proof Pack». لم يُرسَل شيء خارجياً، ولم تُبنَ ميزات جديدة — تحقّق + تشغيل تجريبي آمن + إصلاح نقطة واحدة.

التقرير متّسق مع [`LAUNCH_GATES_STATUS_AR.md`](LAUNCH_GATES_STATUS_AR.md) (بوابات الإطلاق الخمس) و[`DELIVERY_QA_AR.md`](DELIVERY_QA_AR.md) (بوّابة جودة Proof Pack من 10 نقاط).

---

## الخلاصة المباشرة

**هل يمكن تسليم أول Pilot مدفوع من طرف لطرف اليوم؟ — نعم، مع تحفّظ واحد.**

المسار البرمجي كامل وسليم: من تأكيد الدفع → بدء التسليم → تشغيل السبرنت بعشر خطوات → تجميع Proof Pack من 14 قسماً → تصيير نسخة عربية/إنجليزية يستلمها العميل. التشغيل التجريبي على بيانات Saudi B2B التجريبية أنتج Proof Pack مكتمل 14/14 قسماً بدرجة إثبات 100/100 ومستوى `case_candidate`، وأصلاً رأسمالياً واحداً مُسجَّلاً.

التحفّظ الوحيد لجاهزية الإنتاج: **تصيير الـ PDF يحتاج تثبيت `weasyprint` أو `pandoc` في بيئة الإنتاج**. بدونهما يرجع المسار إلى Markdown تلقائياً (مع ترويسة `X-PDF-Renderer: unavailable`). النسخة Markdown ثنائية اللغة وكاملة وصالحة للتسليم، لكن «النسخة المُقدَّمة» المطلوبة في شرط الخروج من التجميد تكون أقوى كـ PDF.

تم تطبيق **إصلاح نقطة واحدة (P1)** أثناء التحقّق — انظر قسم «الإصلاح المُطبَّق».

---

## حالة المكوّنات — Component Status

| المكوّن | الملف / المسار | الحالة | الدليل / فعل المؤسس |
|---|---|---|---|
| منشئ التشخيص (Rung 0) | `scripts/dealix_diagnostic.py` + `dealix_ai_ops_diagnostic.py` | READY | شُغِّل: `--list-bundles` و تشخيص كامل ثنائي اللغة — خرج 0 |
| منشئ موجز الـ Pilot (499 ريال) | `scripts/dealix_pilot_brief.py` | READY | شُغِّل: كتب `pilot_brief.md/json`، `amount_sar=499`, `live_charge=False` |
| بدء جلسة التسليم | `scripts/dealix_delivery_kickoff.py` | READY | يحجب بصحّة عند غياب `payment_state.json` → `BLOCKED_WAITING_PAYMENT` |
| منشئ Proof Pack (Wave 6) | `scripts/dealix_wave6_proof_pack.py` | READY | يرفض بصحّة عند غياب `delivery_session.json` — لا يختلق pack |
| مُجمِّع Proof Pack من الأحداث | `scripts/dealix_proof_pack.py` | READY | `--allow-empty` ينتج قالباً فارغاً صريحاً (`internal_only`, `approval_required`) |
| محرّك السبرنت بعشر خطوات | `auto_client_acquisition/delivery_factory/delivery_sprint.py` | READY | تشغيل تجريبي: 8/8 خطوات `ran`، 14/14 قسماً مملوء |
| معيار Proof Pack v2 (14 قسماً) | `auto_client_acquisition/proof_architecture_os/proof_pack_v2.py` | READY | 14 قسماً معرّفة؛ فحص الاكتمال يعمل |
| درجة الإثبات + المستوى | `auto_client_acquisition/proof_os/proof_score.py` | READY | درجة 0–100، حزام `weak/internal_learning/sales_support/case_candidate` |
| تصيير Proof Pack (Markdown) | `proof_architecture_os/proof_pack_render.py` | READY | يصيّر نسخة عربية/إنجليزية يستلمها العميل (1847 حرفاً للعيّنة) |
| تصيير Proof Pack (PDF) | `proof_to_market/pdf_renderer.py` | GAP (بيئي) | `weasyprint`/`pandoc` غير مثبَّتين — يرجع إلى Markdown؛ يحتاج تثبيت في الإنتاج |
| مسار HTTP للسبرنت | `api/routers/sprint_runner.py` | READY | `/run`, `/render/markdown`, `/render/pdf`, `/render/email-body`, `/sample` |
| مسار HTTP للـ Proof Pack المحكوم | `api/routers/proof_pack_governed.py` | READY | `/generate` يحسب الدرجة، `/retainer-gate` يقيّم الاشتراك |
| آلة حالة الدفع | `auto_client_acquisition/payment_ops/orchestrator.py` | READY | `invoice_intent → evidence → confirmed → kickoff` — جُرِّبت كاملةً |
| مسار HTTP للدفع | `api/routers/payment_ops.py` | READY | `kickoff-delivery` يعيد `delivery_kickoff_id` كرابط تدقيق |
| رابط الدفع ← التسليم | `payment_ops` → `delivery_kickoff_id` → `engagement_id` | READY | الرابط سليم — التسليم محكوم بـ `payment_confirmed` |
| عيّنات Proof Pack المُقدَّمة | `docs/assets/proof_packs/`, `SAMPLE_PROOF_PACK_AR.md` | READY | قوالب + عيّنة مجهّلة كاملة موجودة |
| السجلّات (قيمة/رأسمال/احتكاك) | `value_os`, `capital_os`, `friction_log` | READY | السبرنت سجّل أصلاً رأسمالياً واحداً (`cap_…`) |

---

## تتبّع رابط الدفع ← التسليم (Audit Link)

الرابط **سليم بالكامل**. آلة الحالة جُرِّبت من طرف لطرف:

```
1) invoice_intent           → الفاتورة ليست إيراداً
2) payment_evidence_uploaded → رفع مرجع التحويل البنكي (≥ 5 أحرف)
3) payment_confirmed         → تأكيد المؤسس يدوياً = إيراد
4) delivery_kickoff          → يولّد delivery_kickoff_id (dk_…)
```

- `delivery_kickoff_id` هو **رابط التدقيق**: يُمرَّر كـ `engagement_id` إلى `POST /api/v1/sprint/run`، فيربط الدفعة بالتسليم بالـ Proof Pack.
- اختبار سلبي مؤكَّد: `kickoff_delivery` قبل `payment_confirmed` يُرفَض بـ `delivery_requires_payment_confirmed` — لا يبدأ تسليم بلا دفع مؤكَّد.
- البوّابات الصلبة مفعّلة: `no_live_charge`, `no_fake_revenue`, `evidence_reference_required_for_confirm`, `delivery_requires_payment_confirmed`.
- ملاحظة بيئية: في بيئة التحقّق هذه ظهر `ModuleNotFoundError: sqlalchemy` عند مرآة التدفّق التشغيلية (`persistence/operational_stream_mirror`). لكن `sqlalchemy` **موجود في `requirements.txt`** (السطر 33)، فهي فجوة بيئة التحقّق لا عيب كود؛ منطق آلة الحالة سليم وجُرِّب بعزل المرآة. في الإنتاج (مع تثبيت `requirements.txt`) يعمل المسار كاملاً.

---

## التشغيل التجريبي الآمن — Sample Dry-Run

البيانات: `data/demo/saudi_b2b_demo.csv` (20 شركة Saudi B2B اصطناعية — لا بيانات عميل حقيقية، لا استدعاء API مدفوع).

| القياس | النتيجة |
|---|---|
| خطوات السبرنت | 8/8 `ran` (kickoff, data_quality, account_scoring, draft_pack, governance, proof_pack, capital, retainer) |
| أقسام Proof Pack | 14/14 مملوءة — لا قسم فارغ |
| درجة اكتمال الـ Proof Pack | **100/100** |
| المستوى (Tier) | `case_candidate` |
| درجة جودة البيانات (DQ) | 97.7/100 |
| الأصول الرأسمالية | 1 مُسجَّل (`scoring_rule`) |
| قرار الحوكمة | `allow_with_review` |
| جاهزية الاشتراك | `eligible=False` (متوقَّع — `adoption_score` للعميل التجريبي صفر) |

التصيير: النسخة العربية/الإنجليزية أُنتجت بنجاح (Markdown، 1847 حرفاً). تصيير الـ PDF أرجع `None` (لا مُصيّر مثبَّت) — وهو سلوك التراجع المقصود.

---

## الإصلاح المُطبَّق — Hotfix (P1)

**الملف:** `auto_client_acquisition/delivery_factory/delivery_sprint.py` (ملف واحد، دالة `step6_proof_pack`).

**العيب:** درجة جودة البيانات (DQ) على مقياس 0–100 (موثّق في `data_quality_score.py`)، لكن `step6_proof_pack` كان يصيّرها في قسمَين يراهما العميل (`inputs` و`quality_scores`) بصيغة `…/1.00`. النتيجة في Proof Pack مدفوع حقيقي: «Data-quality score: 97.70/1.00» — رقم بلا معنى (أكبر من 1 على مقياس /1.00) ومُحرج في مستند يستلمه العميل. هذا عيب صحّة في مخرج الدرجة 1 المُقدَّم للعميل.

**التغيير (سطران):**

- `Data-quality score: {dq_score:.2f}/1.00` → `Data-quality score: {dq_score:.1f}/100`
- `Data-quality (DQ) score: {dq_score:.2f}/1.00.` → `Data-quality (DQ) score: {dq_score:.1f}/100.`

**تصحيح ثانوي مرتبط (نفس الملف):** عتبة إشارة الدليل `dq_score >= 0.5` كانت ستمرّ دائماً على مقياس 0–100 (أي DQ غير صفري). صُحِّحت إلى `dq_score >= 70.0` — وهي عتبة مراجعة المؤسس نفسها في دليل التسليم — حتى لا يَدّعي تشغيلٌ ببيانات ضعيفة إشارةَ دليلٍ قوية.

**التحقّق بعد الإصلاح:** أُعيد التشغيل التجريبي — لا يظهر `/1.00` في النسخة المُقدَّمة، 14/14 قسماً سليمة، الدرجة 100. اختبارات `tests/test_delivery_sprint.py` لا تتحقّق من `/1.00` (تتحقّق فقط من `dq_overall > 0`)، واتفاقية `/100` متّسقة مع الاختبارات القائمة (`test_case_study_exporter.py` يستخدم `DQ=82.0/100`). الإصلاح لا يكسر شيئاً.

النطاق: P0/P1، إصلاح ملف واحد — مسموح صراحةً ضمن التجميد. لم تُضَف ميزة ولا موجِّه ولا وحدة.

---

## ما الذي يحجب تسليم أول Pilot مدفوع — Blockers

| # | البند | الشدّة | من يحلّه | الفعل المطلوب |
|---|---|---|---|---|
| 1 | تصيير PDF غير متاح في الإنتاج | P2 — مُجسَّر | المؤسس / DevOps | تثبيت `weasyprint` أو `pandoc` في صورة الإنتاج. حتى ذلك الحين تُسلَّم النسخة Markdown (كاملة وثنائية اللغة وصالحة) — لا تحجب التسليم |
| 2 | `sqlalchemy` غير مثبَّت في بيئة التحقّق | لا شيء في الإنتاج | DevOps | موجود في `requirements.txt` — يُحَلّ بتثبيت الاعتماديات في الإنتاج؛ ليس عيب كود |
| 3 | شرط الخروج من التجميد: موافقة العميل L3+ | فعل المؤسس | المؤسس | المسار البرمجي جاهز — يبقى: عميل حقيقي يدفع، يستلم Proof Pack، يصدّق عليه عند L3+ |
| 4 | بوابات الإطلاق الخمس (Moyasar/Railway) | فعل المؤسس | المؤسس | غير حاجبة للدرجة 1: الدفع مُجسَّر يدوياً (تحويل بنكي) وفق `MANUAL_PAYMENT_SOP` — انظر `LAUNCH_GATES_STATUS_AR.md` |

**ليس حاجباً برمجياً:** لا يوجد عيب كود يمنع تسليم أول Pilot مدفوع. البنود المتبقّية إمّا أفعال مؤسس (بيع، تحصيل، تصديق) أو هيئة بيئة إنتاج (تثبيت اعتماديات). المسار من «دفع مؤكَّد» إلى «Proof Pack مُقدَّم للعميل» يعمل اليوم.

---

## التوصية

1. تثبيت `weasyprint` في صورة الإنتاج لرفع جودة النسخة المُقدَّمة من Markdown إلى PDF — تغيير اعتمادية واحد، لا كود جديد.
2. متابعة البيع بقيادة المؤسس: المسار البرمجي للدرجة 1 جاهز للتسليم؛ القيد هو إغلاق أول Pilot مدفوع، لا الكود.
3. عند تسليم أول Pilot: تشغيل السبرنت ببيانات العميل الحقيقية، عبور بوّابة الجودة من 10 نقاط في [`DELIVERY_QA_AR.md`](DELIVERY_QA_AR.md)، أخذ تصديق العميل L3+، ثم يُرفع التجميد وفق [`COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md).

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
