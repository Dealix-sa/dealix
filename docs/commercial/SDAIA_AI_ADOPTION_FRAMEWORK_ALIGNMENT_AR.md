# Dealix × SDAIA AI Adoption Framework — Alignment Map — خريطة المواءمة مع إطار تبني الذكاء الاصطناعي (SDAIA)

> **النوع:** تقييم ذاتي للمواءمة (Self-Assessment Alignment Map). **ليس** شهادة رسمية من الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA)، ولا يُنشئ التزامًا تنظيميًا.
> **Type:** Self-assessment alignment map. This is **not** an official SDAIA certification and does not create any regulatory obligation.

---

## 1) السياق — لماذا الآن (AR)

في نوفمبر 2025 أصدرت الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA) **إطار تبني الذكاء الاصطناعي** الذي يجب على جهات القطاع العام اتباعه في شراء أنظمة الذكاء الاصطناعي ونشرها وحوكمتها. يقوم الإطار على **خمس ركائز:** حوكمة البيانات، ومساءلة النماذج، والشفافية، والإشراف البشري، وإدارة المخاطر. عمليًا يعمل الإطار كمرشّح للتوريد: المورّد الذي لا يستطيع إظهار المواءمة يفقد الوصول إلى مشتريات الذكاء الاصطناعي الحكومية. و2026 هو «عام الذكاء الاصطناعي» في المملكة.

**المصدر:** إطار تبني الذكاء الاصطناعي من SDAIA، نوفمبر 2025؛ مواد رؤية 2030 / SDAIA العامة. ويعمل هذا الإطار إلى جانب **نظام حماية البيانات الشخصية (PDPL)** الساري منذ 2023: الموافقة، تحديد الغرض، تقليل البيانات، الدقة، تحديد التخزين، والأمن.

تهدف هذه الوثيقة إلى ربط القدرات **القائمة فعلًا** في Dealix بالركائز الخمس — لا قدرات موعودة. الغرض: ترشيح موضع Dealix البيعي تجاه المشترين الحكوميين والقطاعات المنظَّمة، بأدلة قابلة للتدقيق لا بادعاءات.

## 1) Context — Why Now (EN)

In November 2025, the Saudi Data & AI Authority (SDAIA) issued its **AI Adoption Framework**, which public-sector entities must follow for AI procurement, deployment, and governance. The framework rests on **five pillars:** data governance, model accountability, transparency, human oversight, and risk management. In practice it acts as a procurement filter: a vendor that cannot demonstrate alignment loses access to government AI buying. 2026 is the Kingdom's "Year of Artificial Intelligence."

**Source:** SDAIA AI Adoption Framework, Nov 2025; Vision 2030 / SDAIA public materials. The framework operates alongside the **Personal Data Protection Law (PDPL)**, in force since 2023: consent, purpose limitation, data minimization, accuracy, storage limitation, and security.

This document maps Dealix's **existing** capabilities — not promised ones — to the five pillars. The purpose is to sharpen Dealix's commercial position with government-adjacent and regulated buyers, on auditable evidence rather than claims.

---

## 2) جدول المواءمة — Alignment Table

| الركيزة — Pillar | أصول Dealix القائمة — Dealix artifact(s) | موقع الدليل (الوحدة) — Evidence location (module) |
|---|---|---|
| **حوكمة البيانات / Data governance** | SourcePassport، درجة جودة البيانات (DQ)، حجب PII، لا scraping | `auto_client_acquisition/data_os/` · `compliance_trust_os/source_passport_v2.py` |
| **مساءلة النماذج / Model accountability** | `governance_decision` على كل مخرَج؛ `decide(action, context)`؛ حواجز القنوات المحظورة والادعاءات غير الآمنة | `governance_os/` · `policy_check.py` · `forbidden_actions.py` |
| **الشفافية / Transparency** | Proof Pack من 14 قسمًا مع درجة وطبقة؛ تمييز طبقات القيمة (تقديري/ملاحَظ/مُتحقَّق) | `proof_architecture_os/` · `value_ledger.py` |
| **الإشراف البشري / Human oversight** | مركز الموافقات؛ قاعدة «لا إجراء خارجي بلا موافقة»؛ أدوار الوكلاء الثلاثة | `governance_os/` · `approval_center` · constitution Art. I–II, VI |
| **إدارة المخاطر / Risk management** | سجل التدقيق (append-only)؛ سجل الاحتكاك (friction_log)؛ الأصول الرأسمالية القابلة لإعادة الاستخدام | `audit_log.py` · `capital_os/` · `risk_resilience_os/claim_safety.py` |

