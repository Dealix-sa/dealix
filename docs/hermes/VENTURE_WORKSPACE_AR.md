# Venture Workspace — استوديو القطاعات الجديدة

> المرجع: §35 من المواصفة الأصلية.

---

## ما هذه المساحة؟

Venture Workspace هي **مكان التجريب المُهيكل**: فحص قطاعات (verticals) جديدة قبل أن تُدمَج في Internal/Customer. الهدف: لا قطاع يدخل الإنتاج دون **فرضية**، **بيانات**، و**قرار Scale/Kill** صريح.

كل قطاع يُعامَل كـ "venture صغير": فرضية، اختبار، قياس، قرار. هذا يحمي Internal من ضوضاء التجارب ويحمي Sovereign من قرارات سريعة بلا أدلة.

---

## الـ 8 صفحات

| # | الصفحة | الغرض |
|---|---|---|
| 1 | **Vertical Cards** | بطاقات القطاعات المُقترَحة/قيد الاختبار/المعتمدة/المُغلَقة |
| 2 | **Hypotheses** | الفرضيات الجارية لكل قطاع (نص واضح + مقياس نجاح) |
| 3 | **Experiments** | التجارب الفعلية المرتبطة بفرضية (مدة، ميزانية، نتائج) |
| 4 | **Signals (vertical-tagged)** | الإشارات الواردة المُصنَّفة على هذا القطاع |
| 5 | **Pilots** | عملاء أو شركاء قبلوا الاختبار في هذا القطاع |
| 6 | **Evidence (venture)** | حِزَم أدلة خاصة بنتائج التجارب |
| 7 | **Scale/Kill Recommendations** | توصية للـ Sovereign بعد كل دورة (راجع [SCALE_KILL_PLAYBOOK_AR.md](SCALE_KILL_PLAYBOOK_AR.md)) |
| 8 | **Vertical Library** | أرشيف القطاعات المُغلَقة + الدروس المُستخلَصة |

---

## Vertical Card — schema

كل قطاع جديد يُمثَّل ببطاقة موحَّدة. شكل الـ schema:

```json
{
  "vertical_id": "string (snake_case)",
  "name_ar": "string",
  "name_en": "string",
  "status": "proposed | testing | scaling | killed",
  "owner": "string (internal team member)",
  "hypothesis": "string (one sentence)",
  "icp": {
    "size": "SMB | mid-market | enterprise",
    "geography": "saudi | gcc | other",
    "indicators": ["string"]
  },
  "value_proposition": "string",
  "primary_offer": "string (refers to PRODUCT_SURFACE)",
  "success_metric": {
    "name": "string",
    "target": "string",
    "evaluation_window_days": "integer"
  },
  "kill_metric": {
    "name": "string",
    "threshold": "string"
  },
  "budget_cap": "string (SAR range or TBD)",
  "active_experiments": ["experiment_id"],
  "pilots": ["pilot_id"],
  "evidence_refs": ["ev_pack_id"],
  "last_review_date": "ISO date",
  "next_review_date": "ISO date",
  "scale_kill_recommendation": "scale | hold | kill | none_yet"
}
```

---

## بطاقتان نموذجيتان

### Vertical Card 1 — Clinics

```json
{
  "vertical_id": "clinics_riyadh",
  "name_ar": "العيادات الخاصة — الرياض",
  "name_en": "Private Clinics — Riyadh",
  "status": "testing",
  "owner": "Internal Venture Lead",
  "hypothesis": "العيادات الخاصة متوسطة الحجم في الرياض تواجه فجوة في تأهيل الفرص الواردة من قنوات رقمية متعددة، ويمكن لـ Dealix تقديم Diagnostic ثم Sprint تأهيل فرص خلال 30 يومًا.",
  "icp": {
    "size": "SMB",
    "geography": "saudi",
    "indicators": [
      "2-8 أطباء",
      "حضور رقمي نشط (موقع + Google Business + إنستجرام)",
      "استخدام WhatsApp Business للحجوزات"
    ]
  },
  "value_proposition": "تحويل الفرص الواردة المُتفرّقة إلى pipeline موحَّد بأدلة، دون تجاوز PDPL.",
  "primary_offer": "Governed Revenue Diagnostic (راجع PRODUCT_SURFACE_AR.md)",
  "success_metric": {
    "name": "Time-to-Proof",
    "target": "Proof Pack مكتمل خلال 14 يومًا من بدء الـ Diagnostic",
    "evaluation_window_days": 60
  },
  "kill_metric": {
    "name": "Cycle abandonment rate",
    "threshold": "≥ 60% من العيادات تتوقف عن المتابعة بعد المكالمة الأولى"
  },
  "budget_cap": "TBD — نطاق سعري يُحدد عند الإطلاق",
  "active_experiments": ["exp_clinics_001"],
  "pilots": ["pilot_clinic_a", "pilot_clinic_b"],
  "evidence_refs": ["ev_pack_771", "ev_pack_780"],
  "last_review_date": "2026-05-10",
  "next_review_date": "2026-06-10",
  "scale_kill_recommendation": "none_yet"
}
```

