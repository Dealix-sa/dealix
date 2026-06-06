# خطة التفعيل التجاري — 90 يوماً / 90-Day Commercial Activation Plan

**الغرض:** خطة تنفيذ موحّدة لثلاث مراحل (0–30 / 31–60 / 61–90) تربط العرض المناسب من كتالوج التسعير الداخلي بمقياس North Star والعقيدة الحاكمة لكل مرحلة. لا تكرّر الوثائق الطويلة — تلخّص وتربط.

**Purpose:** A consolidated three-phase execution plan (Days 0–30 / 31–60 / 61–90) linking the right offer from the internal pricing catalog to a North Star metric and the gating doctrine for each phase. It summarizes and links; it does not duplicate.

> مصدر الحقيقة للسعر والنطاق: [`auto_client_acquisition/finance_os/pricing_catalog.py`](../../auto_client_acquisition/finance_os/pricing_catalog.py). للأسعار التجارية الموسّعة: [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md).

---

## المراجع المُجمَّعة / Consolidated References

هذه الخطة تُجمّع وتُلخّص الوثائق التالية — افتح الأصل للتفصيل، ولا تنسخه هنا:

- [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) — نقطة الدخول اليومية (5 دقائق)، المراحل 0–5، SOAEN، Motions.
- [LAUNCH_EXECUTION_NOW_AR.md](LAUNCH_EXECUTION_NOW_AR.md) — ربط الاستراتيجية باليوم الواحد، سلم البيع، الحوكمة.
- [COMMERCIAL_LAUNCH_CHECKLIST_AR.md](COMMERCIAL_LAUNCH_CHECKLIST_AR.md) — بوابة جاهزية Soft Launch.
- [PAID_LAUNCH_AFTER_SOFT_PASS_AR.md](PAID_LAUNCH_AFTER_SOFT_PASS_AR.md) — مسار الإطلاق المدفوع بعد نجاح Soft.
- [NORTH_STAR_METRICS_AR.md](NORTH_STAR_METRICS_AR.md) — جدول المقاييس الداخلية (ليست وعوداً للعميل).
- العروض: [offers/P1_REVENUE_INTELLIGENCE_SPRINT_AR.md](offers/P1_REVENUE_INTELLIGENCE_SPRINT_AR.md) · [offers/P2_AI_SALES_OPS_ASSISTANT_AR.md](offers/P2_AI_SALES_OPS_ASSISTANT_AR.md) · [offers/P3_EXECUTIVE_COMMAND_CENTER_AR.md](offers/P3_EXECUTIVE_COMMAND_CENTER_AR.md).

This plan consolidates and summarizes the documents above. Open each original for detail; do not copy it here.

---

## العقيدة الحاكمة لكل المراحل / Doctrine Across All Phases

هذه القواعد غير قابلة للمساومة وتسري على المراحل الثلاث:

- **لا إرسال آلي** — كل رسالة تبقى مسوّدة (Draft Pack) حتى موافقة العميل الصريحة. لا واتساب بارد، لا أتمتة LinkedIn.
- **لا ضمان ROI بدون baseline موثّق** — النتائج تُؤطَّر كفرص مُثبتة بأدلة، لا أرقام مبيعات.
- **كل رسالة خارجية تحتاج موافقة** قبل الإرسال (SOAEN: Source → Owner → Approval → Evidence → Next Action).
- **كل دليل مربوط بالسجل (ledger-backed)** — لا ادعاء بلا مصدر، ولا scraping إنتاجي أو قوائم مشتراة.
- **لا عروض حصرية (exclusivity) قبل 3 إثباتات** — مطابقة لقيد `exclusivity_offers_until_3_proofs` في `pricing_catalog.py` (باقة نمو الشراكات). الحصرية تأتي بعد تراكم الأدلة، لا قبلها.

These rules are non-negotiable and apply to all three phases: no auto-send (every message is a draft until explicit approval), no ROI guarantee without a documented baseline, every external message requires approval, all proof is ledger-backed, and no exclusivity offers until 3 proofs accumulate.

---

