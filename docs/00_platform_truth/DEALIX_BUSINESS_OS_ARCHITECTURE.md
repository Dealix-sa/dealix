# Dealix Business OS Architecture — معمارية نظام تشغيل الأعمال

This document describes how the 12 systems of Dealix are layered, what each one does in a single line, and the four outcomes every system must serve. For the identity behind it, see [`PLATFORM_SOURCE_OF_TRUTH.md`](./PLATFORM_SOURCE_OF_TRUTH.md). For what is sellable today, see [`MODULE_STATUS_MAP.md`](./MODULE_STATUS_MAP.md).

يصف هذا المستند كيف تترتّب الأنظمة الاثنا عشر في Dealix طبقياً، وما يفعله كل نظام في سطر واحد، والنتائج الأربع التي يجب أن يخدمها كل نظام. لهوية المنصّة راجع [`PLATFORM_SOURCE_OF_TRUTH.md`](./PLATFORM_SOURCE_OF_TRUTH.md). ولما هو قابل للبيع اليوم راجع [`MODULE_STATUS_MAP.md`](./MODULE_STATUS_MAP.md).

---

## 1. The four outcomes — النتائج الأربع

Every system, every feature, and every line of work must serve one of four outcomes. If it serves none, it is not built.

كل نظام وكل ميزة وكل بند عمل يجب أن يخدم إحدى أربع نتائج. وإن لم يخدم أياً منها، فلا يُبنى.

1. Bring a real opportunity. إحضار فرصة حقيقية.
2. Convert it to a customer. تحويلها إلى عميل.
3. Deliver proven value. تسليم قيمة مُثبتة.
4. Turn proof into new growth. تحويل الإثبات إلى نمو جديد.

---

## 2. Layered diagram — المخطط الطبقي

```
+----------------------------------------------------------------+
|  COMMAND OS  —  decides & directs / يقرّر ويوجّه                 |
+----------------------------------------------------------------+
|  OUTCOME LAYER  —  the four outcomes / طبقة النتائج             |
|                                                                |
|  [1] Opportunity   [2] Customer   [3] Proven value   [4] Growth|
|   Market Intel  ->  Revenue   ->  Delivery + Proof  ->  Client |
|        OS            OS              OS      OS          OS     |
|                                                  Partner/Academy|
|                                                       OS        |
+----------------------------------------------------------------+
|  SUPPORT LAYER  —  Support OS  ·  Finance OS                    |
+----------------------------------------------------------------+
|  FOUNDATION  —  DATA OS  ·  GOVERNANCE OS  (under everything)  |
|  consent · quality · retention · approval · identity · claims  |
+----------------------------------------------------------------+
```

Read it top to bottom: Command OS decides; the outcome layer runs the loop left to right; Support and Finance keep the work serviced and paid; Data and Governance sit under all of it so nothing moves without consent, identity, and approval.

اقرأه من الأعلى إلى الأسفل: نظام القيادة يقرّر؛ وطبقة النتائج تُشغّل الحلقة من اليسار إلى اليمين؛ والدعم والمالية يبقيان العمل مخدوماً ومدفوعاً؛ والبيانات والحوكمة تجلسان تحت كل ذلك حتى لا يتحرّك شيء دون موافقة وهوية واعتماد.

---

## 3. Each system in one line — كل نظام في سطر

| System | One-line role | الدور في سطر |
|---|---|---|
| Command OS | Reads the state, decides the next move, directs the day | يقرأ الحالة، يقرّر الحركة التالية، يوجّه اليوم |
| Market Intelligence OS | Finds, scores, and shortlists real opportunities | يجد ويسجّل ويختصر الفرص الحقيقية |
| Revenue OS | Maps an opportunity to a path toward a paying customer | يرسم الفرصة إلى مسار نحو عميل يدفع |
| Proof OS | Turns delivered work into sourced, reusable evidence | يحوّل العمل المُسلَّم إلى دليل مُوثَّق قابل لإعادة الاستخدام |
| Delivery OS | Runs the engagement to a defined, on-time result | يُشغّل الارتباط إلى نتيجة محدّدة في وقتها |
| Client OS | Holds client memory, rhythm, and renewal | يحفظ ذاكرة العميل وإيقاعه وتجديده |
| Support OS | Answers from sourced knowledge, never invents | يجيب من معرفة مُوثَّقة ولا يختلق |
| Finance OS | Prices, invoices, and tracks money (ZATCA-aware) | يسعّر ويفوتر ويتتبّع المال (واعٍ بزاتكا) |
| Data OS | Governs consent, quality, retention, and deletion | يحكم الموافقة والجودة والاحتفاظ والحذف |
| Governance OS | Enforces approval, identity, claims, and no-spam | يفرض الموافقة والهوية والادّعاءات ومنع الإزعاج |
| Partner OS | Extends delivery through approved partners | يوسّع التسليم عبر شركاء معتمدين |
| Academy OS | Teaches operators to run the loop | يعلّم المشغّلين إدارة الحلقة |

