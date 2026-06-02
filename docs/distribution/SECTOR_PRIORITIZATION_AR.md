# Sector Prioritization — ترتيب القطاعات — Sector Prioritization

> Purpose — الغرض: تشرح هذه الوثيقة نموذج الترتيب القطاعي بمئة نقطة، والترتيب الابتدائي للقطاعات، وأول عرض مناسب لكل قطاع على السلّم الخماسي. النموذج حتمي وقابل للمراجعة؛ لا «سحر» في الترتيب، وكل وزن مُعلَن.
>
> This document explains the 100-point sector scoring model, the starting sector ranking, and the recommended first offer per sector on the 5-rung ladder. The model is deterministic and reviewable; no "magic" ranking, and every weight is declared.

Cross-link — روابط: [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md) · [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md) · [../02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md](../02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md) · [../strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md](../strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md).

---

## 1. نموذج المئة نقطة — The 100-point model

يُسجَّل كل قطاع على سبعة معايير، مجموع أوزانها 100 نقطة. الدرجة الأعلى تعني أولوية تركيز أعلى.

Each sector is scored on seven criteria summing to 100 points. A higher score means higher focus priority.

| المعيار — Criterion | الوزن — Weight | ماذا يقيس — What it measures |
|---|---|---|
| الوجع — Pain | 20 | حدّة المشكلة التي نحلّها فعليًا |
| تدفّق العملاء المتكرّر — Recurring lead flow | 15 | هل لدى القطاع حاجة متكرّرة لا لمرة واحدة |
| الوصول لصاحب القرار — Access to decision-maker | 15 | سهولة الوصول لمن يوقّع الشراء |
| القدرة على الدفع — Ability to pay | 15 | ميزانية واقعية ضمن السلّم الخماسي |
| سرعة إثبات القيمة — Speed to prove value | 15 | كم يلزم لإظهار قيمة مُلاحَظة |
| سهولة التنفيذ — Ease of execution | 10 | تعقيد التسليم والبيانات |
| الأفضلية المحلية/السعودية — Local/Saudi edge | 10 | ميزتنا في السياق السعودي (لغة، امتثال، علاقة) |

**القاعدة:** الدرجة تُحسَب حتميًا من بيانات `data/distribution/sectors.yaml` وتُراجَع يدويًا. الترتيب أداة قرار، لا وعد بنتيجة.

The score is computed deterministically from `data/distribution/sectors.yaml` and reviewed manually. The ranking is a decision tool, not an outcome promise.

---

## 2. الترتيب الابتدائي — Starting sector ranking

ترتيب ابتدائي للتركيز (الأعلى أولًا). الأرقام تقديرية للانطلاق وتُحدَّث بالأدلة من النتائج الفعلية (راجع [WIN_LOSS_LEARNING_AR.md](./WIN_LOSS_LEARNING_AR.md)).

Starting focus order (highest first). Numbers are estimates to start and are updated with evidence from real outcomes.

| # | القطاع — Sector | الدرجة التقديرية — Est. score |
|---|---|---|
| 1 | وكالات التسويق — Marketing agencies | 88 |
| 2 | شركات التدريب — Training companies | 82 |
| 3 | العيادات — Clinics | 80 |
| 4 | فرق العقار — Real estate teams | 78 |
| 5 | وكالات التوظيف — Recruitment agencies | 76 |
| 6 | الخدمات المهنية — Professional services | 74 |
| 7 | مجموعات المطاعم — Restaurant groups | 70 |
| 8 | مزوّدو التعليم — Education providers | 68 |
| 9 | الخدمات اللوجستية — Logistics | 64 |
| 10 | برمجيات/خدمات محلية — Local SaaS/service | 62 |

> ملاحظة — Note: هذه درجات بذرة لترتيب الجهد، وليست ادعاءً عن جاذبية السوق المُتحقَّقة. تتغيّر مع كل دورة تعلّم.

---

## 3. أول عرض لكل قطاع — First offer per sector

أول عرض يُربَط دائمًا بدرجة على السلّم الخماسي. نبدأ غالبًا من Rung 0 (تشخيص مجاني) أو Rung 1 (سبرنت 499 ريال) لإثبات القيمة قبل أي التزام أكبر.

The first offer always maps to a ladder rung. We usually start at Rung 0 (free diagnostic) or Rung 1 (499 SAR sprint) to prove value before any larger commitment.

| القطاع — Sector | أول عرض مقترح — Suggested first offer | الدرجة — Rung |
|---|---|---|
| وكالات التسويق — Marketing agencies | 7-Day Revenue Intelligence Sprint | Rung 1 — 499 SAR |
| شركات التدريب — Training companies | Free AI Ops Diagnostic ثم Sprint | Rung 0 → 1 |
| العيادات — Clinics | Free AI Ops Diagnostic | Rung 0 — 0 SAR |
| فرق العقار — Real estate teams | 7-Day Revenue Intelligence Sprint | Rung 1 — 499 SAR |
| وكالات التوظيف — Recruitment agencies | Data-to-Revenue Pack | Rung 2 — 1,500 SAR |
| الخدمات المهنية — Professional services | Free AI Ops Diagnostic | Rung 0 — 0 SAR |
| مجموعات المطاعم — Restaurant groups | 7-Day Revenue Intelligence Sprint | Rung 1 — 499 SAR |
| مزوّدو التعليم — Education providers | Free AI Ops Diagnostic | Rung 0 — 0 SAR |
| الخدمات اللوجستية — Logistics | Data-to-Revenue Pack | Rung 2 — 1,500 SAR |
| برمجيات/خدمات محلية — Local SaaS/service | Managed Revenue Ops (بعد إثبات) | Rung 3 — 2,999–4,999 SAR/mo |

السلّم الكامل وأقسام العرض: [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md).

---

## 4. كيف يُستخدَم الترتيب يوميًا — How the ranking is used daily

- مرحلة الاستهداف في خط الأنابيب (المرحلة 1) تُرتّب الجهات داخل أعلى القطاعات أولًا.
- كل جهة تحتاج مصدرًا مُعلَنًا (Source Passport) قبل أن تُستهدَف؛ لا كَشط (البند 1).
- الدرجة لا تتجاوز الموافقة: حتى أعلى قطاع، كل مسودة تبقى `pending_approval`.

The ranking feeds Stage 1 (Target): prospects inside the top sectors are ordered first. Every prospect needs a declared source before targeting (no scraping). The score never overrides approval; even the top sector's drafts stay `pending_approval`.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
