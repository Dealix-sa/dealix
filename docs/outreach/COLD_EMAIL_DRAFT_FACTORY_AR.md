# مصنع المسودات — Cold Email Draft Factory
# Cold Email Draft Factory — Operating Spec

**المسار:** `docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`
**الجمهور:** المؤسس + مسؤول العمليات التجارية
**آخر تحديث:** 2026-06-02
**الحالة:** نافذ

---

## الغرض / Purpose

هذا المصنع يُنتج حتى 250 مسودة يومياً جاهزة لمراجعة المؤسس. **لا مسودة تُرسَل بدون موافقة صريحة.** كل ما يخرج من هذا المصنع يذهب مباشرة إلى قائمة انتظار الموافقة في [`docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md`](./FOUNDER_APPROVAL_QUEUE_AR.md).

الفرق الجوهري:
- **250 مسودة/يوم:** مسموح (draft_only mode)
- **250 إرسال/يوم:** **ممنوع** حتى تجتاز هذه الشروط كلها: SPF + DKIM + DMARC مُفعّلة + رابط إلغاء استلام + قائمة الحظر نشطة + منحنى الإحماء مكتمل + موافقة المؤسس على كل دفعة

المرجع التقني: `auto_client_acquisition/email/daily_targeting.py` + `auto_client_acquisition/channel_policy_gateway/email.py`

---

## 1. التوزيع اليومي للمسودات / Daily Draft Mix

| النوع | العدد | الهدف |
|---|---|---|
| أول تواصل (first-touch) | 100 | فتح محادثة جديدة مع حساب لم يُتواصل معه من قبل |
| متابعة أولى (follow-up 1) | 75 | التذكير بعد 3 أيام عمل من first-touch بدون رد |
| متابعة ثانية (follow-up 2) | 50 | محاولة أخيرة قبل الانتقال لحالة nurture |
| مقدمة للعرض السعري (proposal-intro) | 15 | لحسابات وصلت لحالة `meeting_booked` أو `proposal_needed` |
| إغلاق المحادثة (close-loop/breakup) | 10 | رسالة نهائية مهذبة قبل إغلاق الملف |
| **المجموع** | **250** | |

**ملاحظة التوقيت:** يعمل المصنع يومياً في 7:00 صباح (توقيت الرياض) عبر `daily_targeting.py`. النتيجة تُعرض على المؤسس في قائمة الموافقة قبل 9:00 صباحاً.

---

## 2. حقول مسودة التواصل الكاملة / Full outreach_draft Field List

المرجع التقني: `schemas/outreach_draft.schema.json`

| الحقل | النوع | القيم المسموحة / الوصف |
|---|---|---|
| `company` | string | اسم الشركة من سجل العميل المحتمل |
| `sector` | string | القطاع من `SECTOR_BRIEFS` في `research_agent.py` |
| `recipient_role` | string | الدور المستهدف (مدير عام، مدير مبيعات، الخ) |
| `source` | enum | `founder_list`, `inbound`, `referral`, `manual_research` |
| `pain_hypothesis` | string | فرضية الألم المبنية على البحث — لا اختراع |
| `personalization_note` | string | الإشارة الحقيقية المستخدمة في التخصيص (مستوى P1 حد أدنى) |
| `offer` | string | أحد: `pilot_499`, `pilot_999`, `pilot_1500`, `partnership` |
| `subject` | string | سطر الموضوع — لا يحتوي فرضية Re: أو Fwd: مزيّفة |
| `body` | string | نص الرسالة الكامل بما فيه سطر إلغاء الاستلام |
| `CTA` | string | طلب واحد فقط — لا CTAs متعددة في رسالة واحدة |
| `language` | enum | `ar`, `en`, `ar_en_bilingual` |
| `evidence_level` | enum | `none`, `sector_pattern`, `case_safe`, `verified` |
| `risk_level` | enum | `low`, `medium`, `high` |
| `compliance_status` | enum | `pass`, `needs_review`, `blocked` |
| `approval_status` | enum | `pending`, `approved`, `rejected` |
| `send_status` | enum | `not_sent`, `sent`, `failed`, `bounced` |
| `unsubscribe_included` | boolean | يجب أن يكون `true` في كل رسالة تسويقية |
| `personalization_score` | enum | `P0`, `P1`, `P2`, `P3` (انظر `PERSONALIZATION_RULES_AR.md`) |

---

## 3. بوابة المنع — متى لا تُنتج المسودة / Draft Blocking Gate

**المصنع يمتنع عن إنتاج مسودة إذا انطبق أي شرط من الشروط التالية:**

1. **`personalization_score < P1`** — الرسالة عامة بالكامل بدون أي إشارة محددة
2. **`risk_level = high`** — الحساب يحمل علامة مخاطرة عالية
3. **`unsubscribe_included = false`** — لم يُضف سطر إلغاء الاستلام
4. **ادعاء يفتقر لدليل** — أي رقم أو وعد لا يُقابله `evidence_level` ≥ `sector_pattern`
5. **الشركة في قائمة الحظر** — أي نطاق أو بريد إلكتروني في قائمة الحظر الرئيسية
6. **سطر الموضوع مضلل** — Re: أو Fwd: مزيّف، أو ادعاء تعامل سابق لا يوجد
7. **`compliance_status = blocked`** — المسودة فشلت في فحص `compliance.py`
8. **`allowed_use`** غير موثّق في سجل الحساب
9. **`do_not_contact = true`** أو **`opt_out = true`** — محجوب نهائياً

