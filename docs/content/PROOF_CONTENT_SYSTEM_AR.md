# Proof Content System — نظام تحويل الإثبات إلى محتوى

> جزء من: Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
>
> **الجمهور:** المؤسس + فريق المحتوى.
> **الفكرة:** حزمة الإثبات (Proof Pack) ليست أرشيفاً داخلياً فقط؛ هي مادة محتوى. لكن ليس كل دليل قابلاً للنشر. هذا المستند يصنّف الأدلة من L0 إلى L5، ويحدّد ما يُنشَر علناً وما يبقى داخلياً.
> مراجع: [docs/content/CASE_STUDY_SYSTEM_AR.md](./CASE_STUDY_SYSTEM_AR.md) · [docs/content/CONTENT_ENGINE_AR.md](./CONTENT_ENGINE_AR.md) · [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) · [docs/07_proof_os/CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md)

---

## المبدأ — The principle

الإثبات هو مصدر المحتوى الأقوى لأنه مبنيٌّ على عمل فعلي، لا على ادعاء. لكن قوة الدليل تتفاوت: درجة جودة محسوبة على بيانات تركيبية تختلف عن نتيجة عميل مُؤكَّدة موثَّقة بإذن نشر. الخلط بينهما يكسر الثقة. لذلك نصنّف كل دليل بمستوى، ولا ننشر دليلاً يفوق مستوى ما يُسمح بنشره.

القاعدة الثابتة: القيمة التقديرية ليست قيمة مُتحقَّقة. ما لم يُؤكَّد بإذن ومصدر، يبقى تقديراً مُعلَّماً أو يبقى داخلياً.

Proof is the strongest content source because it rests on real work. But evidence strength varies; mixing a synthetic-data score with a permission-backed client result breaks trust. We label every piece of evidence with a level and never publish above the permitted level.

---

## مستويات الأدلة L0–L5 — Evidence levels

| المستوى / Level | الوصف / Description | مثال / Example | النشر / Publishability |
|---|---|---|---|
| **L0** | منهجية وبنية، بلا أرقام | «حزمة إثبات من 14 قسماً» | عام / Public |
| **L1** | درجة محسوبة على بيانات تركيبية أو داخلية | «اكتمال 72٪ على بيانات عرض» | عام مع تعليم / Public, labeled |
| **L2** | نمط آمن مُجهَّل من عمل مُسلَّم | «340 حساب → 10 أولويات (نمط آمن)» | عام مع تعليم / Public, labeled |
| **L3** | تقدير منهجي للقيمة من حالة حقيقية مُجهَّلة | «وفّر ~32 ساعة (تقديري)» | عام مع تعليم صارم / Public, strict label |
| **L4** | نتيجة عميل حقيقية بلا إذن نشر | درجة جودة فعلية لعميل مُسمّى داخلياً | داخلي فقط / Internal only |
| **L5** | نتيجة عميل مُؤكَّدة بإذن نشر مُوقَّع | حالة مُسمّاة بعد توقيع العميل | عام بالاسم / Public, named |

L0–L3 قابلة للنشر العام بشرط التعليم الواضح («نمط آمن»، «تقديري»). L4 داخلي لا يُنشَر مطلقاً قبل أن يصبح L5. L5 وحده يجوز فيه ذكر الاسم.

L0–L3 are publishable with clear labels. L4 is internal and is never published until it becomes L5. Only L5 may carry a customer name.

---

## ما هو قابل للنشر مقابل ما هو داخلي — Publishable vs internal

**قابل للنشر / Publishable (L0–L3):**
- بنية حزمة الإثبات ومنهجيتها.
- درجات محسوبة على بيانات تركيبية أو عرض، مع تعليم.
- أنماط آمنة مُجهَّلة (قبل/بعد بلا اسم).
- تقديرات منهجية للوقت أو الجودة، مُعلَّمة «تقديرية».

**داخلي فقط / Internal only (L4 وما يحمل بيانات حساسة):**
- نتائج عملاء حقيقيين بلا إذن نشر.
- أي مقياس سرّي أو رقم إيراد.
- أي بيانات شخصية (بريد، هاتف، اسم فرد، هوية).
- محتوى جواز مصدر يخصّ عميلاً.

القاعدة العملية: إن لم تستطع أن تُسمّي مستوى الدليل بثقة، فهو داخلي حتى تتأكد.

Practical rule: if you cannot confidently name the evidence level, it is internal until verified.

---

## مسار التحويل — The conversion path

1. **استخراج من الحزمة** — اختيار رقم أو نمط من حزمة إثبات مُسلَّمة.
2. **تصنيف المستوى** — تحديد L0–L5 بدقة.
3. **بوابة المستوى** — إن كان L4، يتوقّف المسار: داخلي. إن كان L0–L3، يكمل بالتعليم المناسب.
4. **الصياغة** — تحويل الدليل إلى قطعة محتوى عبر [CONTENT_ENGINE_AR.md](./CONTENT_ENGINE_AR.md)، مع العناصر الستة.
5. **التعليم** — إضافة الوسم الصريح: «نمط آمن» / «تقديري» / «بيانات تركيبية».
6. **اعتماد المؤسس** — قبل النشر، مقابل اللاءات ومقابل مطابقة المستوى للنشر.

أي محاولة لنشر L4 بوصفه L5 (نتيجة عميل بلا إذن) تُعدّ انتهاكاً، وتُردّ عند البوابة.

Any attempt to publish L4 as if it were L5 (a client result without permission) is a violation and is rejected at the gate.

---

## الربط بدراسات الحالة — Link to case studies

دراسات الحالة في [CASE_STUDY_SYSTEM_AR.md](./CASE_STUDY_SYSTEM_AR.md) هي أكبر مُستهلك لهذا النظام: كل رقم فيها يجب أن يكون L0–L3 ما دامت قالباً آمناً، ولا يرتقي إلى L5 (ذكر الاسم) إلا بإذن نشر مُوقَّع. ملخص الحالة الآمن في [CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md) ومعيار الحزمة في [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) هما المرجعان الرسميان للبنية.

الخطوة التالية الافتراضية لأي قطعة إثبات منشورة: ربطها بعرض من السلّم — تشخيص مجاني (0) ثم سبرنت ذكاء الإيرادات (499).

Case studies are the largest consumer of this system: every number stays L0–L3 while the case is a safe template, rising to L5 only with signed permission. The default next step for any published proof piece is a ladder offer.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.**
