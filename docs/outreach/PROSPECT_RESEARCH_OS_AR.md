# نظام بحث العملاء المحتملين — Prospect Research OS

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس + عمليات الـ Outreach
**المخطط:** schemas/prospect.schema.json
**آخر تحديث:** 2026-06-02

---

## الغرض

تحويل قائمة شركات خام إلى عملاء محتملين **مؤهَّلين وآمنين قانونياً** جاهزين لمصنع المسودات (انظر docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md). البحث هنا **يدوي وبموافقة المؤسس** على المصادر — لا جمع آلي يخالف شروط استخدام أي منصة، ولا قوائم مشتراة.

## مصادر مسموحة

- بيانات يزوّدها المؤسس أو الفريق (CRM، اجتماعات سابقة، إحالات).
- مصادر عامة منشورة طوعاً: الموقع الرسمي للشركة، السجل التجاري العام، صفحة «من نحن»، إعلانات توظيف عامة، أخبار قطاعية.
- بحث ويب يدوي موثّق المصدر في حقل `source`.

## مصادر ممنوعة

- أي **LinkedIn automation** أو سحب جماعي يخالف شروط المنصة.
- قوائم مشتراة بدون عقد استخدام صريح.
- بيانات شخصية حسّاسة (هوية وطنية، أرقام خاصة) — لا تُخزَّن مطلقاً في سجل العميل المحتمل.

> القاعدة: إن لم يكن المصدر **عاماً منشوراً بإرادة الشركة** أو **مزوّداً من المؤسس**، لا يدخل النظام.

## نموذج التسجيل (Prospect Score)

كل عميل محتمل يحصل على درجة من 100 بالأوزان التالية. الدرجة تُرتِّب صف الموافقة، ولا تُلغي حكم المؤسس.

| العامل | الوزن | ماذا نقيس |
|--------|------|-----------|
| ملاءمة القطاع (sector fit) | 20 | هل القطاع ضمن ICP المعتمد |
| تدفق العملاء المتوقع (likely lead flow) | 20 | حجم الطلب الذي قد يستفيد من خدمتنا |
| وضوح صانع القرار (decision-maker clarity) | 15 | هل نعرف الدور المسؤول عن القرار |
| إشارة الألم (pain signal) | 15 | دليل ملموس على مشكلة نحلّها |
| القدرة على الدفع (payment ability) | 15 | مؤشرات حجم/نضج تدعم سلّم الأسعار |
| إشارة التخصيص (personalization signal) | 10 | تفصيل حقيقي محدّد نبني عليه الرسالة |
| انخفاض المخاطر (low risk) | 5 | لا تعارض امتثال أو سمعة |

**عتبات:** ≥70 مؤهَّل للمسودة · 50–69 يحتاج إشارة تخصيص أقوى قبل المسودة · <50 إلى `nurture` أو استبعاد.

## حالات العميل المحتمل (Prospect States)

التسلسل المعتمد في `state`:

`researched` → `qualified` → `draft_ready` → `drafted` → `approved` → `sent` → `replied` → `meeting_booked` → `proposal_needed` → `proposal_sent` → `won` / `lost`

حالات جانبية: `nurture` (غير جاهز الآن) · `do_not_contact` (استبعاد دائم — طلب توقّف، تعارض، أو قائمة كبح).

- لا ينتقل عميل إلى `drafted` قبل اكتمال إشارة تخصيص حقيقية (انظر docs/outreach/PERSONALIZATION_RULES_AR.md).
- لا ينتقل إلى `sent` إلا عبر صف موافقة المؤسس وخطة الإرسال المرحلية (docs/outreach/SENDING_RAMP_OS_AR.md).
- `do_not_contact` نهائي ويُزامَن مع قائمة الكبح schemas/suppression.schema.json.

## حقول السجل (مرجع المخطط)

```
company, sector, website, decision_maker_role, source,
pain_signal, payment_ability, personalization_signal,
sector_fit_score, lead_flow_score, decision_maker_score,
pain_score, payment_score, personalization_score, risk_score,
total_score, state, consent_status, do_not_contact
```

## سير العمل اليومي

1. **التقاط:** إدخال الشركات من المصدر المعتمد مع `source` لكل صف.
2. **تأهيل:** حساب الدرجات السبع وتعبئة `total_score` و`state=qualified` عند ≥70.
3. **إشارة تخصيص:** توثيق تفصيل حقيقي واحد على الأقل لكل عميل — وإلا يبقى `researched`.
4. **فحص الكبح:** مطابقة كل عميل مع قائمة الكبح؛ أي تطابق → `do_not_contact`.
5. **تسليم:** الترقية إلى `draft_ready` وتمرير الدفعة إلى مصنع المسودات.

## ضوابط لا يجوز تجاوزها

- لا واتساب بارد. التواصل الأول بريد فقط؛ واتساب بعد رد/موافقة (docs/whatsapp/).
- لا تخصيص مُختلَق — كل إشارة قابلة للتحقق من مصدرها.
- لا ترقية إلى `sent` بدون موافقة المؤسس وفحص صحة النطاق والكبح والانسحاب.
- احترام أي طلب توقّف فوراً عبر `do_not_contact`.

## روابط

- مصنع المسودات: docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md
- قواعد التخصيص: docs/outreach/PERSONALIZATION_RULES_AR.md
- صف موافقة المؤسس: docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md
- سياسة الامتثال: docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md
- خطة الإرسال المرحلية (سياسة التسليم): docs/outreach/SENDING_RAMP_PLAN_AR.md

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
