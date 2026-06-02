# نظام دراسات الحالة — Case Study System

> كل دراسة حالة تبدأ آمنة ومجهولة الهوية حتى تتوفر موافقة العميل الصريحة المُسجَّلة. لا نشر لأي نتيجة تتجاوز مستوى إثباتها.
>
> روابط: [`auto_client_acquisition/case_study_engine/builder.py`](../../auto_client_acquisition/case_study_engine/builder.py) · [`docs/07_proof_os/`](../07_proof_os/) · [`docs/content/PROOF_CONTENT_SYSTEM_AR.md`](./PROOF_CONTENT_SYSTEM_AR.md) · [`docs/content/CONTENT_ENGINE_AR.md`](./CONTENT_ENGINE_AR.md) · [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md) · [`docs/brand/BRAND_CONTENT_RULES_AR.md`](../brand/BRAND_CONTENT_RULES_AR.md)

---

## المبدأ التشغيلي — Operating Principle

دراسة الحالة في Dealix ليست أداة تسويق — هي أثر تدقيق. تُبنى من Proof Pack مُكتمَل، تخضع للتدقيق، تُصنَّف بمستوى إثبات صريح، ولا تُنشَر حتى تمر بمسار الموافقة الكامل.

**الحكم الأساسي:** إن لم يكن هناك Proof Pack → لا دراسة حالة. إن لم يكن هناك موافقة عميل → دراسة حالة آمنة مجهولة فقط.

---

## تصنيفات الحالات — Case Classifications

### تصنيف 1 — حالة افتراضية / Hypothetical Case-Safe Template

**التعريف:** سيناريو تُمثَّل فيه منهجية Dealix على بيانات تركيبية أو نمط عام، دون ربط بعميل حقيقي.

**متى يُستخدَم:**
- لا يوجد عميل حقيقي بعد
- الحالة مُستوحاة من نمط قطاعي ملاحَظ، لا من عملية محددة
- العميل الحقيقي موجود لكن الموافقة لم تُمنَح بعد

**التصنيف الإلزامي على المستند:** `Hypothetical / Case-Safe Template — نمط افتراضي آمن`

**ما يُسمَح بنشره:** البنية، المنهجية، مستوى الإثبات الاختباري.

**ما لا يُسمَح به:** نسب أي رقم نتيجة لعميل حقيقي، ادعاء أن الحالة وقعت فعلاً.

### تصنيف 2 — حالة مجهولة الهوية / Anonymized Client Case

**التعريف:** حالة من عميل حقيقي، تُزال منها جميع عناصر التعريف، وتُنشَر بعد موافقة المؤسس.

**شروط التصنيف:**
- `evidence_level` في Proof Pack: `customer_observed` أو أعلى
- `pii_redacted: true` في جميع proof events المرتبطة
- موافقة المؤسس مُسجَّلة

**التصنيف الإلزامي:** لا تصنيف إضافي مطلوب، لكن الحالة لا تُنشَر بأي قناة خارجية بدون الشرط الثالث أدناه.

### تصنيف 3 — حالة مؤكَّدة من العميل / Client-Confirmed Case

**التعريف:** حالة من عميل حقيقي، وافق على النشر بتوقيع رقمي عبر `proof_ledger.consent_signature`.

**شروط التصنيف (كلها إلزامية):**
- `evidence_level`: `customer_confirmed` أو `payment_confirmed`
- `consent_status: signed` في سجل الحالة
- `approval_status: approved` من المؤسس
- `pii_redacted: true`

**ما يُسمَح بنشره:** أرقام نتائج مُتحقَّقة مع تنبيه مستوى الإثبات. اسم القطاع (مع موافقة). المنهجية الكاملة.

---

## بنية دراسة الحالة — Case Study Structure

كل دراسة حالة تتبع البنية الخماسية التالية بالترتيب:

### 1. السياق (Context)

ما طبيعة الشركة؟ القطاع، الحجم التقريبي، ما الوضع قبل التدخل؟

**ضابط:** لا تفاصيل تعريفية (اسم، منطقة جغرافية محددة، عدد موظفين دقيق) إلا بموافقة.

### 2. المشكلة (Problem)

ما الثغرة التشغيلية التي أدت إلى طلب التدخل؟ مُوصَفة بلغة تشغيلية، لا بلغة مبيعات.

