# Partner Workspace — مساحة الشريك (White-label)

> المرجع: §33 من المواصفة الأصلية.

---

## ما هذه المساحة؟

Partner Workspace هي السطح الذي يستخدمه شريك Dealix (وكالة، Integrator، استشاري) لتقديم خدمات Dealix لعملائه **تحت علامة الشريك**. الشريك لا يرى نواة Dealix، ولا يرى عملاء شركاء آخرين، ولا يرى Sovereign — لكنه يستطيع تشغيل خدمات Dealix بفعالية كأنّها له، ضمن حدود واضحة.

الفكرة الجوهرية: **Dealix كـ"رأسمال تقني" للشركاء**، لا كأداة فضفاضة.

---

## الـ 8 صفحات للشريك

| # | الصفحة | الغرض |
|---|---|---|
| 1 | **Brand Setup** | إعداد العلامة (شعار، ألوان، اسم النطاق) — يظهر للعميل النهائي |
| 2 | **Client Roster** | قائمة عملاء الشريك (هو يديرها، Dealix لا تتدخل فيها) |
| 3 | **Service Catalog** | الخدمات المتاحة للشريك (subset من عروض Dealix) |
| 4 | **Active Engagements** | الـ Engagements الجارية لكل عميل من عملاء الشريك |
| 5 | **Evidence (per client)** | حِزَم الأدلة المُولَّدة لعملاء الشريك (راجع [EVIDENCE_PACK_AR.md](EVIDENCE_PACK_AR.md)) |
| 6 | **Reports** | تقارير القيمة الشهرية لكل عميل (بعلامة الشريك) |
| 7 | **Settlement** | حساب العمولات/الإيرادات بين الشريك و Dealix |
| 8 | **Support / Escalation** | قناة دعم محدودة + مسار تصعيد للحالات الحرجة |

---

## الـ 5 قواعد للشريك

1. **العلامة للشريك، النواة لـ Dealix.** الشريك يضع وجهه، Dealix تضمن الجودة الداخلية. لا يستطيع الشريك تعديل المنطق التشغيلي للوكلاء أو الأدوات.
2. **عميل الشريك = عميل الشريك.** Dealix لا تتواصل مباشرة مع عميل الشريك دون إذن خطي. كل تواصل يمرّ عبر الشريك.
3. **بيانات معزولة بالكامل.** بيانات عملاء الشريك لا تُستخدم لأي تدريب نموذج أو تحليل عبر-عملاء دون موافقة صريحة.
4. **بوابات Dealix لا تُتجاوَز.** كل رسالة، كل عرض، كل تشغيل وكيل يمرّ ببوابات الجودة (راجع [QUALITY_GATES_AR.md](QUALITY_GATES_AR.md)) حتى لو طلب الشريك تجاوزها.
5. **Kill Switch يصل للشريك.** إذا أصدر Sovereign قرار Kill على أداة/وكيل/قطاع، يُنفَّذ تلقائيًا في مساحة الشريك دون استشارته (مع إخطار فوري وشرح).

---

## ما لا يُكشَف للشريك أبدًا

- **Sovereign Layer بكامله** — Command Page، Money Command، Approvals، Strategic Decisions، Decision Journal، Capital Allocation، Kill Switch، Agent Control، Tool Control.
- **بيانات عملاء شركاء آخرين** — حتى الوجود لا يُؤكَّد.
- **الاستراتيجية الداخلية لـ Dealix** — roadmap، تسعير داخلي، اقتصاديات الوحدة، خطط Scale/Kill.
- **Tool Registry internals** — أسماء الأدوات، إعدادات الـ guardrails، تكلفة الاستدعاء، logs.
- **Agent internals** — أسماء النماذج، prompts، أوزان، logs تفصيلية. الشريك يرى النتيجة لا المحرك.

---

## نموذج الاتفاق التشغيلي

الشريك يدخل علاقة Dealix عبر اتفاق يحدّد:

- نطاق الخدمات المتاحة له (subset من Service Catalog الكامل).
- حدّ السعر الأدنى الذي يستطيع تقديم الخدمة به (لحماية القيمة).
- التزامات Trust (PDPL، سرية، عدم تجاوز بوابات الجودة).
- آلية الـ Settlement (نسبة، شهرية، تسوية ربع سنوية).
- شروط الإنهاء + بقاء أدلة العملاء بحوزة العميل النهائي حتى بعد الإنهاء.

---

## كيف يبدو يوم عمل في Partner Workspace

| الوقت | الفعل النموذجي |
|---|---|
| الصباح | فحص Active Engagements + Evidence الجاهز للإرسال |
| منتصف اليوم | مراجعة تقارير القيمة الشهرية قبل إرسالها للعملاء |
| بعد الظهر | الرد على Support tickets داخل الشريك، تصعيد عند الحاجة |
| نهاية اليوم | فحص Settlement + الفواتير المعلَّقة |

كل هذه الأفعال تُسجَّل كأحداث في bus المركزي، ويراها Sovereign على مستوى مُجمَّع (لا يرى محتوى تفصيليًا لعميل الشريك).

---

## English Summary

- The Partner Workspace lets agencies and integrators deliver Dealix services under their own brand across 8 pages: Brand Setup, Client Roster, Service Catalog, Active Engagements, Evidence per client, Reports, Settlement, and Support.
- Five non-negotiable partner rules: brand belongs to partner, partner's customer is partner's customer, data is fully isolated, Dealix quality gates cannot be bypassed, and Sovereign kill commands propagate automatically.
- Five things are never exposed: the Sovereign layer, other partners' customers, Dealix internal strategy, tool registry internals, and agent internals.
- The relationship is governed by a written agreement covering scope, minimum pricing, trust obligations, settlement, and termination/data-retention terms.
- Partner activities are logged as events; Sovereign sees aggregates, never partner-customer content detail.