> الثوابت الأحد عشر (لا scraping، لا أتمتة تواصل بارد، لا ادعاءات زائفة، لا PII في السجلات، لا إجابة بلا مصدر، لا إجراء بلا موافقة …) **تعبر الركائز الخمس جميعها** — `docs/governance/FORBIDDEN_ACTIONS.md`.
> The eleven non-negotiables (no scraping, no cold-outreach automation, no fake claims, no PII in logs, no source-less answers, no action without approval …) **cut across all five pillars** — `docs/governance/FORBIDDEN_ACTIONS.md`.

---

## 3) الركيزة الأولى — حوكمة البيانات (AR)

تدعم Dealix المواءمة مع حوكمة البيانات عبر **جواز المصدر (SourcePassport)**: لكل مصدر مالكٌ، واستخدام مسموح، وحالة وجود PII، وسياسة احتفاظ، وحالة علاقة. القاعدة صريحة: **لا جواز مصدر = لا استخدام للذكاء الاصطناعي**. تُحسب **درجة جودة البيانات (DQ)** قبل أي سير عمل، ويُحجب الـ PII تلقائيًا قبل التسجيل أو التصدير. Dealix **لا تقوم بالـ scraping**، وتُفصل البيانات العامة عن بيانات العميل. هذا يواكب مبادئ PDPL: تقليل البيانات، تحديد الغرض، الدقة، وتحديد الاحتفاظ.

## 3) Pillar 1 — Data Governance (EN)

Dealix supports alignment with data governance through the **SourcePassport**: every source carries an owner, an allowed use, a PII flag, a retention policy, and a relationship status. The rule is explicit: **no Source Passport = no AI use**. A **Data Quality (DQ) score** is computed before any workflow, and PII is redacted before logging or export. Dealix **does not scrape**, and public data is kept separate from client data. This is consistent with PDPL principles: minimization, purpose limitation, accuracy, and storage limitation.

---

## 4) الركيزة الثانية — مساءلة النماذج (AR)

كل مخرَج في Dealix يحمل **`governance_decision`** بإحدى سبع قيم: `ALLOW`، `ALLOW_WITH_REVIEW`، `DRAFT_ONLY`، `REQUIRE_APPROVAL`، `REDACT`، `BLOCK`، `ESCALATE`. تمر المخرجات عبر `decide(action, context)` قبل أي تسليم أو إجراء خارجي، وتعمل **حواجز القنوات المحظورة** و**الادعاءات غير الآمنة** على منع التواصل البارد والوعود المضمونة برمجيًا. لا يعيد أي وكيل تطبيق سياسات الحوكمة داخل المطالبات (prompts) — السياسة مركزية وقابلة للتدقيق.

## 4) Pillar 2 — Model Accountability (EN)