**ضابط:** الألم يُسمَّى بوضوح. لا تضخيم. "فقدان leads في مرحلة pipeline" أدق من "انهيار قمع المبيعات".

### 3. ما جهّزه Dealix (What Dealix Set Up)

أي طبقات المنهجية تم تفعيلها؟ Source Passport، scoring، draft pack، governance decisions؟

**ضابط:** يُوصَف ما جُهِّز، ليس ما أُرسِل. Dealix لا يُرسِل نيابة عن العميل دون موافقته الصريحة على كل إرسال.

### 4. النتيجة بمستوى إثباتها (Evidenced Result with Tier)

ما الأثر القابل للقياس؟ يُعرَض مع تصنيف صريح:

| مستوى الإثبات | التعريف | كيف يُعرَض |
|---|---|---|
| تقديري (Estimated) | محسوب من نموذج، لم يُتحقَّق | "قدّرنا..." |
| ملاحَظ (Observed) | مُسجَّل في النظام، لم يُؤكَّد من العميل | "لاحظنا..." |
| مُتحقَّق (Verified) | أكّده العميل بتوقيع | "أكّد العميل..." |
| مؤكَّد بالدفع (Payment-Confirmed) | الدفع وقع عند الأثر المُوصَف | "الدفع عند تسليم..." |

### 5. القيد والحدود (Limitation)

ما الذي لا تُثبته هذه الحالة؟ ما الشروط التي يجب توافرها في شركة أخرى لتحصل على نتيجة مشابهة؟

**ضابط:** هذا القسم ليس اختيارياً. كل دراسة حالة بدون قسم القيود لا تمر بوابة الموافقة.

---

## مسار البناء التقني — Technical Build Path

يُنفَّذ عبر [`auto_client_acquisition/case_study_engine/builder.py`](../../auto_client_acquisition/case_study_engine/builder.py):

```
select_publishable(events) → تصفية الأحداث المؤهلة
↓
build_candidate(customer_handle, events, sector) → بناء المسودة + تدقيق المحتوى المحظور
↓
request_quote(candidate_id) → طلب توقيع العميل عبر proof_ledger
↓
approve_candidate(candidate_id, approver) → موافقة نهائية بعد التوقيع
↓
list_library() → الحالات القابلة للنشر
```

**محظورات الكود المُطبَّقة:** الكلمات المحظورة (guaranteed, blast, scraping, cold outreach, نضمن) تُحذَف تلقائياً وتُسجَّل في `safety_findings`.

---

## قاعدة التصنيف الإلزامية — Mandatory Labeling Rule

| التصنيف | النص الإلزامي على المستند |
|---|---|
| حالة افتراضية | `Hypothetical / Case-Safe Template — نمط افتراضي آمن` |
| حالة مجهولة الهوية (داخلي فقط) | `Internal — Not for External Distribution / داخلي فقط` |
| حالة مجهولة مُعتمَدة للنشر | `Anonymized — Approved for Publication / مجهولة — مُعتمَدة للنشر` |
| حالة مؤكَّدة من العميل | `Client-Confirmed — Level: [Verified/Payment-Confirmed]` |

---

## الروابط المرجعية — References

- محرك البناء: [`auto_client_acquisition/case_study_engine/builder.py`](../../auto_client_acquisition/case_study_engine/builder.py)
- OS الإثبات: [`docs/07_proof_os/PROOF_OS.md`](../07_proof_os/PROOF_OS.md)
- معيار Proof Pack: [`docs/07_proof_os/PROOF_PACK_STANDARD.md`](../07_proof_os/PROOF_PACK_STANDARD.md)
- الملخص الآمن للحالة: [`docs/07_proof_os/CASE_SAFE_SUMMARY.md`](../07_proof_os/CASE_SAFE_SUMMARY.md)
- درجة الإثبات: [`docs/07_proof_os/PROOF_SCORE.md`](../07_proof_os/PROOF_SCORE.md)
- تحويل الإثبات للمحتوى: [`docs/content/PROOF_CONTENT_SYSTEM_AR.md`](./PROOF_CONTENT_SYSTEM_AR.md)
- محرك المحتوى: [`docs/content/CONTENT_ENGINE_AR.md`](./CONTENT_ENGINE_AR.md)
- المؤشر الرئيسي: [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md)
- سياسة الادعاءات: [`docs/05_governance_os/CLAIM_SAFETY.md`](../05_governance_os/CLAIM_SAFETY.md)

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