Statuses for each of these are binding only in [`MODULE_STATUS_MAP.md`](./MODULE_STATUS_MAP.md); most are BETA, INTERNAL, or FUTURE today.

حالات كل نظام مُلزِمة فقط في [`MODULE_STATUS_MAP.md`](./MODULE_STATUS_MAP.md)؛ ومعظمها اليوم في BETA أو INTERNAL أو FUTURE.

---

## 4. How the loop runs across the systems — كيف تجري الحلقة عبر الأنظمة

The operating rule holds at every step: AI explores and recommends, deterministic workflows execute, and a human approves any critical external commitment.

تبقى قاعدة التشغيل في كل خطوة: الذكاء الاصطناعي يستكشف ويوصي، والتدفقات الحتمية تنفّذ، والبشر يعتمدون أي التزام خارجي حرج.

- **Outcome 1 — opportunity:** Market Intelligence OS researches and scores; the founder shortlists. النتيجة الأولى — الفرصة: استخبارات السوق تبحث وتسجّل؛ والمؤسس يختصر.
- **Outcome 2 — customer:** Revenue OS maps the path; outreach stays manual and approved. النتيجة الثانية — العميل: الإيراد يرسم المسار؛ والتواصل يبقى يدوياً ومعتمداً.
- **Outcome 3 — proven value:** Delivery OS produces the result; Proof OS packages it as evidence. النتيجة الثالثة — قيمة مُثبتة: التسليم ينتج النتيجة؛ والإثبات يحزّمها كدليل.
- **Outcome 4 — growth:** Client OS keeps the rhythm; Partner and Academy OS scale it later. النتيجة الرابعة — النمو: العميل يحفظ الإيقاع؛ والشركاء والأكاديمية يوسّعانه لاحقاً.

---

## 5. Why data and governance sit underneath — لماذا تجلس البيانات والحوكمة في الأساس

The foundation layer is not optional plumbing; it is the product's trust surface. Data OS enforces consent, retention windows, and deletion on request. Governance OS enforces the 11 non-negotiables in practice: no agent without identity, no external action without approval, no claim without a source. In a market where privacy and retention clarity is scarce — one post-PDPL study found only about 31% of sampled Saudi e-commerce sites disclosed all four checked privacy elements — putting these controls beneath every system is how Dealix earns trust as a differentiator rather than a disclaimer.

طبقة الأساس ليست سباكة اختيارية؛ بل هي سطح الثقة في المنتج. نظام البيانات يفرض الموافقة ونوافذ الاحتفاظ والحذف عند الطلب. ونظام الحوكمة يفرض البنود الأحد عشر عملياً: لا وكيل بلا هوية، ولا فعل خارجي بلا موافقة، ولا ادّعاء بلا مصدر. في سوق يندر فيه وضوح الخصوصية والاحتفاظ — وجدت دراسة بعد نظام حماية البيانات أن نحو 31% فقط من المواقع المعاينة أفصحت عن العناصر الأربعة المفحوصة — فإن وضع هذه الضوابط تحت كل نظام هو كيف تكسب Dealix الثقة كميزة لا كتنصّل.

The offer family that this architecture produces is mapped in [`PRODUCT_FAMILY_MAP.md`](./PRODUCT_FAMILY_MAP.md), with prices bound in [`../01_go_to_market/PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md).

عائلة العروض التي تنتجها هذه المعمارية موضّحة في [`PRODUCT_FAMILY_MAP.md`](./PRODUCT_FAMILY_MAP.md)، بأسعار مربوطة في [`../01_go_to_market/PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
