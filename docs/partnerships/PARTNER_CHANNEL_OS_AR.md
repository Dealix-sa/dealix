# نظام توزيع شراكات القنوات — Partner Channel OS
## الشريك يملك علاقة العميل؛ Dealix يشغّل Revenue OS

**المرجع الرئيسي:** [`docs/partners/PARTNER_PROGRAM.md`](../partners/PARTNER_PROGRAM.md) · [`docs/partners/PARTNER_PACKAGES.md`](../partners/PARTNER_PACKAGES.md)
**وحدات الكود:** `auto_client_acquisition/partnership_os/` (fit_score.py · partner_motion.py · partner_profile.py · referral_store.py · referral_tracker.py)
**المخطط:** `schemas/partner.schema.json` · بيانات الشركاء: `data/partners/`
**مؤشر الإنتاج:** [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md)

---

## 1 — ما هو نظام قناة الشراكات

Dealix لا تقوم ببيع مباشر وحصري. القناة غير المباشرة هي الوصف الدقيق: الشريك يحتفظ بعلاقة العميل ويقدّم خدمات التنفيذ أو الاستشارة، وDealix توفّر طبقة Revenue OS — التشخيص، وإثبات القيمة، والحوكمة، والقياس.

هذا النموذج يعني:

- الشريك لا يتنازل عن علاقة عملائه لجهة أخرى.
- Dealix لا تتواصل مع عملاء الشريك مباشرةً دون موافقة الشريك والعميل.
- كل اتفاق يبدأ بسيط — إحالة واحدة أو Diagnostic مشترك واحد — ثم يتوسّع بناءً على أدلة.

---

## 2 — أنواع الشركاء المناسبين

| نوع الشريك | سبب الملاءمة |
|---|---|
| وكالات التسويق والمحتوى | لديها قواعد عملاء B2B يحتاجون تحسين إيراداتهم |
| مستشارو الأعمال والإدارة | يدخلون مراحل التشخيص والتحسين — Dealix يكمّل عملهم |
| منفّذو CRM (HubSpot / Zoho / SFDC) | يُضيفون طبقة تشغيل البيانات فوق CRM الذي نصّبوه |
| شركات ومكاتب المحاسبة | لديها رؤية على الفواتير والأداء — نقطة دخول طبيعية |
| مزودو التدريب والتأهيل | يُقدّمون محتوى؛ Dealix يُضيف التطبيق التشغيلي |
| وكالات الويب والبرمجيات | يبنون أنظمة العميل؛ Dealix يشغّل طبقة القياس والإثبات |
| موزّعو البرمجيات (Resellers) | لديهم قواعد عملاء SME جاهزة للتحسين التشغيلي |

---

## 3 — نماذج التقسيم

| نموذج الشراكة | الوصف | نطاق الحصة (توجيهي، يُقرّه المؤسس) |
|---|---|---|
| رسوم إحالة (Referral Fee) | الشريك يُحيل؛ Dealix تنفّذ؛ الشريك يحصل على نسبة من أول دفعة | 10–20% من قيمة أول سبرنت أو اشتراك |
| تقسيم إيراد (Revenue Share) | تنفيذ مشترك؛ الشريك يمتلك جزءاً من الإيراد الشهري | يُحدَّد حسب جهد التنفيذ؛ لا يُفعَّل قبل وجود بيانات إحالة |
| هامش تنفيذ (Implementation Margin) | الشريك يحتفظ برسوم تنفيذه؛ Dealix تُكمّل بطبقة التشخيص + الإثبات | الشريك يُسعّر تنفيذه باستقلالية |
| White-label | Dealix تعمل تحت علامة الشريك | مقيّد: لا يُفعَّل قبل 3 pilots مدفوعة موثّقة |

لا يوجد حصرية. لا شريك يحصل على استثناء من هذا القيد.

---

## 4 — دورة حياة الشريك

```
تحديد → تأهيل (fit_score) → اتفاق → تمكين → تسليم مشترك → متابعة
```

### 4.1 تحديد (Identify)

الشريك المحتمل يُضاف بـ `partner_profile.Partner` بحقول:
`partner_id`, `placeholder_name`, `partner_type`, `sector`, `region`, `status = "pending"`.
لا يُضاف اسم حقيقي في الريبو — يستخدم placeholder.

