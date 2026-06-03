# نظام البحث عن العملاء المحتملين — Prospect Research OS
# Prospect Research Operating System

**المسار:** `docs/outreach/PROSPECT_RESEARCH_OS_AR.md`
**الجمهور:** المؤسس + مسؤول العمليات
**آخر تحديث:** 2026-06-02
**الحالة:** نافذ

---

## قاعدة الأولوية / Priority Rule

**العربية أولاً. لا شراء قوائم. لا scraping. كل بيانات لها مصدر موثّق.**

All prospect data enters through one of four approved channels only. Any other source is blocked at the compliance gate in `auto_client_acquisition/email/compliance.py`.

---

## 1. مصادر البيانات المسموح بها / Approved Data Sources

### 1.1 قوائم المؤسس المورّدة / Founder-Supplied Lists

القوائم التي يجمعها المؤسس يدوياً من مصادر عامة مشروعة:

- دلائل الأعمال السعودية (مجلس الغرف، منصة Maroof، وزارة التجارة — عام ومتاح للعموم)
- البحث اليدوي على Google Maps + Google Business (قراءة عامة، لا scraping آلي)
- حضور الفعاليات والمعارض التجارية السعودية (بطاقات عمل بإذن صريح)
- بحث LinkedIn يدوي من خلال واجهة المستخدم الاعتيادية (لا أتمتة، لا LinkedIn automation)

**القاعدة الصارمة:** لا قوائم مشتراة من مزودي بيانات بدون عقد استخدام مُعتمد. لا web scraping آلي. راجع `auto_client_acquisition/safe_send_gateway/doctrine.py`.

### 1.2 البحث العام اليدوي / Manual Public Research

البحث الذي يُنفَّذ يدوياً على:

- الموقع الرسمي للشركة (قراءة، لا جمع آلي)
- السجل التجاري العام
- مشاركات LinkedIn العامة للشركة (قراءة فقط)
- أخبار القطاع والتقارير العامة

**ما يُنتج:** `personalization_note` و`pain_hypothesis` و`sources_used` في سجل العميل المحتمل.

### 1.3 الطلبات الواردة / Inbound Leads

- نماذج الموقع الإلكتروني لـ Dealix
- طلبات جُمعت في جلسات اكتشاف أو ديمو
- إحالات مباشرة من شركاء أو عملاء حاليين (بموافقة الطرف المُحيل)

هذه الفئة تحمل `consent_status = explicit_inbound` وتتقدم إلى المرحلة `qualified` مباشرة إذا استوفت معايير النقاط.

### 1.4 الإحالات / Referrals

- إحالة من عميل حالي أو شريك يمتلك علاقة مسبقة مع الشركة المستهدفة
- يُسجَّل اسم المُحيل ونوع العلاقة في حقل `source` في سجل العميل المحتمل
- يُعامَل كـ warm outreach، لا cold outreach

---

## 2. مخطط بيانات العميل المحتمل / Prospect Schema

المرجع التقني: `schemas/prospect.schema.json` و`data/prospects/`

| الحقل | النوع | الوصف |
|---|---|---|
| `id` | UUID | معرّف فريد |
| `company` | string | اسم الشركة |
| `sector` | enum | القطاع من تصنيف `SECTOR_BRIEFS` في `research_agent.py` |
| `recipient_role` | string | دور متلقي الرسالة (مدير مبيعات، مدير عام، الخ) |
| `source` | enum | `founder_list`, `inbound`, `referral`, `manual_research` |
| `pain_hypothesis` | string | فرضية الألم المبنية على القطاع + إشارات التخصيص |
| `personalization_note` | string | ملاحظة تخصيص محددة ومرتبطة بمصدر حقيقي |
| `allowed_use` | string | يجب أن يكون موثّقاً وليس `unknown` |
| `consent_status` | string | `public_business`, `explicit_inbound`, `referral_warm` |
| `risk_level` | enum | `low`, `medium`, `high` |
| `prospect_score` | integer | 0–100 (انظر القسم 3) |
| `state` | enum | 14 حالة (انظر القسم 4) |
| `do_not_contact` | boolean | إذا `true` → محجوب نهائياً في جميع القنوات |
| `opt_out` | boolean | إلغاء استلام صريح — يُعامَل مثل `do_not_contact` |
| `bounced_before` | boolean | ارتداد بريد سابق |
| `suppressed_at` | datetime | تاريخ الإضافة لقائمة الحظر |
| `last_contacted_at` | datetime | آخر تواصل |
| `data_quality_score` | integer | 0–100 (من `deliverability_check.py` و scoring pipeline) |