## المرحلة 1 — الأيام 0–30: التمرير الناعم (Soft Pass) / Phase 1 — Days 0–30: Soft Pass

**الأهداف / Objectives:**
- تشغيل صفحة بيع عامة + funnel + آلة يومية موحّدة دون ادعاء إطلاق مدفوعات live.
- إجراء 3–5 جلسات **Diagnostic مجانية** حقيقية واستخلاص أول إثباتات.
- بيع أول **Growth Starter Pilots** بعد التشخيص.

**العرض في اللعب / Offer in Play** (من `pricing_catalog.py`):
- **Diagnostic مجاني / Free Growth Diagnostic** — 0 ريال — جلسة 30–60 دقيقة + 3 توصيات + توصية أفضل عرض أول. مسار الترقية: `growth_starter_pilot_499_sar`.
- **باقة بداية النمو — Pilot / Growth Starter Pilot** — 499 ريال (دفعة واحدة) — 7 أيام: 10 فرص مؤهّلة، مسوّدات عربية، خطة متابعة 72 ساعة، Proof Pack موقَّع. مسار الترقية: `executive_growth_os`.

**هدف North Star / North Star Target:**
- **Pilots النشطة + Proof Packs مسلّمة هذا الأسبوع** (المؤشر الأسبوعي الواحد قبل التوسّع — من MASTER_COMMERCIAL_OPERATING_PLAN). الهدف المرحلي: أول `payment_received` + أول `proof_pack_delivered`.

**العقيدة الحاكمة / Gating Doctrine:**
- لا انتقال للإطلاق المدفوع قبل `DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS` و3–5 اجتماعات تشخيص حقيقية.
- Soft Launch **لا يفعّل** أي إرسال بارد. كل مخرج Diagnostic = توصيات ومسودات بموافقة فقط.

Phase 1 runs the public sales page, funnel, and daily machine; delivers 3–5 real free diagnostics; and sells the first Growth Starter Pilots. North Star: active Pilots + Proof Packs delivered this week, with the milestone of the first `payment_received` + `proof_pack_delivered`. Gate: no paid launch before the Soft PASS verdict and 3–5 real diagnostic meetings.

---

## المرحلة 2 — الأيام 31–60: Sprints مدفوعة + تراكم الأدلة / Phase 2 — Days 31–60: Paid Sprints + Proof Accumulation

**الأهداف / Objectives:**
- تحويل التشخيص إلى **Sprints** مدفوعة وتراكم Proof Packs قابلة للتدقيق.
- تنظيف بيانات العميل وترتيب الفرص عبر **من البيانات إلى الإيراد** حيث تكون القائمة هي العائق.
- بناء طبقة الأدلة التي تُمكّن قرار التجديد في المرحلة 3.

**العرض في اللعب / Offer in Play** (من `pricing_catalog.py`):
- **من البيانات إلى الإيراد / Data to Revenue** — 1,500 ريال (مشروع) — تنظيف وإزالة تكرار القائمة، درجة قابلية تواصل، مسوّدات مقسّمة، تقرير مخاطر. مسار الترقية: `executive_growth_os`.
- **باقة بداية النمو — Pilot** (مكرّرة) لمن لم يبدأ بعد، كمدخل مدفوع قصير قبل التشغيل الشهري.
- مرجع موسّع للـ Sprint المدفوع: [offers/P1_REVENUE_INTELLIGENCE_SPRINT_AR.md](offers/P1_REVENUE_INTELLIGENCE_SPRINT_AR.md).

**هدف North Star / North Star Target:**
- **تحسّن جودة الجدول** (`mean_completeness` قبل/بعد) و**تغطية المصدر** (نسبة الإجابات مع `source_id` = 100% للمعلن) — من NORTH_STAR_METRICS. مؤشر تجاري مرافق: عدد Proof Packs المسلّمة المتراكمة.

**العقيدة الحاكمة / Gating Doctrine:**
- لا تحويل إيرادي رقمي موعود في أي Sprint إلا إذا وُثّق baseline في SOW منفصل.
- لا قوائم مشتراة (`purchased_lead_lists`) ولا إرسال فعلي لطرف ثالث (`live_external_send`).
- التجديد لا يُناقَش قبل تسليم إثبات موثّق.

