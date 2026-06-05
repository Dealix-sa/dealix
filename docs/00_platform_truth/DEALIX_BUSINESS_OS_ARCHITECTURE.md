# Dealix Business OS Architecture — بنية نظام تشغيل الأعمال

> هذه الوثيقة تصف **كيف** تتركّب Dealix داخليًا: الأنظمة الأربعة عشر، كيف تتدفّق البيانات بينها، والبنية التقنية التي تشغّلها.
> This document describes **how** Dealix is assembled: the 14 Operating Systems, how data flows between them, and the technical stack that runs them.
>
> المصدر الأعلى / Upstream truth: `PLATFORM_SOURCE_OF_TRUTH.md`. عند أي تعارض، وثيقة المصدر تكسب.

الحالة / Status: **LIVE (canonical architecture)** · آخر تحديث / Last updated: 2026-06-05

---

## 1. المبدأ المعماري / The Architectural Principle

Dealix ليست 14 منتجًا منفصلًا. هي **نظام واحد** بأربع عشرة طبقة، يربطها ناقل واحد: الحدث له دليل، والدليل يُغذّي القرار، والقرار يمرّ ببوّابة، والبوّابة تُسجَّل.

Dealix is not 14 separate products. It is **one system** with fourteen layers, joined by a single spine: every event carries evidence, evidence feeds a decision, the decision passes a gate, and the gate is logged.

ثلاث قواعد معمارية ثابتة / Three fixed architectural laws:

1. **الحوكمة تحكم الكل / Governance gates everything.** لا فعل خارجي يخرج بلا مرور على Governance OS.
2. **الدليل يسبق الادّعاء / Proof precedes claim.** لا مخرَج يُعرض على العميل بلا أصل في Proof OS / Data OS.
3. **المعرفة تتراكم / Knowledge compounds.** كل تسليم يُنتج قالبًا يُسرّع التسليم التالي عبر Knowledge OS.

---

## 2. شجرة الأنظمة الأربعة عشر / The 14-OS Tree

```
Dealix Business OS
│
├── 01 Command OS ........... غرفة القيادة — يقرأ الكل، يقرّر القادم
│
├── طبقة الإدخال / Intelligence Layer
│   ├── 02 Market Intelligence OS ... فهم السوق + الشركات المستهدفة
│   └── 09 Data OS ............ المصدر، الجودة، الخصوصية (PDPL)
│
├── طبقة القيمة / Value Layer
│   ├── 03 Revenue OS ......... خريطة الإيراد
│   ├── 05 Delivery OS ........ تنفيذ العمل
│   ├── 06 Client OS .......... صحة وتوسّع ما بعد البيع
│   ├── 07 Support OS ......... الطلبات والمشكلات
│   └── 08 Finance OS ......... الفواتير والربحية
│
├── طبقة الإثبات / Proof Layer
│   └── 04 Proof OS ........... تحويل العمل إلى دليل قابل للعرض
│
├── طبقة الضبط / Control Layer
│   ├── 10 Governance OS ...... البوّابات والموافقات
│   ├── 11 Knowledge OS ....... القوالب والأصول المتراكمة
│   └── 12 Agent OS ........... الوكلاء بعقد واضح
│
└── طبقة التوسّع / Expansion Layer
    ├── 13 Partner OS ......... الشركاء والقنوات
    └── 14 Academy OS ......... التدريب
```

> وسوم الحالة الحقيقية لكل نظام في / Real status labels per OS: `MODULE_STATUS_MAP.md`. أغلب طبقات التوسّع اليوم `FUTURE`/`DOCS_ONLY`.

---

## 3. تدفّق البيانات بين الأنظمة / Data Flows Between Systems

الأنظمة لا تعمل منعزلة؛ تمرّر قيمة في حلقة مغلقة:

The systems are not isolated; they pass value in a closed loop:

| المصدر / From | الوجهة / To | ما يُمرَّر / What flows |
|---|---|---|
| **Market Intelligence OS** | Revenue OS + Roadmap | شركات مستهدفة مع دليل → تغذّي خريطة الإيراد وأولويات البناء. Sourced targets feed the revenue map and build priorities. |
| **Delivery OS** | Proof OS | العمل المنجَز → يتحوّل إلى أحداث دليل قابلة للعرض. Delivered work becomes showable proof events. |
| **Proof OS** | Market Intelligence + Knowledge | الدليل والحالات → محتوى وقوالب وتموضع لاستهداف أفضل. Proof and cases feed content, templates, and sharper targeting. |
| **Governance OS** | الكل / Everything | بوّابة موافقة على كل فعل خارجي أو حسّاس. An approval gate on every external or sensitive action. |
| **Knowledge OS** | الكل / Everything | قوالب متراكمة تُقصّر زمن كل تسليم لاحق. Compounding templates that cut the time of every later delivery. |
| **Data OS** | Market Intelligence + Proof | بيانات بمصدر وجودة موسومة تمنع الدليل المزيّف. Provenanced, quality-scored data that prevents fake proof. |
| **Finance OS** | Command OS | الربحية لكل عميل → تظهر في قرار المؤسس القادم. Per-client profitability surfaces in the founder's next decision. |

الحلقة المختصرة / The short loop:
**Intelligence → Revenue → Delivery → Proof → (back to) Intelligence**، والكل تحت **Governance**، ومتسارع بـ **Knowledge**.

---

## 4. البنية التقنية / The Technical Stack

> صدق: الكثير من هذه الطبقة موجود فعلًا في الريبو (FastAPI، 120+ راوتر، سلسلة تجارية diagnostic→pilot→proof→payment→upsell، Moyasar sandbox، تكامل PDPL). الإطار "OS" جديد، لكن الكود تحته حقيقي.

| الطبقة / Layer | اليوم / Today | لاحقًا / Later |
|---|---|---|
| **Frontend** | React/Vite + Next.js الموجود (واجهات داخلية + عميل). | توحيد على واجهة واحدة محكومة. |
| **Backend** | FastAPI — 120+ راوتر، سلسلة تجارية كاملة. | تجزئة خدمات حسب الـ OS. |
| **Data** | JSONL ملفات + مجلّدات تسليم. | ترحيل إلى Postgres مع بقاء الـ JSONL كسجلّ. |
| **Agents** | LLM Router (Claude / OpenAI / DeepSeek / local). | عقود Agent OS كاملة + اختبارات لكل وكيل. |
| **Search** | تجريد مزوّد (provider abstraction). | تعدّد مزوّدين مع احترام robots.txt والشروط. |
| **Payments** | Moyasar (sandbox). | إنتاج مع تسوية وربط Finance OS. |
| **Workflows** | GitHub Actions. | مشغّلات مجدولة + بوّابات حوكمة آلية. |
| **Docs** | Markdown كمصدر حقيقة (`docs/`). | يبقى المصدر؛ يُولّد منه الـ UI. |
| **Privacy** | تكامل PDPL، تصنيف PII، تنقيح. | تدقيق دوري + سجلّ احتفاظ. |

القاعدة الذهبية / Golden rule: **الوثائق هي مصدر الحقيقة، لا الكود.** الكود ينفّذ ما تقوله الوثيقة؛ إن اختلفا، تُصحَّح الوثيقة عمدًا أو يُصحَّح الكود.

---

## 5. بوّابة النماذج — LLM Gateway Routing / جدول التوجيه

كل استدعاء نموذج يمرّ ببوّابة واحدة تختار النموذج حسب المهمّة والمخاطرة والعربية والكلفة. تفصيل أعمق في `docs/06_llm_gateway/`.

