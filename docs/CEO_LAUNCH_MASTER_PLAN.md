# Dealix — خطة التدشين الرئيسية (CEO) / CEO Launch Master Plan

<!-- Owner: Founder / dealix-pm | العربية أولاً — Arabic primary -->
<!-- هذه الوثيقة هي مصدر الحقيقة الوحيد لتدشين Dealix. كل وثيقة تدشين أخرى مرجعية أو أرشيفية — انظر قسم الفهرس. -->
<!-- This document is the single source of truth for the Dealix launch. Every other launch doc is reference or archival — see the Index section. -->

> **كيف تقرأ هذه الوثيقة:** إن كان لديك 10 دقائق فقط، اقرأ القسم 2 (النجم القطبي + بوّابة Go-Live) والقسم 4 (مسار الـ14 يوماً) والقسم 8 (إجراءات المؤسس). الباقي خلفية وفهرس.
>
> **How to read this:** If you have 10 minutes, read Section 2 (North Star + Go-Live gate), Section 4 (the 14-Day Revenue Path), and Section 8 (Founder Actions). The rest is backdrop and index.

---

## 1. الرؤية والتموضع — Vision & Positioning

### العربية

Dealix شركة **عمليات ذكاء اصطناعي مُحوكَمة للسوق السعودي B2B** (Governed AI Operations for Saudi B2B). نحن لا نبيع "أدوات ذكاء اصطناعي" ولا نبيع تواصلاً جماعياً (spam). نبيع شيئين معاً لا ينفصلان:

1. **قدرة تشغيلية** — نحوّل بيانات العميل المبعثرة إلى قرار إيراد قابل للتنفيذ هذا الأسبوع: أي الحسابات أولاً، وماذا نكتب لها بالعربية والإنجليزية، وكيف نتابع.
2. **إثبات قابل للتدقيق** — كل مخرَج يحمل قرار حوكمة، وجواز مصدر، وحزمة إثبات من 14 قسماً بدرجة محسوبة. العميل لا يأخذ وعداً؛ يأخذ أثراً تدقيقياً يستطيع الدفاع عنه أمام منظّمه وفريقه.

**لماذا الآن:** السوق السعودي يتحرك بسرعة نحو تبنّي الذكاء الاصطناعي، والاختصار الأسرع (أتمتة تواصل بلا حوكمة) هو الأسرع ندماً. تموضعنا هو الشركة التي ترفض الاختصار علناً وتبني الأثر التدقيقي الذي يجعل الرفض مصدقاً.

**ما لا نقدّمه — حدود قاطعة:** لا كشط (scraping)، لا واتساب بارد، لا أتمتة LinkedIn، لا تواصل جماعي، ولا إرسال خارجي نيابة عن العميل بلا موافقته الصريحة.

### English

Dealix is a **Governed AI Operations company for Saudi B2B**. We do not sell "AI tools" and we do not sell bulk outreach. We sell two inseparable things:

1. **Operating capability** — we turn a customer's scattered data into a revenue decision they can act on this week: which accounts first, what to write them in Arabic and English, how to follow up.
2. **Auditable proof** — every output carries a governance decision, a Source Passport, and a 14-section Proof Pack with a computed score. The customer does not receive a promise; they receive an audit trail they can defend to their regulator and their team.

**Why now:** the Saudi B2B market is moving fast on AI adoption, and the fastest shortcut (ungoverned outreach automation) is the fastest to regret. Our positioning is the company that refuses the shortcut publicly and builds the audit trail that makes the refusal credible.

**What we do not offer — hard boundaries:** no scraping, no cold WhatsApp, no LinkedIn automation, no bulk outreach, and no external sending on a customer's behalf without their explicit approval.

---

## 2. النجم القطبي وبوّابة Go-Live — North Star & Go-Live Gate

### النجم القطبي — North Star

> **أول 1–3 تجارب مدفوعة فعلياً (Rung 1، سبرنت 499 ريال) خلال 14 يوماً — الإيراد أولاً.**
> First 1–3 actually-paid pilots (Rung 1, the 499 SAR Sprint) within 14 days — revenue first.

