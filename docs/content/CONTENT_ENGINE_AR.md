# محرك المحتوى — Content Engine

> نظام إنتاج المحتوى اليومي والأسبوعي لـ Dealix. كل قطعة محتوى تبدأ كمسودة وتنتهي بموافقة المؤسس قبل النشر اليدوي.
>
> روابط: [`auto_client_acquisition/gtm_os/content_calendar.py`](../../auto_client_acquisition/gtm_os/content_calendar.py) · [`auto_client_acquisition/gtm_os/message_experiment.py`](../../auto_client_acquisition/gtm_os/message_experiment.py) · [`dealix/marketing_factory/weekly_pack.py`](../../dealix/marketing_factory/weekly_pack.py) · [`dealix/marketing_factory/content_calendar.seed.yaml`](../../dealix/marketing_factory/content_calendar.seed.yaml) · [`docs/content/LINKEDIN_CADENCE_PLAN.md`](./LINKEDIN_CADENCE_PLAN.md) · [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md) · [`docs/brand/BRAND_CONTENT_RULES_AR.md`](../brand/BRAND_CONTENT_RULES_AR.md)

---

## المبدأ التشغيلي — Operating Principle

كل محتوى ينشأ من ألم قطاعي موثق أو دليل ميداني، لا من جداول ملء. المنشور بلا ربط بـ sector + pain + proof هو منشور لا يُنشَر.

**المسار الإلزامي لكل قطعة:**
```
فكرة → صياغة مسودة → مراجعة الحواجز (11 غير قابل للتفاوض) → موافقة المؤسس → نشر يدوي
```

لا أتمتة نشر. لا إرسال مجدول تلقائي. `content_calendar.py` و `weekly_pack.py` ينتجان مسودات فقط — حقل `approval_status` يبقى `approval_required` حتى تتحول الموافقة يدوياً.

---

## الجدول اليومي — Daily Cadence (4 أنواع)

### النوع 1 — رؤية المؤسس (Founder Insight)

**التكرار:** يومي (بحسب ما هو متاح من رؤى حقيقية، ليس ملء إلزامي).

**التعريف:** ملاحظة قصيرة من العمل الفعلي — اكتشاف في بيانات، قرار اتُّخذ، رفض لشيء ما وسببه.

**الضوابط:**
- يجب أن تحتوي على موقف واضح، ليس سرداً محايداً.
- لا ادعاءات نتائج بدون مرجع إثبات.
- لا ذكر أسماء عملاء. لا PII.

### النوع 2 — ألم القطاع (Sector-Pain Post)

**التكرار:** يومي، متناوب بين القطاعات (تأمين، تعليم، لوجستيات، B2B خدمات، توزيع).

**التعريف:** وصف مشكلة تشغيلية نمطية في قطاع محدد — مُستنَدة إلى نمط ملاحَظ، لا إلى عميل بعينه.

**الضوابط:**
- يُسمَّى القطاع، لا الشركة.
- إن استُشهد بأرقام، يُوضَح مستوى الإثبات (تقديري / ملاحَظ / مُتحقَّق).
- ربط بعرض Dealix المحدد في نهاية المنشور.

### النوع 3 — إثبات أو تعلّم (Proof / Learning Post)

**التكرار:** 3–4 مرات / أسبوع.

**التعريف:** مشاركة نتيجة من عمل فعلي (مجهول الهوية)، أو درس من خطأ، أو تحديث منهجية.

**الضوابط:**
- إن كانت الأرقام من Proof Pack، يُذكر مستوى الإثبات صراحةً.
- إن كانت الحالة من عميل حقيقي، تخضع لشروط [`docs/content/CASE_STUDY_SYSTEM_AR.md`](./CASE_STUDY_SYSTEM_AR.md).
- إن كانت تركيبية، يُصنَّف المحتوى "نمط افتراضي آمن".

### النوع 4 — قصة حالة قصيرة (Short Case-Style Post)

**التكرار:** 2–3 مرات / أسبوع.

**التعريف:** سيناريو موجز في تنسيق سياق → ألم → تدخّل → ملاحظة — مجهول الهوية دائماً إلا بموافقة صريحة.

**الضوابط:**
- الحالات غير المؤكَّدة تُصنَّف "حالة افتراضية" صراحةً.
- لا ادعاء نتيجة دون مرجع Proof Pack.
- تنتهي بـ CTA للتشخيص المجاني.

---

## الجدول الأسبوعي — Weekly Cadence (5 أنواع)

### 1 — منشور LinkedIn الطويل (Long-Form LinkedIn Post)

**التوقيت:** مرة أسبوعياً، يفضّل الإثنين أو الأربعاء.

**الهيكل:** خطاف → ألم موثق → تدخل Dealix → دليل → CTA. الحد الأدنى 400 كلمة.

**المرجع:** [`docs/content/LINKEDIN_CADENCE_PLAN.md`](./LINKEDIN_CADENCE_PLAN.md)

