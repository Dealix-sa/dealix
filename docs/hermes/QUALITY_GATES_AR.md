# Quality Gates — بوابات الجودة

> المرجع: §41 من المواصفة الأصلية.

---

## ما هي بوابة الجودة؟

بوابة جودة = قائمة فحص ملزمة يجب اجتيازها قبل أن يُسمَح بإجراء معيّن. ليست توصية، ليست check-list شكلية. **إن لم تمر، لا يحدث الإجراء.** Hermes هو من يفرض البوابة قبل الـ dispatch (راجع [HERMES_ORCHESTRATOR_AR.md](HERMES_ORCHESTRATOR_AR.md)).

في Dealix، 4 بوابات أساسية:

1. أي **رسالة خارجية**.
2. أي **مقترح**.
3. أي **تشغيل وكيل**.
4. أي **استدعاء أداة**.

---

## 1) بوابة: أي رسالة خارجية

تنطبق على: بريد إلكتروني، رسالة WhatsApp ضمن الحدود المسموحة، مكالمة هاتفية مُؤتمتة، منشور باسم العميل، أي محتوى يخرج خارج Dealix.

- [ ] **المُرسِل معلوم وموثَّق** — لا "مجهول" ولا "تلقائي تمامًا".
- [ ] **المُستقبِل أعطى إذنًا قانونيًا** (PDPL-aware؛ راجع `docs/04_data_os/PII_CLASSIFICATION.md` و`docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md`).
- [ ] **القناة معتمدة** (لا cold WhatsApp، لا scraping، لا LinkedIn automation).
- [ ] **المحتوى مُراجَع بشريًا** أو ضمن قالب مُعتمد مسبقًا.
- [ ] **لا ادعاءات أرقام** غير مدعومة بدليل في Evidence Pack.
- [ ] **اللغة وفق دليل الأسلوب** (تنفيذي، بلا حشو تسويقي).
- [ ] **تذييل القيمة موجود**: "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value" حيث يكون السياق ماليًا.
- [ ] **رابط Opt-out** متاح حيث يلزم.
- [ ] **سجل الإرسال موثَّق** كحدث.

---

## 2) بوابة: أي مقترح

تنطبق على: Diagnostic proposal, Sprint proposal, Retainer proposal, شراكة، عرض Marketplace.

- [ ] **اسم العميل/الشريك مؤكَّد** (لا فرص وهمية، لا بيانات افتراضية).
- [ ] **ICP fit موثَّق** في opportunity.qualified event.
- [ ] **النطاق محدد بدقّة** — قائمة مُسلَّمات + استثناءات صريحة.
- [ ] **السعر ضمن نطاق Dealix المُعتمد** (راجع `docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md`).
- [ ] **مُسلَّمات قابلة للتدقيق** — كل مُسلَّم له تعريف "تم" واضح.
- [ ] **مقاييس النجاح محدّدة** (Time-to-Proof, KPI specific).
- [ ] **بنود PDPL/قنوات معتمدة** مذكورة صراحة.
- [ ] **شروط الإنهاء + ملكية البيانات** بعد الإنهاء واضحة.
- [ ] **توقيع داخلي قبل الإرسال** من Lead المسؤول.
- [ ] **لا ضمانات أرقام** — "فرص مُثبتة بأدلة" لا "نضمن مبيعات".

---

## 3) بوابة: أي تشغيل وكيل

تنطبق على: كل استدعاء agent.run في Dealix (وكيل تأهيل، وكيل تواصل، وكيل تحليل…).

- [ ] **الوكيل مُسجَّل في Agent Registry** بإصدار محدَّد.
- [ ] **الصلاحية L0–L6 معروفة** ومناسبة للإجراء (راجع [RISK_MODEL_AR.md](RISK_MODEL_AR.md)).
- [ ] **حد التكلفة لكل تشغيل** معرَّف ولم يُتجاوَز.
- [ ] **حد المعدّل (rate limit)** غير مُتجاوَز.
- [ ] **المدخلات مُصنَّفة من ناحية حساسية البيانات** (PII/None).
- [ ] **الأدوات التي سيستدعيها الوكيل** مُسموح بها في Tool Registry.
- [ ] **Pre-execution evidence مُسجَّل** (النية، المدخلات، السياق).
- [ ] **Kill Switch قابل للوصول** خلال التشغيل.
- [ ] **Post-execution evidence مطلوب** (المخرَجات، التكلفة، النتيجة).
- [ ] **أي خرق سياسة → execution.failed + governance.alert**.

---

## 4) بوابة: أي استدعاء أداة

تنطبق على: كل tool.call (سواء من وكيل أو من نظام أو من فعل بشري).

- [ ] **الأداة في Allowlist** ولم تُحجَر.
- [ ] **Manifest موقَّع** ومطابق للنسخة المُسجَّلة (version pinning).
- [ ] **Semantic vetting سارٍ** ولم يُلغَ.
- [ ] **Runtime guardrails نشطة** (input/output validation, egress).
- [ ] **حد التكلفة/المعدّل** لم يُتجاوَز.
- [ ] **المخرَجات النصية تُعامَل كبيانات** لا كتعليمات (حماية من prompt injection عبر tool output — راجع [TRUST_WORKSPACE_AR.md](TRUST_WORKSPACE_AR.md)).
- [ ] **سجل الاستدعاء كامل** (المُستدعي، المدخلات، النتيجة، التكلفة).
- [ ] **تصنيف البيانات الخارجة** صحيح قبل الـ egress.

---

## ربط البوابات بأركان حوكمة الذكاء الاصطناعي الأربعة

بوابات الجودة هنا تخدم الأركان الأربعة لتخفيف مخاطر الـ AI:

| الركن | كيف تخدمه البوابات |
|---|---|
| **Governance & Oversight** | بوابات المقترح والوكيل تربطان كل فعل بـ owner + قرار موثَّق |
| **Technical & Security** | بوابة الأداة تفرض allowlist + manifests + guardrails |
| **Operational Process** | كل البوابات قوائم فحص يومية، مدمجة في الإيقاع التشغيلي (راجع [DAILY_OPERATING_RHYTHM_AR.md](DAILY_OPERATING_RHYTHM_AR.md)) |
| **Transparency & Accountability** | كل بوابة تُولّد أحداثًا قابلة للتدقيق + تظهر في Trust Workspace Health |

---

## ما يحدث عند الفشل

أي بند `[ ]` لم يُحدَّد ⇒ البوابة تفشل ⇒ Hermes ينشر `execution.failed` + `governance.alert` ⇒ Trust ترصد ⇒ Sovereign يُخطَر حسب مستوى الخطر.

البوابة الفاشلة لا تُتجاوَز "هذه المرة فقط". إن تكرّر الفشل لنفس السبب، يدخل البند للـ Risk Register.

---

## English Summary

- Quality Gates are mandatory pre-execution checklists enforced by Hermes; failing the gate means the action does not happen.
- Four core gates cover any external message, any proposal, any agent run, and any tool call — each rendered as a task-list checklist.
- Gates explicitly forbid uncensored claims, cold-outreach channels, unsigned tool manifests, and treating tool output as instructions (prompt-injection protection).
- The four gates map cleanly to the four AI risk-mitigation pillars: Governance & Oversight, Technical & Security, Operational Process, and Transparency & Accountability.
- Gate failures produce `governance.alert` events and are surfaced in the Trust Workspace; recurring failures escalate to the Risk Register.