كل قرار في الـ14 يوماً القادمة يُقاس بسؤال واحد: هل يقرّبنا من فاتورة مدفوعة؟ إن لم يكن — يُؤجَّل.

### بوّابة Go-Live — الانتقال للموجة التالية

لا ننتقل للموجة التالية (توسّع، عروض جديدة، Wave 16) حتى تتحقّق **الشروط الأربعة كلها** — المصدر: `.claude/agents/dealix-pm.md`:

| # | الشرط | Condition | كيف يُتحقَّق |
|---|---|---|---|
| 1 | ≥ 1 فاتورة مدفوعة فعلياً في Moyasar | ≥ 1 paid Moyasar invoice | لوحة Moyasar (وضع حي) — لا فاتورة مسودة، لا اهتمام شفهي |
| 2 | ≥ 1 Proof Pack بدرجة ≥ 70 | ≥ 1 Proof Pack scored ≥ 70 | `proof_ledger` — درجة محسوبة عبر 14 قسماً |
| 3 | ≥ 1 ملخّص حالة آمن منشور | ≥ 1 case-safe summary published | `docs/case-studies/` — مُعلَّم anonymized، بموافقة مكتوبة |
| 4 | 0 انتهاكات عقيدة في سجلّ التدقيق | 0 doctrine violations in audit trail | حرّاس `tests/test_no_*` خضراء + سجلّ التدقيق نظيف |

**قاعدة الحقيقة المالية:** الإيراد = دليل دفع فقط (Moyasar / تحويل بنكي). الفاتورة المسودة ليست إيراداً. الاهتمام الشفهي ليس إيراداً. التشخيص المُسلَّم ليس إيراداً.

---

## 3. سلّم العروض الخمسة — The 5-Rung Offer Ladder