Phase 2 converts diagnostics into paid Sprints and accumulates auditable Proof Packs, using Data to Revenue where the list is the bottleneck. North Star: table-quality improvement and 100% source coverage, with cumulative Proof Packs as the commercial companion metric. Gate: no promised numeric revenue conversion without a documented baseline in a separate SOW; no purchased lists, no live external send.

---

## المرحلة 3 — الأيام 61–90: تحويل Executive Growth OS المتكرّر / Phase 3 — Days 61–90: Executive Growth OS Recurring Conversion

**الأهداف / Objectives:**
- تحويل عملاء الـ Sprint إلى تشغيل شهري متكرّر تحت **نظام تشغيل القيادة التنفيذية**.
- بناء غرفة الإثبات والتقرير التنفيذي للعميل كأساس لقرار التجديد (Client Portal OS).
- فتح مسار الشراكات فقط بعد تراكم 3 إثباتات.

**العرض في اللعب / Offer in Play** (من `pricing_catalog.py`):
- **نظام تشغيل القيادة التنفيذية / Executive Growth OS** — 2,999 ريال/شهر (متكرّر) — موجز تنفيذي أسبوعي، Proof Pack شهري، ساعة مكتب أسبوعية، كل مزايا الباقات الأدنى. مسار الترقية: `full_control_tower_custom`.
- **نمو الشراكات / Partnership Growth** — يبدأ من 3,000 ريال (مشروع؛ المدى الموثّق 3,000–7,500) — رادار 8 فئات شركاء، fit-score، مسوّدات تواصل دافئة، Proof Pack مشترك. مسار الترقية: `full_control_tower_custom`. **يُفتح فقط بعد 3 إثباتات.**
- مراجع موسّعة للتشغيل الشهري والغرفة التنفيذية: [offers/P2_AI_SALES_OPS_ASSISTANT_AR.md](offers/P2_AI_SALES_OPS_ASSISTANT_AR.md) · [offers/P3_EXECUTIVE_COMMAND_CENTER_AR.md](offers/P3_EXECUTIVE_COMMAND_CENTER_AR.md).

**هدف North Star / North Star Target:**
- **تحويل Sprint → Retainer** (نسبة من أكملوا Sprint ووقّعوا ريتينر خلال 90 يوماً) و**موافقات مسجّلة** (100% من انتقالات active لها `approval_id`) و**حوادث PII = 0** — من NORTH_STAR_METRICS.

**العقيدة الحاكمة / Gating Doctrine:**
- **لا عروض حصرية قبل 3 إثباتات** (`exclusivity_offers_until_3_proofs`) — الشراكات والحصرية بعد الأدلة لا قبلها.
- `executive_growth_os` يستثني `guaranteed_revenue_promises` و`live_external_charge` صراحةً — التجديد يُبنى على Proof Pack موثّق، لا على وعد عائد.

Phase 3 converts Sprint clients to recurring monthly operations under Executive Growth OS, builds the Proof Room and executive client report as the renewal basis, and opens the partnerships path only after 3 proofs. North Star: Sprint-to-retainer conversion, 100% recorded approvals, and zero PII incidents. Gate: no exclusivity offers before 3 proofs; renewal is built on a documented Proof Pack, not a revenue promise.

---

## ملخّص مسار العرض / Offer Path Summary

```text
Diagnostic (0) → Growth Starter Pilot (499) → Data to Revenue (1,500)
  → Executive Growth OS (2,999/mo) → Partnership Growth (3,000+, بعد 3 إثباتات)
```

الأرقام أعلاه من `pricing_catalog.py` حصراً. الأسعار التجارية الموسّعة (Diagnostic 3,500 / Sprint 9,500 / Pilot 22,000 / RevOps OS / Enterprise) موثّقة في [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) ولا تُخلَط بأرقام الكتالوج.

The figures above are strictly from `pricing_catalog.py`. The extended commercial pricing is documented separately in the RevOps packages doc and must not be mixed with catalog numbers.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