الفحص يُطبَّق في `auto_client_acquisition/email/compliance.py` (دالة `check_outreach()`) وفي `auto_client_acquisition/channel_policy_gateway/email.py`.

---

## 4. شروط جاهزية الإرسال / Send Readiness Conditions

المسودات لا تتحول إلى إرسال حتى تجتاز هذا الفحص كاملاً عبر `auto_client_acquisition/email/deliverability_check.py`:

| الشرط | الأداة | الحالة المطلوبة |
|---|---|---|
| SPF record صحيح | `deliverability_check.py` | `spf.is_valid = true` |
| DKIM record صحيح | `deliverability_check.py` | `dkim.is_valid = true` |
| DMARC record صحيح | `deliverability_check.py` | `dmarc.is_valid = true` |
| رابط إلغاء الاستلام | `compliance.py` → `append_opt_out_line()` | موجود في كل رسالة |
| قائمة الحظر نشطة | `compliance.py` | `suppression_emails` + `suppression_domains` محمّلة |
| منحنى الإحماء | جدول الإحماء اليدوي | يجب احترامه (انظر القسم 5) |
| موافقة المؤسس | `approval_center/` | `approval_status = approved` |

عند اكتمال هذه الشروط: `DeliverabilityStatus.overall_status = "ready_for_marketing"`.

---

## 5. منحنى الإحماء / Warm-Up Ramp

قبل الوصول لـ 250 إرسال/يوم، يجب اتباع هذا الجدول:

| الأسبوع | الحد اليومي للإرسال | الشرط |
|---|---|---|
| 1 | 10 | SPF + DKIM + DMARC كلها صحيحة |
| 2 | 25 | bounce rate < 2% في الأسبوع الأول |
| 3 | 50 | bounce rate < 2% تراكمياً |
| 4 | 100 | spam complaint rate < 0.1% |
| 5+ | 250 | جميع المعدلات ضمن الحدود + مراجعة أسبوعية |

**ملاحظة:** هذا الجدول حد أقصى، ليس هدفاً. جودة القائمة تُقدَّم على الكمية دائماً.

---

## 6. مسار الإنتاج التفصيلي / Production Pipeline

```
[daily_targeting.py — 7:00 صباحاً]
    ↓
[فلترة الحظر + الامتثال]
    (compliance.py → check_outreach())
    ↓
[تقييم النقاط + اختيار التنوع القطاعي]
    (select_top_n_diversified())
    ↓
[البحث عن كل حساب]
    (research_agent.py → CompanyBrief)
    ↓
[تحديد نوع المسودة]
    (first-touch / follow-up 1 / follow-up 2 / proposal-intro / close-loop)
    ↓
[فحص بوابة المنع — القسم 3]
    ↓ يجتاز الفحص
[إنتاج outreach_draft كاملة الحقول]
    ↓
[تسجيل: draft.compliance_status + draft.approval_status = pending]
    ↓
[FOUNDER_APPROVAL_QUEUE — لا إرسال تلقائي]
```

---

## 7. القواعد الصارمة / Non-Negotiables

المأخوذة من `auto_client_acquisition/safe_send_gateway/doctrine.py`:

- **ممنوع تماماً:** واتساب بارد، LinkedIn automation، bulk outreach بدون موافقة، ادعاءات مبيعات مضمونة، scraping
- **كل مسودة تخضع لمراجعة المؤسس قبل الإرسال** — لا استثناء حتى لمسودات منخفضة المخاطرة
- **سطر إلغاء الاستلام إلزامي** في كل رسالة تسويقية — مُطبَّق برمجياً في `compliance.py` عبر `append_opt_out_line()`
- **طلبات إلغاء الاستلام تُنفَّذ فوراً** — خلال 24 ساعة كحد أقصى، وتُضاف لقائمة الحظر بشكل دائم
- لا `Re:` أو `Fwd:` في سطر الموضوع إلا إذا كانت ردّاً حقيقياً على محادثة فعلية

---

## روابط ذات صلة

- [`docs/outreach/PROSPECT_RESEARCH_OS_AR.md`](./PROSPECT_RESEARCH_OS_AR.md) — كيف تُوصل الحسابات لمرحلة draft_ready
- [`docs/outreach/PERSONALIZATION_RULES_AR.md`](./PERSONALIZATION_RULES_AR.md) — تعريف مستويات P0–P3
- [`docs/outreach/COLD_EMAIL_SEQUENCES_AR.md`](./COLD_EMAIL_SEQUENCES_AR.md) — القوالب التفصيلية لكل نوع مسودة
- [`docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md`](./COLD_EMAIL_COMPLIANCE_AR.md) — قواعد الامتثال الكاملة
- [`docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md`](./FOUNDER_APPROVAL_QUEUE_AR.md) — عملية الموافقة
- [`docs/outreach/UNSUBSCRIBE_POLICY_AR.md`](./UNSUBSCRIBE_POLICY_AR.md) — سياسة إلغاء الاستلام
- [`docs/commercial/PRODUCT_CATALOG_AR.md`](../commercial/PRODUCT_CATALOG_AR.md) — تفاصيل العروض المتاحة
- [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md) — الفهرس الرئيسي
- `schemas/outreach_draft.schema.json` — المخطط التقني الكامل

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