| المهمّة / Task | الوجهة / Route to | السبب / Why |
|---|---|---|
| تصنيف سريع / Fast classification | نموذج رخيص / cheap model | حجم كبير، قرار بسيط، كلفة دنيا. |
| صياغة عربية / Arabic drafting | نموذج عربي قوي / strong Arabic model | جودة لغة عربية أولًا. |
| تفكير استراتيجي / Strategic reasoning | نموذج ممتاز / premium model | قرارات إيراد وقيادة. |
| كود / Code | نموذج برمجي / coding model | دقّة بنيوية. |
| بديل / Fallback | OpenRouter | استمرارية عند تعطّل مزوّد. |
| مسودّات محلية / Local drafts | Ollama (local) | خصوصية وكلفة صفرية للمسودّات. |

قواعد البوّابة الإلزامية / Mandatory gateway rules:
- **PII-aware:** أي حمولة فيها PII تُنقّح قبل الإرسال لأي مزوّد خارجي (Data OS + Redaction).
- **لا تدريب على بيانات العملاء / No training on customer data.**
- **سجلّ تشغيل / Run ledger:** كل استدعاء يُسجَّل (النموذج، الكلفة، المهمّة) — `docs/06_llm_gateway/AI_RUN_LEDGER.md`.

---

## 6. عقد Agent OS / The Agent Contract Shape

لا يُشغَّل أي وكيل بلا عقد مكتمل. شكل العقد:

```json
{
  "name": "string — اسم الوكيل",
  "mission": "string — مهمّة واحدة واضحة",
  "inputs": ["مدخلات محدّدة المصدر"],
  "outputs": ["مخرجات بصيغة معروفة"],
  "allowed_tools": ["الأدوات المسموح استدعاؤها فقط"],
  "forbidden_actions": ["أفعال ممنوعة صراحة — مثل الإرسال الخارجي"],
  "approval_class": "A0 | A1 | A2 | A3 | A4 | A5",
  "logs": "أين تُكتب آثار التشغيل",
  "tests": ["اختبارات يجب أن تمرّ قبل التشغيل"],
  "owner": "المسؤول البشري",
  "rollback": "كيف نوقف ونعكس أثر الوكيل"
}
```

أي وكيل بلا `owner`، أو بلا `tests`، أو بلا `rollback` — **لا يُشغَّل**.

---

## 7. فئات الموافقة / Approval Classes A0–A5

كل فعل آليّ يُصنَّف بفئة موافقة. **A2 فأعلى تتطلّب موافقة المؤسس.**

| الفئة / Class | المعنى / Meaning | يتطلّب / Requires |
|---|---|---|
| **A0** | قراءة فقط، داخلي بحت. Read-only, internal. | لا شيء / none. |
| **A1** | كتابة داخلية (مسودّة، ملف داخلي). Internal write. | تسجيل تلقائي / auto-log. |
| **A2** | مخرَج يواجه العميل (مسودّة تُرسَل). Customer-facing output. | **موافقة المؤسس / founder approval.** |
| **A3** | فعل خارجي (رسالة، نشر). External action. | **موافقة المؤسس + سجلّ.** |
| **A4** | مالي (فاتورة، دفع، تسعير). Financial action. | **موافقة المؤسس + سجلّ + مراجعة.** |
| **A5** | يمسّ بيانات/خصوصية حسّاسة. Sensitive data/privacy. | **موافقة المؤسس + مراجعة PDPL + سجلّ.** |

> الربط بالقواعد الصارمة: A2–A5 هي التجسيد التقني لقاعدة "لا فعل خارجي يواجه العميل بلا موافقة المؤسس". تفصيل في `docs/05_governance_os/`.

---

## روابط مرجعية / Cross-links

- المصدر الكامل / Source of truth: `PLATFORM_SOURCE_OF_TRUTH.md`
- سلّم العروض / Offer ladder: `PRODUCT_FAMILY_MAP.md`
- حالة الوحدات / Module status: `MODULE_STATUS_MAP.md`
- برج التحكّم / Control tower: `LAUNCH_CONTROL_TOWER.md`
- بوّابة النماذج / LLM gateway: `../06_llm_gateway/LLM_GATEWAY.md`
- الحوكمة / Governance: `../05_governance_os/GOVERNANCE_OS.md`

---

*القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.*
