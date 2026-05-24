# المؤسس — قراءة 3 دقائق · 2026-05-24

> **هذا الملف يستهلك 3 دقائق من وقتك. اقرأه قبل أي شيء آخر اليوم.**

---

## 1) ماذا تغيّر في الـ 24 ساعة الماضية

| البند | الحالة قبل | الحالة الآن | الأثر عليك |
|------|------------|--------------|-------------|
| **خطة 138 مهمة (Strongest Plan)** | FAIL | ✅ PASS | لا تحقق إضافي مطلوب |
| **استخبارات PDPL مايو 2026** | مفقودة | ✅ موجودة + موجز إنفاذ | استخدمها في كل اعتراض سعر |
| **PDPL Pass Sections** | 1/6 | ✅ 6/6 | جاهزة لمراجعة محامٍ سعودي |
| **AEO Objections (PDPL)** | غير موجودة | ✅ 5 جديدة | استخدمها صباح أي مكالمة |
| **War Room Today** | مفقود | ✅ 15 هدف (placeholders) | يحتاج استبدال بأسماء warm حقيقية |
| **Sales Approval Queue** | فارغ | ✅ 8 SKIP (doctrine-correct) | **عملك:** املأ schema العملاء |
| **Sprint Readiness Audit** | غير موجود | ✅ موجود | اقرأ قبل أول صفقة |
| **Proof Pack Template TODOs** | مفتوحة | ✅ مكتملة | جاهز للتسليم |
| **KPI Guardrail** | غير موجود | ✅ يرفض placeholder data | لا تستطيع تزوير الأرقام (بحسن النية) |
| **No-Cold-Outreach Doctrine Test** | غير موجود | ✅ موجود في CI | حماية مستمرة |

---

## 2) قراراتك هذا الأسبوع (3 فقط — كل قرار 20 دقيقة كحد أقصى)

### قرار #1 — التسجيل في منصة حوكمة البيانات الوطنية (SDAIA)
- **السياق:** Dealix يستضيف على Railway (US/EU) → نقل عبر الحدود → التسجيل إلزامي
- **الخيار:** سجّل الآن استباقاً، أو انتظر أول عميل enterprise
- **توصيتي:** سجّل هذا الأسبوع — التكلفة ~ 0 (تعبئة نموذج)، الحماية كاملة
- **سجّل قرارك في:** `dealix/config/founder_weekly_one_decision.yaml`

### قرار #2 — إضافة "PDPL-Shield" كميزة بيع في `/dealix-diagnostic`
- **السياق:** PDPL لم يعد فقط سياسة داخلية — أصبح قيمة عميل قابلة للبيع (5M ريال غرامة محتملة)
- **الخيار:** نعم (تكت لـ engineer بعد payment_received) / لا
- **توصيتي:** نعم — اكتب الـ ticket فقط، لا تنفّذ قبل أول دفع

### قرار #3 — أول صفقة Diagnostic مدفوعة هذا الأسبوع
- **السياق:** هذا هو **الـ bottleneck الوحيد**. كل شيء آخر جاهز.
- **العمل المطلوب منك (4 ساعات هذا الأسبوع):**
  1. اختر 5 جهات اتصال warm حقيقية من شبكتك الشخصية (LinkedIn 1st-degree + عملاء سابقون)
  2. أضف لكل واحد: `relationship_basis` (تعرّفنا في مؤتمر X / كنت عميل قديم / شريك Y) و `consent_on_file=yes`
  3. حدّث `data/warm_list.csv` يدوياً
  4. اطلب من `dealix-sales` إعادة توليد الـ drafts → ستحصل على 5 رسائل جاهزة للموافقة
  5. اعتمد + أرسل يدوياً من رقمك الشخصي
  6. عند أول دفع 499 ريال → سجّل `payment_received` في `data/evidence_events_tracker.csv`

---

## 3) ما لا تفعله (قاعدة no-build مفعّلة)

- ❌ لا تبني features جديدة
- ❌ لا توظّف مبيعات
- ❌ لا ترسل cold outreach (حتى لو "مهذّب")
- ❌ لا تخترع أرقام KPI لتجاوز الـ guardrail
- ❌ لا ترفع الأسعار قبل 3 صفقات Managed Ops حقيقية
- ❌ لا تطلب من dealix-engineer بناء جديد قبل `payment_received`

---

## 4) أوامر سريعة (الصباح / المساء / الأسبوع)

```bash
# صباح (كل يوم — 5 دقائق):
bash scripts/founder_cadence.sh

# مساء (إغلاق اليوم):
bash scripts/founder_cadence.sh --evening

# جمعة (Scorecard أسبوعي):
bash scripts/founder_cadence.sh --weekly

# تحقق سريع للحالة:
python3 scripts/founder_strongest_plan_status.py
python3 scripts/founder_comprehensive_plan_status.py

# قبل أي ديمو / لمسة عميل:
# اقرأ: docs/commercial/MARKET_INTELLIGENCE_2026_MAY_UPDATE_AR.md §1 (PDPL) و §3 (الأسعار)
```

---

## 5) المخرجات الـ 5 الأكثر قيمة هذا الأسبوع

1. ✅ تحديث استخبارات السوق (مايو 2026) — قيمة بيع مباشر
2. ✅ PDPL Pass كامل — جاهز لمحامٍ
3. ✅ KPI Guardrail — يحميك من الكذب على نفسك بحسن النية
4. ✅ Doctrine Test — يحميك من قرار خاطئ في 3 صباحاً
5. ⏳ **أول `payment_received`** — هذا فقط بيدك

---

## 6) المراجع (إن أردت التعمق)

- **شامل:** [FOUNDER_STRONGEST_PLAN_AR.md](../commercial/FOUNDER_STRONGEST_PLAN_AR.md)
- **يومي:** [FOUNDER_OPERATING_SYSTEM_AR.md](FOUNDER_OPERATING_SYSTEM_AR.md)
- **استخبارات الشهر:** [MARKET_INTELLIGENCE_2026_MAY_UPDATE_AR.md](../commercial/MARKET_INTELLIGENCE_2026_MAY_UPDATE_AR.md)
- **بوابة Phase 0-1:** [FOUNDER_PHASE_0_1_GATE_AR.md](FOUNDER_PHASE_0_1_GATE_AR.md)
- **أول صفقة مدفوعة:** [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md)

---

*يولّد كل يوم — `scripts/founder_today_summary.py` (TODO: إضافة سكربت لاحقاً)*  
*هذا الملف ليس استشارة قانونية. للقضايا الحرجة، محامٍ سعودي مرخّص.*

**End of today's brief. Now go close one deal.**