### 2 — نص كاروسيل (Carousel Script)

**التوقيت:** مرة أسبوعياً، يفضّل الأربعاء أو الخميس.

**الهيكل:** 5–8 شرائح. الشريحة الأولى: خطاف. الشرائح 2–6: نقاط عملية. الأخيرة: CTA.

**الضابط:** لا شريحة بادعاء نتيجة بدون مستوى إثبات مُوضَح.

### 3 — مسودة دراسة حالة (Case Study Draft)

**التوقيت:** مرة أسبوعياً عند توفر مادة إثبات جديدة.

**الإجراء:** يُحال مباشرة إلى منهجية [`docs/content/CASE_STUDY_SYSTEM_AR.md`](./CASE_STUDY_SYSTEM_AR.md). لا نشر قبل التصنيف المناسب.

### 4 — شرح منتج (Product Explainer)

**التوقيت:** مرة كل أسبوعين.

**المحتوى:** شرح وظيفة واحدة من منهجية Dealix بلغة تشغيلية — Source Passport، Governance Runtime، Proof Score، إلخ.

**الضابط:** لا ادعاء قدرة لم تُختبر على بيانات حقيقية أو تركيبية موثقة.

### 5 — درس المؤسس (Founder Lesson)

**التوقيت:** مرة أسبوعياً، يفضّل السبت.

**المحتوى:** ما رُفض هذا الأسبوع ولماذا، أو ما تعلّمناه من احتكاك موثق في سجل الاحتكاك.

**الضابط:** الرفض يُسمَّى بالشيء المرفوض، لا بالمنافس.

---

## حقول فكرة المحتوى — content_idea Fields

كل فكرة محتوى تُسجَّل بهذه الحقول قبل الصياغة:

```json
{
  "idea_id": "idea_YYYYMMDD_XXX",
  "pillar": "founder_insight | sector_pain | proof_learning | case_style | product_explainer | founder_lesson",
  "sector": "insurance | education | logistics | b2b_services | distribution | cross_sector",
  "pain": "وصف موجز للألم التشغيلي المُعالَج",
  "proof_ref": "مرجع Proof Pack أو null إن كانت تقديرية",
  "offer": "العرض المرتبط (diagnostic / starter / crm_cleanup / ...)",
  "cta": "نص الدعوة للتواصل",
  "status": "draft | approved | published | rejected"
}
```

---

## قاعدة ربط المحتوى — Content Tie-Back Rule

كل قطعة محتوى يجب أن تُجيب على هذه الأسئلة الستة قبل الموافقة:

| السؤال | المطلوب |
|---|---|
| القطاع | أي قطاع يعاني هذا الألم؟ |
| الألم | ما الثغرة التشغيلية تحديداً؟ |
| سير العمل | أي طبقة من Dealix تُعالجها؟ |
| الإثبات | ما مستوى الإثبات (تقديري / ملاحَظ / مُتحقَّق)؟ |
| العرض | ما المنتج المناسب للربط به؟ |
| الدعوة | ما الخطوة التالية للقارئ؟ |

---

## حواجز الامتثال — Compliance Checkpoints

قبل أي موافقة، يتحقق المؤسس من:

- [ ] لا أسماء عملاء حقيقيين دون موافقة صريحة مُسجَّلة
- [ ] لا PII (بريد إلكتروني، هاتف، هوية وطنية)
- [ ] لا ادعاء نتيجة رقمية بدون مرجع Proof Pack
- [ ] لا وعود مبيعات. لا "نضمن". لا "سنرفع إيراداتك X%"
- [ ] لا ذكر لخدمات مرفوضة (كشط، أتمتة LinkedIn، WhatsApp بارد)
- [ ] المحتوى التركيبي مُصنَّف صراحةً

---

## الروابط المرجعية — References

- نظام LinkedIn: [`docs/content/LINKEDIN_SYSTEM_AR.md`](./LINKEDIN_SYSTEM_AR.md)
- نظام دراسة الحالة: [`docs/content/CASE_STUDY_SYSTEM_AR.md`](./CASE_STUDY_SYSTEM_AR.md)
- نظام الإثبات للمحتوى: [`docs/content/PROOF_CONTENT_SYSTEM_AR.md`](./PROOF_CONTENT_SYSTEM_AR.md)
- خطة النشر على LinkedIn: [`docs/content/LINKEDIN_CADENCE_PLAN.md`](./LINKEDIN_CADENCE_PLAN.md)
- المؤشر الرئيسي: [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md)
- قواعد العلامة التجارية: [`docs/brand/BRAND_CONTENT_RULES_AR.md`](../brand/BRAND_CONTENT_RULES_AR.md)
- محرك المحتوى الأسبوعي: [`dealix/marketing_factory/weekly_pack.py`](../../dealix/marketing_factory/weekly_pack.py)
- التقويم التلقائي: [`auto_client_acquisition/gtm_os/content_calendar.py`](../../auto_client_acquisition/gtm_os/content_calendar.py)

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