### Vertical Card 2 — Real Estate Brokers

```json
{
  "vertical_id": "realestate_brokers_ksa",
  "name_ar": "وسطاء العقار — السعودية",
  "name_en": "Real Estate Brokers — KSA",
  "status": "proposed",
  "owner": "Internal Venture Lead",
  "hypothesis": "مكاتب الوساطة العقارية ذات الـ 5–20 وسيطًا تفقد فرصًا بسبب غياب تأهيل ICP موحَّد، ويمكن لـ Dealix بناء Lead Intelligence Sprint مع التزام PDPL وقنوات معتمدة فقط.",
  "icp": {
    "size": "SMB",
    "geography": "saudi",
    "indicators": [
      "5-20 وسيطًا",
      "ترخيص فال نشط",
      "حجم استفسارات شهري > حد أدنى يُحدَّد في الاختبار"
    ]
  },
  "value_proposition": "تأهيل واردات الإعلانات وتوحيدها في pipeline قابل للتدقيق، دون استخدام قنوات بارد غير معتمدة.",
  "primary_offer": "Revenue Intelligence Sprint",
  "success_metric": {
    "name": "Qualified-lead conversion lift",
    "target": "تحسّن مُقاس مقارنة بـ baseline قبل الـ Sprint، خلال 45 يومًا",
    "evaluation_window_days": 45
  },
  "kill_metric": {
    "name": "PDPL/channel friction",
    "threshold": "أي حالة طلب من العميل تخطي قناة معتمدة (cold WhatsApp/scraping)"
  },
  "budget_cap": "TBD — نطاق سعري يُحدد عند الإطلاق",
  "active_experiments": [],
  "pilots": [],
  "evidence_refs": [],
  "last_review_date": "2026-05-24",
  "next_review_date": "2026-06-24",
  "scale_kill_recommendation": "none_yet"
}
```

---

## كيف ينتقل قطاع من Venture إلى Internal؟

1. **testing → scaling** يتطلب: ≥ Proof Pack واحد مُثبت، KPI نجاح مُحقَّق، ≥ شريك أو عميل واحد راضٍ بشكل موثَّق.
2. **توصية scale** تُرفَع للـ Sovereign عبر صفحة Approvals.
3. **قرار scale** يُسجَّل في Decision Journal، ينتقل القطاع رسميًا إلى Internal، ويُضاف للـ Product Surface.
4. **قرار kill** يُسجَّل أيضًا — لا قطاع "يموت بصمت"؛ الدروس تُؤرشف في Vertical Library.

---

## القاعدة الجوهرية

> **Venture للتجريب، ليس للإنتاج.** أي خدمة لعميل دافع من قطاع لم يُنتقَل بعد إلى Scaling تظلّ تحت رقابة Trust الإضافية، ويُذكَر صراحة في أي مقترح أنّه ضمن "Pilot stage".

---

## English Summary

- The Venture Workspace is Dealix's structured experimentation lab for new verticals across 8 pages (Vertical Cards, Hypotheses, Experiments, vertical-tagged Signals, Pilots, Venture Evidence, Scale/Kill Recommendations, Vertical Library).
- Each vertical is represented by a standard Vertical Card JSON schema with hypothesis, ICP, value prop, primary offer, success metric, kill metric, budget cap, and review cadence.
- Two example cards (Clinics Riyadh, Real Estate Brokers KSA) are included as schema-shaped templates; budget caps are TBD and success/kill metrics are written as testable conditions.
- Promotion from testing to scaling requires a Proof Pack, a satisfied pilot, and an explicit Sovereign decision recorded in the Decision Journal.
- Verticals that are killed leave a documented lesson in the Vertical Library; no vertical exits silently.