Every Dealix output carries a **`governance_decision`** with one of seven values: `ALLOW`, `ALLOW_WITH_REVIEW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `ESCALATE`. Outputs pass through `decide(action, context)` before any delivery or external action, and **forbidden-channel** and **unsafe-claim** guards block cold outreach and guaranteed-outcome promises in code. No agent re-implements governance policy inside prompts — policy is central and auditable.

---

## 5) الركيزة الثالثة — الشفافية (AR)

تنتج Dealix **Proof Pack من 14 قسمًا** (ملخص تنفيذي، المشكلة، المدخلات، جوازات المصدر، العمل المنجز، المخرجات، درجات الجودة، قرارات الحوكمة، المخاطر المحجوبة، مقاييس القيمة، القيود، الخطوة التالية، الأصول الرأسمالية المُنشأة) مع **درجة وطبقة** قابلتين للمراجعة من الإدارة أو الجهة الرقابية. وتُسجَّل **القيمة على طبقات صريحة:** تقديري (Estimated)، ملاحَظ (Observed)، مُتحقَّق (Verified)، ومؤكَّد من العميل (Client-confirmed). الطبقات **لا تُرقَّى تلقائيًا**، والقيمة المُتحقَّقة تتطلب `source_ref`. هذا يواكب الشفافية ومبدأ الدقة في PDPL.

## 5) Pillar 3 — Transparency (EN)

Dealix produces a **14-section Proof Pack** (executive summary, problem, inputs, source passports, work done, outputs, quality scores, governance decisions, blocked risks, value metrics, limitations, next step, capital assets created) with a **score and tier** that management or a regulator can review. Value is recorded in **explicit tiers:** Estimated, Observed, Verified, and Client-confirmed. Tiers are **never auto-promoted**, and Verified value requires a `source_ref`. This supports transparency and the PDPL accuracy principle.

---

## 6) الركيزة الرابعة — الإشراف البشري (AR)

مبدأ Dealix ثابت: **الذكاء الاصطناعي يجهّز، والإنسان يوافق، والنظام يسجّل.** عبر **مركز الموافقات** و قاعدة **«لا إجراء خارجي بلا موافقة»**، لا تُرسل Dealix أي رسالة خارجية نيابة عن العميل دون موافقة صريحة. تُصنَّف الوكلاء إلى ثلاثة أدوار فقط — مُراقِب، ومُوصٍ، ومُنفِّذ عبر سير عمل حتمي فقط — ولا يوجد دور «مُنفِّذ» غير مقيَّد. يُوجَّه قرار `ESCALATE` إلى مركز الموافقات مع عدد المُوافِقين المطلوب.

## 6) Pillar 4 — Human Oversight (EN)

Dealix's principle is fixed: **AI prepares, a human approves, the system logs.** Through the **Approval Center** and the **"no external action without approval"** rule, Dealix sends no external message on a customer's behalf without explicit approval. Agents are declared as exactly one of three roles — Observer, Recommender, or Executor-through-workflow-only — with no unconstrained "Executor." An `ESCALATE` decision routes to the Approval Center with a required-approver count.

---

## 7) الركيزة الخامسة — إدارة المخاطر (AR)

تُلحق كل قرار حوكمة وموافقة واستدعاء أداة وإجراء حسّاس بـ **سجل تدقيق append-only** (لا حذف ولا تعديل في المكان، ومؤشرات وهاش بدل المحتوى الخام والـ PII). يلتقط **سجل الاحتكاك (friction_log)** نقاط الفشل والتوتر التشغيلي لتغذية المعالجة، وتُحوَّل الدروس إلى **أصول رأسمالية قابلة لإعادة الاستخدام** عبر `capital_os`. بوابات سلامة الادعاء تمنع تصدير نتائج غير مُتحقَّقة كحقائق. هذه الآليات تواكب إدارة المخاطر والمساءلة معًا.

## 7) Pillar 5 — Risk Management (EN)

Every governance decision, approval, tool call, and sensitive action is appended to an **append-only audit log** (no deletion, no in-place edit; pointers and hashes instead of raw content and PII). A **friction_log** captures failures and operational tension to feed remediation, and lessons become **reusable capital assets** via `capital_os`. Claim-safety gates prevent exporting unverified outcomes as fact. Together these mechanisms support risk management and accountability.

---

## 8) ما لا تدّعيه هذه الوثيقة — What This Document Does Not Claim

- **AR:** هذا تقييم ذاتي للمواءمة، وليس شهادة من SDAIA. Dealix ليست جهة مانحة للشهادات. لا تَعِد Dealix بنتائج عملاء، ولا بامتثال مضمون، ولا بحصول على ترخيص؛ نستخدم «يدعم المواءمة مع» و«مصمَّم للربط مع» — لا «يضمن الشهادة». أي اعتماد رسمي يتم عبر القنوات الرسمية للجهة المختصة.
- **EN:** This is a self-assessment alignment map, not an SDAIA certification. Dealix is not a certifying authority. Dealix promises no customer outcomes, no guaranteed compliance, and no licensing; we use "supports alignment with" and "designed to map to" — never "guarantees certification." Any formal accreditation is obtained through the competent authority's official channels.

---

## 9) روابط ذات صلة — Related Documents (relative paths)

- `../governance/GOVERNANCE_RUNTIME.md` — Runtime checks, 7 decisions, envelope
- `../governance/FORBIDDEN_ACTIONS.md` — الثوابت / non-negotiables
- `../sovereignty/SOURCE_PASSPORT_STANDARD.md` — SourcePassport standard
- `../enterprise_architecture/DATA_OS.md` · `../enterprise_architecture/PROOF_OS.md` · `../enterprise_architecture/VALUE_OS.md`
- `../trust/HUMAN_OVERSIGHT_MODEL.md` · `../trust/ENTERPRISE_TRUST_PACK.md`
- `../../dealix/masters/constitution.md` — AI Operating Constitution (Art. I–XII)
- `./MARKET_INTELLIGENCE_GOVERNED_AI_CATEGORY_AR.md` — Governed Revenue AI category
- `../compliance/CUSTOMER_PDPL_GUIDE_AR.md` — PDPL customer guide

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
> هذه الوثيقة إرشاد مواءمة وليست استشارة قانونية أو تنظيمية. / This document is alignment guidance, not legal or regulatory advice.