### 4.2 تأهيل (Qualify — fit_score)

`fit_score.compute_fit_score()` يحسب درجة 0–100 بناءً على:

| معيار | نقاط |
|---|---|
| نوع الشريك (sales_consultant / crm_implementer = 30) | 15–30 |
| يخدم B2B | 20 |
| لديه قاعدة عملاء قائمة | 25 |
| تركيز على السوق السعودية | 15 |
| منطقة (الرياض / جدة / الدمام / الشرق) | 10 |

**عتبات القرار:**
- أقل من 40: لا شراكة.
- 40–59: إحالة فقط — جرّب 2–3 إحالات.
- 60–79: Diagnostic مشترك بالعلامتين.
- 80+: مؤهَّل للـ Proof Pack المشترك وما يليه (بموافقة المؤسس).

### 4.3 اتفاق (Agree)

اتفاق بسيط يحدّد: النموذج، نسبة التقسيم، آلية التتبع عبر `referral_store`، نافذة الإسناد.
لا عقود معقّدة في المرحلة الأولى.

### 4.4 تمكين (Enable)

- Playbook المناسب (وكالة → [`AGENCY_PARTNER_PLAYBOOK_AR.md`](./AGENCY_PARTNER_PLAYBOOK_AR.md) · مستشار → [`CONSULTANT_PARTNER_PLAYBOOK_AR.md`](./CONSULTANT_PARTNER_PLAYBOOK_AR.md)).
- كود إحالة يُنشأ عبر `referral_store.create_referral_code()`.
- جلسة تمكين واحدة (60 دقيقة) تشمل: العرض، نقاط الحديث، حدود ما يجوز للشريك ادّعاؤه.

### 4.5 تسليم مشترك (Co-deliver)

- الشريك يُحيل أو يشارك في التنفيذ.
- `referral_tracker.add_referral()` يسجّل كل إحالة.
- كل اتصال بعميل الشريك يستلزم موافقة مسبقة صريحة من الشريك والعميل.

### 4.6 متابعة (Track)

- الإيراد المُسنَد للشريك يُتابَع في لوحة خط أنابيب الشراكات: [`reports/partnerships/PARTNER_PIPELINE.md`](../../reports/partnerships/PARTNER_PIPELINE.md).
- المراجعة الشهرية: هل وصلت الإحالات إلى مستوى `has_referral_data = True`؟ هذا الشرط ضروري لتفعيل نموذج Revenue Share.

---

## 5 — ما لا يفعله Dealix عبر قنوات الشركاء

- لا يُرسل Dealix رسائل باسم الشريك دون إذن صريح مكتوب.
- لا يُجري Dealix اتصالاً بارداً بأي قناة بحجة كونه "شريك".
- لا يعدّ Dealix بأرقام مبيعات أو نسب تحويل كحقائق — كل تقدير مُصنَّف "تقديري" وليس قيمة مُتحقَّقة.

---

## 6 — الحوكمة والامتثال

كل اتفاق شراكة يخضع لمبادئ PDPL: لا يُشارك Dealix بيانات العميل مع الشريك دون موافقة العميل. راجع [`docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`](../02_saudi_positioning/PDPL_AWARE_LANGUAGE.md).

---

## English Mirror — Partner Channel OS

**Model:** The partner owns the client relationship; Dealix operates the Revenue OS layer.

Dealix uses indirect distribution. Partners retain client ownership and deliver implementation or advisory services. Dealix contributes the Revenue OS: diagnostic, value proof, governance, and measurement.

**Suitable partner types:** marketing agencies, business consultants, CRM implementers, accounting firms, training providers, web agencies, software resellers.

**Split options (indicative, founder-approved per deal):**

| Model | Description | Indicative Range |
|---|---|---|
| Referral Fee | Partner refers; Dealix delivers | 10–20% of first sprint/subscription |
| Revenue Share | Joint delivery; partner takes monthly share | Set by implementation effort; requires live referral data |
| Implementation Margin | Partner bills own fees; Dealix adds diagnostic layer | Partner prices independently |
| White-label | Dealix operates under partner brand | Restricted: min. 3 documented paid pilots required |

**Partner lifecycle:** Identify → Qualify (fit_score) → Agree → Enable → Co-deliver → Track.

No exclusivity is granted to any partner, at any tier.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