المصدر الكامل: [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md). الاقتصاد: [`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md).

| الدرجة | العرض | السعر | الهامش (نقدي) | الهامش (بعد وقت المؤسس) | شرط الفتح |
|---|---|---|---|---|---|
| 0 | Free AI Ops Diagnostic | مجاني | استثمار اكتساب | −77 ريال | باب الدخول — أي مؤسس B2B سعودي |
| 1 | 7-Day Revenue Proof Sprint | **499 ريال** | ~85% | ~23% | بعد التشخيص — **بوّابة الـPilot** |
| 2 | Data-to-Revenue Pack | **1,500 ريال** | ~75% | ~34% | بعد تأهيل / بعد سبرنت |
| 3 | Managed Revenue Ops | **2,999–4,999 ريال/شهر** | ~70% | ~45% | بعد سبرنت ناجح |
| 4 | Executive Command Center | **7,500–15,000 ريال/شهر** | ~65% | ~65% | بعد ≥ 3 تجارب مكتملة |
| 5 | Agency Partner OS | مخصص + rev-share 15–30% | ~55–60% | ~57% | بعد ≥ 3 Proof Packs |

> **القاعدة الذهبية:** كل درجة تُفتح فقط بعد إثبات حقيقي من الدرجة السابقة. لا ترقية قبل نتيجة موثّقة.

### إفصاح نمط التسليم — Delivery-Mode Disclosure (إلزامي)

الدرجتان 0 و1 (التشخيص المجاني وسبرنت الـ499 ريال) تُسلَّمان عبر **منتج مُتحقَّق منه** يُنتج مُخرَجاً جاهزاً للعميل. أمّا **الدرجات 3–5 فهي اليوم بقيادة المؤسس / شبه-مؤتمتة** (founder-assisted / semi-automated): الأدوات موجودة لكن التسليم يتطلّب تشغيلاً يدوياً من المؤسس. لا تُعرَض كخدمات مُدارة بالكامل، ولا تُفتح إلا بعد استيفاء شرط الفتح المذكور.

Rungs 0–1 ship a verified product deliverable. **Rungs 3–5 are founder-assisted / semi-automated today — not full managed services** — and unlock only on the stated entry conditions.

---

## 4. مسار الـ14 يوماً للإيراد — The 14-Day Revenue Path

> **هذا هو القلب التشغيلي للوثيقة.** يدمج [`14_DAY_FIRST_REVENUE_PLAYBOOK.md`](14_DAY_FIRST_REVENUE_PLAYBOOK.md) + [`go-to-market/outreach_day1.md`](go-to-market/outreach_day1.md) + [`PILOT_DELIVERY_SOP.md`](PILOT_DELIVERY_SOP.md). سبرنت الـ7 أيام يقع **داخل** هذا المسار (الأيام 6–13).
>
> **This is the operational heart of the document.** The 7-day sprint sits *inside* this path (days 6–13).

| اليوم | الحدث / المرحلة | المخرج المطلوب | إيراد متوقّع | المصدر |
|---|---|---|---|---|
| **0** | بنية تحتية + تحقّق | 3 خطوات يدوية مكتملة، `/health` أخضر، نقاط الإيراد ترجع 200 | 0 | `go-to-market/launch_runbook.md` |
| **1** | اختيار + صياغة 10 رسائل دافئة | 5 رسائل مُرسَلة يدوياً (نسخ A/B/C) | 0 | `outreach_day1.md` |
| **2** | إرسال الـ5 المتبقية + أول ردود | 2 رد، 1 مكالمة مجدوَلة | 0 | `outreach_day1.md` |
| **3** | تشغيل أول تشخيصَين مصغّرَين | 2 تشخيص ثنائي اللغة في يد العميل | 0 | Rung 0 |
| **4** | عرض سبرنت 499 ريال على الأنسب | 1 عرض مُرسَل، 1 "نعم" شفهي + مسار التزام مكتوب | 0 | `outreach_day1.md` |
| **5** | التزام / دفع + فتح جلسة التسليم | 1 جلسة تسليم `in_progress` + تحصيل 499 ريال أو التزام مكتوب | **499–998** | `PILOT_DELIVERY_SOP.md` (Pre-Sprint) |
| **6** | سبرنت يوم 1 — التشخيص والسياق | تقرير تشخيص + 3 أولويات موافق عليها | — | `PILOT_DELIVERY_SOP.md` يوم 1 |
| **7** | سبرنت يوم 2 — تحليل الفرص | قائمة أفضل 5 فرص موثّقة | — | `PILOT_DELIVERY_SOP.md` يوم 2 |
| **8** | سبرنت يوم 3 — صياغة الرسائل | 5 مسودات عربية `draft_only` للمراجعة | — | `PILOT_DELIVERY_SOP.md` يوم 3 |
| **9** | سبرنت يوم 4 — مراجعة ونهائية الرسائل | 5 رسائل `approved_manual` تُسلَّم للعميل (هو المرسِل) | — | `PILOT_DELIVERY_SOP.md` يوم 4 |
| **10** | سبرنت يوم 5 — KPI Baseline | جدول قبل/بعد موثّق وموقّع | — | `PILOT_DELIVERY_SOP.md` يوم 5 |
| **11** | سبرنت يوم 6 — تجميع Proof Pack | Proof Pack 4–6 صفحات، درجة ≥ 70 | — | `PILOT_DELIVERY_SOP.md` يوم 6 |
| **12** | سبرنت يوم 7 — التسليم النهائي | اجتماع 30 دقيقة + Sprint Completion Certificate موقّع | — | `PILOT_DELIVERY_SOP.md` يوم 7 |
| **13** | متابعة + عرض تحويل Managed Ops | عرض الانتقال إلى Rung 3 + ملخّص حالة آمن (مسودة) | محتمل +3,000/شهر | `OFFER_LADDER_AND_PRICING.md` |
| **14** | يوم القرار | مصفوفة قرار: تحويل / استمرار / إعادة تفكير الشريحة | — | `14_DAY_FIRST_REVENUE_PLAYBOOK.md` يوم 14 |

**هدف اليوم 14 (= بوّابة Go-Live):** ≥ 1 فاتورة Moyasar مدفوعة + ≥ 1 Proof Pack بدرجة ≥ 70.

**القمع المرجعي:** 20 رسالة دافئة → 5 demos → 1–2 تجربة مدفوعة. ممنوع: تحويل لتواصل بارد، شراء إعلانات، بناء V13، إضافة درجة تسعير جديدة، أو ادّعاء إيراد لم يصل البنك.

**حين تتوقف وتُعيد التفكير:** 0 ردود → الشريحة خطأ. ردود لكن 0 قبول تشخيص → نسخة التشخيص ضعيفة. تشخيصات لكن 0 عروض → التشخيص لا يجسر للعرض. عروض لكن 0 التزام → السعر أو العرض لا يطابق الألم. **الإجابة في كل حالة ليست كوداً أكثر — بل 14 يوماً بعرض أدقّ.**

---

## 5. خطة 90 يوماً كخلفية — The 90-Day Plan as Backdrop

المصدر: [`dealix/registers/90_day_execution.yaml`](../dealix/registers/90_day_execution.yaml). مسار الـ14 يوماً يقع داخل Phase 1.

| المرحلة | الأيام | الفكرة | المخرجات الرئيسية |
|---|---|---|---|
| **Phase 0 — Control plane first** | 0–30 | تثبيت الأساس قبل بناء المزيد | كل مخرَج حرج = DecisionOutput مُتحقَّق منه؛ سجلّ no-overclaim مفروض بـCI؛ سجلّ الامتثال السعودي؛ OTel baseline؛ عقود DecisionOutput/EventEnvelope/EvidencePack/AuditEntry منشورة |
| **Phase 1 — Revenue + Partnership controlled MVP** | 31–60 | أول سطح مواجه للعميل، مُحوكَم بالكامل | التأهيل يعمل end-to-end بحزم أدلة؛ Approval Center حي؛ واجهة موصِّلات v1 (HubSpot/WhatsApp/Email)؛ تعريفات KPI دلالية لـ5 مقاييس؛ لوحة forecast vs actual |
| **Phase 2 — Enterprise readiness lift** | 61–90 | إنتاج طبقة الثقة وإثبات تنفيذ دائم | تجربة OpenFGA؛ Vault للأسرار؛ شهادات artifact؛ مركز صحة التكامل؛ runbooks الحوادث P0/P1؛ eval harness في CI |

**هدف الـ90 يوماً:** ~8–15K ريال MRR + ~30–40K ريال دفعات لمرة واحدة = **~40–55K ريال تراكمي** بنهاية اليوم 90.

**قواعد قرار 90 يوم (`dealix-pm.md`):** إيراد ≥ 40K + 3 اشتراكات نشطة يوم 90 → اقترح Wave 3 (Enterprise Trust). إيراد < 25K يوم 60 → أوقف بناء عروض جديدة وضاعِف البيع.

---

## 6. مالكو المسارات وبوّابات القرار — Workstream Owners & Decision Gates

| المسار | الوكيل المالك | المسؤولية | بوّابة القرار |
|---|---|---|---|
| **Engineering** | `dealix-engineer` | جاهزية إنتاج 100% لمسار الإيراد؛ كل الاختبارات خضراء؛ smoke لنقاط الإيراد الأربع | لا تدشين قبل `/health` أخضر + 4 نقاط ترجع 200 + حرّاس العقيدة خضراء |
| **Sales / GTM** | `dealix-sales` | سقالة `warm_list.csv`؛ مولِّد مسودات التواصل (`draft_only` فقط)؛ مُصيِّر العروض؛ محرّك التأهيل | لا انتقال لـRung 2+ قبل سبرنت Rung 1 موثّق |
| **Content** | `dealix-content` | هذه الوثيقة؛ 6 منشورات LinkedIn + خطة النشر؛ قوالب البريد؛ إعلان التدشين (مسودة) | كل مخرَج عميل ينتهي بالتنويه ثنائي اللغة |
| **Delivery / Ops** | `dealix-delivery` | runbook الـ7 أيام؛ SOP نجاح العميل؛ تجميع Proof Pack؛ playbook التوسّع متعدد العملاء | لا إغلاق مشروع بلا Proof Pack ≥ 70 + Capital Asset |
| **Finance** | `dealix-pm` | النموذج المالي؛ تتبّع الإيراد عبر `VALUE_LEDGER.md`؛ بوّابات Go/No-Go | الإيراد = دليل دفع Moyasar فقط |

**المنسّق الوحيد:** `dealix-pm` — يفوّض بالتوازي، يجمع، يقرّر بوّابات Go/No-Go. لا يرسل تواصلاً خارجياً، لا يحصّل من عميل، لا ينتهك عقيدة.

---

## 7. فهرس وثائق التدشين — Launch Docs Index & Classification

> الغرض: المستودع فيه 60+ وثيقة تدشين متداخلة. هذا الفهرس يُنهي التشتّت — وثيقة واحدة canonical، والباقي مرجعي أو أرشيفي.

| الوثيقة | التصنيف | الاستخدام |
|---|---|---|
| **`CEO_LAUNCH_MASTER_PLAN.md`** (هذه) | **CANONICAL** | مصدر الحقيقة الوحيد للتدشين. ابدأ من هنا دائماً. |
| `OFFER_LADDER_AND_PRICING.md` | **REFERENCE** | مصدر الحقيقة للأسعار والنطاق والاستثناءات. |
| `FINANCIAL_MODEL.md` | **REFERENCE** | مصدر الحقيقة لاقتصاديات الوحدة وتوقّع 90 يوماً. |
| `14_DAY_FIRST_REVENUE_PLAYBOOK.md` | **REFERENCE** | التفصيل اليومي للأيام 1–14 (مُلخَّص ومدموج في القسم 4). |
| `PILOT_DELIVERY_SOP.md` | **REFERENCE** | SOP تسليم سبرنت الـ7 أيام (الأيام 6–12 من المسار). |
| `go-to-market/outreach_day1.md` | **REFERENCE** | نسخ التواصل الدافئ + قواعد القمع. |
| `go-to-market/launch_runbook.md` | **REFERENCE** | الخطوات اليدوية الـ3 للبنية التحتية (انظر القسم 8). |
| `MULTI_CUSTOMER_SCALING_PLAYBOOK.md` | **REFERENCE** | كيف يدير المؤسس 3–5 تجارب متوازية وحدود السعة. |
| `COMMERCIAL_LAUNCH_MASTER_PLAN.md` | **ARCHIVAL** | خطة تدشين أقدم (مراحل beta). محتوى أُدمج هنا أو في المراجع. لا تنفّذ منها. |
| `90_DAY_BUSINESS_EXECUTION_PLAN.md` | **ARCHIVAL** | استُبدلت بـ`90_day_execution.yaml` + القسم 5 هنا. |
| `STRATEGIC_MASTER_PLAN_2026.md` | **ARCHIVAL** | رؤية استراتيجية أوسع؛ غير تنفيذية لمسار الـ14 يوماً. |
| `DEALIX_100_PERCENT_LAUNCH_PLAN.md` | **ARCHIVAL** | خطة تدشين سابقة؛ مُستوعَبة في القسمين 4 و8. |
| `V14_7_DAY_REVENUE_PLAN.md` | **ARCHIVAL** | جيل V14؛ استُبدل بالقسم 4. |
| `V14_COMPREHENSIVE_STRATEGIC_PLAN.md` | **ARCHIVAL** | جيل V14؛ استراتيجي، غير canonical. |
| `V14_FOUNDER_DAILY_OPS.md` | **ARCHIVAL** | جيل V14؛ استُبدل بمسار القسم 4 اليومي. |
| `V14_PHASE_K_CLOSURE_PLAN.md` | **ARCHIVAL** | إغلاق طور V14؛ تاريخي. |
| `V14_TURNKEY_PACKAGE.md` | **ARCHIVAL** | حزمة V14؛ تاريخي. |

**قاعدة:** عند أي تعارض بين هذه الوثيقة وأي وثيقة أخرى — **هذه الوثيقة تسود**. الوثائق الأرشيفية تُحفظ للسياق التاريخي فقط ولا يُنفَّذ منها.

---

## 8. إجراءات المؤسس — Founder Actions (ما لا يستطيع أي وكيل تنفيذه)

العقيدة تمنع الوكلاء من الإرسال الحي والتحصيل الحي. الإجراءات التالية **يدوية وحصرية للمؤسس**:

1. **الخطوات الـ3 للبنية التحتية** — المصدر: `go-to-market/launch_runbook.md`:
   - **Railway** — مسح Start Command (يستخدم Dockerfile CMD)، ولصق env vars في Raw Editor، ثم Save.
   - **Moyasar Webhook** — إضافة webhook بـURL `https://<railway-url>/api/v1/webhooks/moyasar`، أحداث `payment_paid`/`payment_failed`/`payment_refunded`، والـSecret.
   - **تحديث Landing URL** — مطابقة `window.DEALIX_API_BASE` لـpublic domain الفعلي من Railway.
2. **تحويل Moyasar للوضع الحي** — تشغيل `scripts/moyasar_live_cutover.py` بعد اليوم الأول. الوكلاء يعملون في الوضع الاختباري فقط.
3. **ملء `data/warm_list.csv` بأسماء حقيقية** — الوكيل يبني السقالة (شرائح ICP + الخانات)؛ المؤسس يملأ الأسماء من شبكته الخاصة (ليست في المستودع).
4. **الإرسال الفعلي للتواصل** — WhatsApp/LinkedIn/البريد ترسَل يدوياً من حساب المؤسس. لا إرسال آلي.
5. **مكالمات الـdemo** — المؤسس يحضر كل مكالمة (30 دقيقة لكل demo).
6. **المراجعة القانونية لاتفاقية الـPilot** — `PILOT_AGREEMENT_DRAFT.md` تُراجَع قانونياً قبل أول توقيع عميل.

---

## 9. النموذج المالي — Financial Model (ملخّص)

المصدر الكامل: [`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md). كل الأرقام **توقّعات تخطيطية** — لا يوجد عميل دافع فعلي بعد.

| المؤشر | القيمة | الملاحظة |
|---|---|---|
| CAC للتجربة (Rung 1) | **~600 ريال** | حركة بقيادة المؤسس، 0 إنفاق إعلاني |
| LTV (مساهمة، تحفّظي) | **~5,800 ريال** | بافتراض تحويل 60% إلى Managed Ops، بقاء 6 أشهر |
| نسبة LTV : CAC | **~10 : 1** | صحّية جداً (المعيار الجيد ≥ 3:1) |
| فترة استرداد CAC | < شهر واحد | من أول اشتراك Managed Ops |
| التراكمي يوم 90 (سيناريو الأساس) | **~46,000 ريال** | 8 تجارب + 4 اشتراكات، ضمن هدف 40–55K |
| نقطة التعادل النقدية | أول عميل اشتراك | التكاليف الثابتة ~500–800 ريال/شهر |

**القراءة التنفيذية:** Rung 1 ليست منتج الربح — هي **باب تحويل** قريب من التعادل بعد وقت المؤسس. الربح في التحويل إلى Rung 3 المتكرّر. القيد الحاكم ليس الاقتصاد بل **سعة وقت المؤسس** (~5 عملاء متزامنين قبل التوظيف/الأتمتة).

---

## 10. العقيدة — الأحد عشر مبدأً غير القابلة للتفاوض

المصدر: `.claude/agents/dealix-pm.md` (الأسطر 33–44). مفروضة في الكود عبر اختبارات ناجحة. أي طلب ينتهك مبدأً → يُرفَض ويُقترَح بديل آمن.

1. لا أنظمة كشط (no scraping systems).
2. لا أتمتة واتساب بارد (no cold WhatsApp automation).
3. لا أتمتة LinkedIn (no LinkedIn automation).
4. لا ادّعاءات وهمية أو بلا مصدر (no fake / un-sourced claims).
5. لا ضمان نتائج بيع (no guaranteed sales outcomes).
6. لا PII في السجلّات (no PII in logs).
7. لا إجابة معرفية بلا مصدر (no source-less knowledge answers).
8. لا إجراء خارجي بلا موافقة (no external action without approval).
9. لا وكيل بلا هوية (no agent without identity).
10. لا مشروع بلا Proof Pack (no project without Proof Pack).
11. لا مشروع بلا Capital Asset (no project without Capital Asset).

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