---

## 3. معايير تقييم النقاط / Prospect Scoring Rubric

المجموع الكلي: **100 نقطة**. الحد الأدنى للتأهيل: **60 نقطة**.

| المعيار | الوزن | 0 نقطة | نقطة كاملة |
|---|---|---|---|
| `sector_fit` — توافق القطاع مع ICP الحالي | 20 | قطاع خارج التصنيف | قطاع أساسي (عقار، مقاولات، ضيافة، لوجستيات، SaaS) |
| `likely_lead_flow` — احتمال تدفق leads | 20 | نشاط ليس lead-driven | نشاط يعتمد على استفسارات واردة يومياً |
| `decision_maker_clarity` — وضوح صانع القرار | 15 | لا يوجد اسم أو دور | اسم + دور محدد موثّق |
| `pain_signal` — إشارة ألم موثّقة | 15 | لا توجد إشارة | إشارة محددة من القطاع أو من البحث |
| `payment_ability` — قدرة الدفع | 15 | غير واضحة + لا مؤشرات | مؤشرات نشاط تجاري نشط + قدرة pilot واضحة |
| `personalization_signal` — وجود إشارة تخصيص حقيقية | 10 | لا توجد | إشارة P1 على الأقل (انظر `PERSONALIZATION_RULES_AR.md`) |
| `low_risk` — خفض المخاطر الامتثالية | 5 | `risk_level=high` أو `allowed_use=unknown` | `risk_level=low` + `allowed_use` موثّق |

**العتبات:**

- 80–100: أولوية قصوى — يدخل مباشرة في المسودة اليومية الأولى
- 60–79: مؤهل — يُضاف للقائمة اليومية حسب التوافر
- 40–59: يحتاج إثراء — يبقى في حالة `researched` حتى تُحسَّن البيانات
- 0–39: غير مؤهل — يُعاد للمراجعة في 90 يوماً

---

## 4. الحالات الأربع عشرة / The 14 Prospect States

```
researched        → qualified         → draft_ready       → drafted
→ approved        → sent              → replied           → meeting_booked
→ proposal_needed → proposal_sent     → won               → lost
→ nurture         → do_not_contact
```

| الحالة | التعريف | من يُحدّثها |
|---|---|---|
| `researched` | البيانات جُمعت، النقاط لم تُحسب بعد | `research_agent.py` |
| `qualified` | نقاط ≥ 60، اجتاز فحص الامتثال | `daily_targeting.py` |
| `draft_ready` | جاهز لمصنع المسودات | `daily_targeting.py` |
| `drafted` | مسودة رسالة موجودة في قائمة الموافقة | `COLD_EMAIL_DRAFT_FACTORY_AR.md` |
| `approved` | المؤسس وافق على المسودة | `approval_center/` |
| `sent` | الرسالة أُرسلت فعلياً | `gmail_send.py` |
| `replied` | ردّ وارد من الشركة | `reply_classifier.py` |
| `meeting_booked` | اجتماع محجوز في التقويم | `agents/booking.py` |
| `proposal_needed` | قرار اجتماع: يحتاج عرضاً سعرياً | `agents/proposal.py` |
| `proposal_sent` | العرض السعري أُرسل | `agents/proposal.py` |
| `won` | العقد أُغلق | المؤسس يُدخل يدوياً |
| `lost` | العقد أُغلق بخسارة، لا متابعة قريبة | المؤسس يُدخل يدوياً |
| `nurture` | غير جاهز الآن — يُعاد التواصل في 30–90 يوماً | تلقائي بعد متابعة 2 |
| `do_not_contact` | طلب صريح لعدم التواصل — نهائي | غير قابل للتجاوز |

---

## 5. قاعدة الإقصاء أولاً / Suppression-First Rule

**قبل أي بحث أو إثراء، يُطبَّق الفلتر التالي بالترتيب:**

1. `do_not_contact = true` → محجوب نهائياً، لا استثناء
2. `opt_out = true` → محجوب، يُسجَّل في قائمة الحظر
3. البريد الإلكتروني أو النطاق موجود في قائمة الحظر → محجوب
4. `bounced_before = true` → محجوب
5. `risk_level = high` → يحتاج مراجعة صريحة من المؤسس قبل المتابعة
6. `allowed_use` غير موثّق → محجوب حتى التوثيق

هذا الترتيب مُطبَّق برمجياً في `compliance.py` (`check_outreach()`) ولا يمكن تجاوزه.

---

## 6. معالجة طلبات do_not_contact

عندما يطلب شخص أو شركة عدم التواصل:

1. يُحدَّث حقل `do_not_contact = true` فوراً في السجل
2. يُضاف البريد الإلكتروني + النطاق لقائمة الحظر الرئيسية
3. يُلغى أي مسودة في الانتظار لهذا الحساب
4. لا يمكن لأي مستخدم أو عملية آلية تغيير هذه الحالة إلى `false` بدون توثيق مكتوب ومراجعة يدوية
5. تُحفظ قائمة الحظر في ملف منفصل يُنسخ احتياطياً يومياً

راجع: [`docs/outreach/UNSUBSCRIBE_POLICY_AR.md`](./UNSUBSCRIBE_POLICY_AR.md)

---

## 7. كيف يُغذّي البحثُ مصنعَ المسودات / Research → Draft Factory Flow

```
[مصدر البيانات المعتمد]
        ↓
[research_agent.py → CompanyBrief]
   (sector + pain_hypothesis + personalization_note + best_offer)
        ↓
[daily_targeting.py → فلترة + تقييم + ترتيب]
   (يُطبّق suppression-first + حد 50 يومياً)
        ↓
[حالة: draft_ready]
        ↓
[COLD_EMAIL_DRAFT_FACTORY_AR.md — مصنع المسودات]
   (ينتج outreach_draft كامل الحقول)
        ↓
[FOUNDER_APPROVAL_QUEUE_AR.md — قائمة انتظار الموافقة]
   (المؤسس يراجع + يوافق أو يرفض)
        ↓
[gmail_send.py — إرسال فعلي بعد الموافقة فقط]
```

**الوحدات البرمجية المرجعية:**

- `auto_client_acquisition/email/research_agent.py` — إنتاج `CompanyBrief`
- `auto_client_acquisition/email/daily_targeting.py` — الاختيار اليومي والجدولة
- `auto_client_acquisition/email/compliance.py` — بوابة الامتثال
- `auto_client_acquisition/email/deliverability_check.py` — التحقق من DNS وجاهزية الإرسال
- `auto_client_acquisition/channel_policy_gateway/email.py` — قرارات السماح/المنع
- `auto_client_acquisition/safe_send_gateway/` — قواعد العقيدة غير القابلة للتفاوض

---

## 8. القواعد الصارمة لهذا الملف / Non-Negotiables for Prospect Research

هذه القواعد مأخوذة من عقيدة Dealix وتُطبَّق في جميع مراحل البحث:

1. لا شراء قوائم بريدية أو قواعد بيانات من مزودين خارجيين دون عقد استخدام مُعتمد من المؤسس
2. لا scraping آلي لأي موقع إلكتروني — الجمع اليدوي الفردي فقط
3. لا LinkedIn automation — بحث يدوي فقط عبر واجهة المستخدم
4. لا WhatsApp بارد — أي تواصل عبر WhatsApp يستلزم موافقة صريحة مسبقة
5. كل `personalization_note` يجب أن يستند لإشارة حقيقية موثّقة لا لاستنتاج مختلق
6. تُحفَظ جميع بيانات العملاء المحتملين وفق سياسة `docs/04_data_os/DATA_RETENTION_POLICY.md`
7. أي بيانات شخصية تتطلب امتثال PDPL — راجع `docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`

---

## روابط ذات صلة

- [`docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`](./COLD_EMAIL_DRAFT_FACTORY_AR.md) — كيف تتحول `draft_ready` إلى مسودة
- [`docs/outreach/PERSONALIZATION_RULES_AR.md`](./PERSONALIZATION_RULES_AR.md) — معايير التخصيص P0–P3
- [`docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md`](./COLD_EMAIL_COMPLIANCE_AR.md) — قواعد الامتثال الكاملة
- [`docs/outreach/UNSUBSCRIBE_POLICY_AR.md`](./UNSUBSCRIBE_POLICY_AR.md) — إدارة إلغاء الاستلام
- [`docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md`](./FOUNDER_APPROVAL_QUEUE_AR.md) — عملية موافقة المؤسس
- [`docs/commercial/PRODUCT_CATALOG_AR.md`](../commercial/PRODUCT_CATALOG_AR.md) — العروض المتاحة للإشارة إليها في المسودات
- [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md) — الفهرس الرئيسي لـ GTM
- [`docs/04_data_os/DATA_RETENTION_POLICY.md`](../04_data_os/DATA_RETENTION_POLICY.md) — سياسة الاحتفاظ بالبيانات
- `schemas/prospect.schema.json` — المخطط التقني (انظر القسم 2 أعلاه)
- `data/prospects/` — ملفات البيانات الفعلية

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
