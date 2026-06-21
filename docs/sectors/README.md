# أدلة القطاعات — Dealix Revenue Execution OS — Sector Playbooks

> دليل تشغيلي داخلي للمؤسس وفريق البيع: كيف نقترب من كل قطاع، أي منتج نبيعه أولاً، أي رسائل نصيغ (كمسودات)، وأي دليل نطلب.
> Internal operating index for the founder and sales motion: how to approach each sector, which product to sell first, which messages to draft, and which proof to request.

**هذه الوثائق مسودات تشغيلية — ليست وعوداً تعاقدية ولا صفحات تسويق عامة.**
**These documents are internal operating drafts — not contractual promises, not public marketing pages.**

---

## مصدر الحقيقة للمنتجات والأسعار — Source of truth for products and prices

لا يجوز ذكر أي منتج أو سعر خارج هذين المصدرين. أي رقم في أي ملف قطاع يجب أن يُطابق أحدهما حرفياً:
No product or price may be stated outside these two sources. Every figure in every sector file must match one of them exactly:

1. **[DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md)** — حزم RevOps الأعلى لمسة (Revenue Diagnostic 3,500 · Lead Intelligence Sprint 9,500 · Pilot Conversion Sprint 22,000 · Monthly RevOps OS 15,000–25,000/شهر · Enterprise).
2. **[`autonomous_growth/product_catalog.py`](../../autonomous_growth/product_catalog.py)** — السلم الخماسي (Free Diagnostic 0 · Revenue Intelligence Sprint 499 · Data Pack 1,500 · Managed Ops 2,999–4,999/شهر · Custom AI 5,000–25,000).

> القائمة الكاملة للمنتجات المسموح بيعها أولاً — Allowed first-products:
> Free Diagnostic (0) · Revenue Intelligence Sprint (499) · Data Pack (1,500) · Managed Ops (2,999–4,999/mo) · Custom AI (5,000–25,000) · Revenue Diagnostic (3,500) · Lead Intelligence Sprint (9,500) · Pilot Conversion Sprint (22,000) · Monthly RevOps OS (15,000–25,000/mo).

إذا احتجت سعراً غير موجود أعلاه — **توقف**؛ لا تخترع رقماً، ارجع للمؤسس.
If you need a price not listed above — **stop**; do not invent a figure, escalate to the founder.

---

## القواعد غير القابلة للمساومة (11) — The 11 non-negotiables

تُطبّق في كل رسالة، كل عرض، كل ملف. أي مخالفة = إيقاف.
Enforced in every message, every offer, every file. Any breach = stop.

1. **الذكاء الاصطناعي يصيغ، المؤسس يوافق، النظام يتتبّع.** — AI drafts, the founder approves, the system tracks.
2. **لا إرسال خارجي آلي في الإصدار الأول.** كل إرسال يدوي بعد موافقة. — No external auto-send in v1; every send is manual after approval.
3. **لا أتمتة واتساب باردة.** — No cold WhatsApp automation.
4. **لا أتمتة LinkedIn.** — No LinkedIn automation.
5. **لا scraping ولا قوائم مشتراة.** — No scraping, no purchased lists.
6. **كل «outreach» في العروض = مسودات بانتظار الموافقة.** — All outreach in offers = DRAFTS pending approval.
7. **لا ادعاءات نتائج مضمونة** — ممنوع «نضمن» / «guaranteed results/ROI» / «100%». — No guaranteed-outcome claims.
8. **لا بيانات تعريف شخصية (PII) في السجلات** — لا أرقام، لا بريد، لا هوية، لا أسماء حقيقية في السجل. — No PII in logs.
9. **ادعاءات مدعومة بالدليل فقط** — كل ادعاء مربوط بمستوى L0–L5. — Evidence-backed claims only, tied to L0–L5.
10. **كل عرض مربوط بمنتج من الكتالوج.** — Every offer linked to a catalog product.
11. **لا نشر إنتاجي ولا أسرار في المحتوى.** — No production deploy, no secrets in content.

> المرجع التشغيلي: [`../sales-kit/FOUNDER_SIGNAL_WAR_ROOM.md`](../sales-kit/FOUNDER_SIGNAL_WAR_ROOM.md) · [`../sales-kit/L4_TRUTH_CHECK.md`](../sales-kit/L4_TRUTH_CHECK.md) · [`../commercial/operations/PROOF_STACK_ORDER_AR.md`](../commercial/operations/PROOF_STACK_ORDER_AR.md).

---

## مستويات الدليل (L0–L5) — Evidence ladder

سلّم نشر الإثبات. كل ادعاء قطاعي يجب أن يشير إلى المستوى الذي يسمح باستخدامه. لا يوجد L6/L7.
The proof-publication ladder. Every sector claim must point to the level that authorizes its use. There is no L6/L7.

| المستوى | المعنى | يُستخدم في |
|---|---|---|
| **L0** | مخطّط — لا دليل بعد | تخطيط داخلي فقط |
| **L1** | تم التسليم / مسودة داخلية | عروض داخلية فقط |
| **L2** | تمت مراجعة العميل / موافقة على مسودة | عروض pilot لعملاء مشابهين |
| **L3** | موافقة العميل / دليل بيع خاص (أرسل العميل بنفسه) | «ساعدنا [نوع شركة] على [إجراء]» |
| **L4** | أثر موثّق / موافقة نشر علني | حالة نجاح، «أدى إلى [نتيجة] في [إطار]» |
| **L5** | إيراد مُثبت أو شهادة موقّعة | حالة كاملة + تسويق خارجي (بموافقة موقّعة) |

> مصدر السلّم: `auto_client_acquisition/proof_engine/evidence.py` — انظر [`../sales-kit/L4_TRUTH_CHECK.md`](../sales-kit/L4_TRUTH_CHECK.md) و[`../PROOF_AND_CASE_STUDY_SYSTEM.md`](../PROOF_AND_CASE_STUDY_SYSTEM.md).
> القاعدة: قبل أي عميل حقيقي، أقصى ما نقدّمه هو **عيّنات L1 وأنماط case-safe** — لا أرقام منسوبة لعملاء.

---

## كيف تستخدم ملف القطاع — How to use a sector file

1. **حدّد القطاع** الأقرب للعميل المحتمل أمامك. — Pick the closest sector to the prospect in front of you.
2. **اقرأ مؤشرات المناسب/غير المناسب** قبل أي رسالة. لا تلاحق غير المناسب. — Read the fit / disqualifier signals first; do not chase a poor fit.
3. **ابدأ بالمنتج الأول** المحدّد في الملف — لا تقفز للأعلى قبل حدث إثبات. — Start with the file's first product; do not jump up a rung before a proof event.
4. **انسخ مسودة الرسالة**، عدّلها لاسم العميل وسياقه، ثم **أرسلها يدوياً بنفسك**. الرسائل في هذه الملفات **مسودات** — لا تُرسَل آلياً. — Copy a message draft, tailor it, then send it manually yourself. The messages here are DRAFTS — never auto-sent.
5. **سجّل اللمسة** في [`../sales-kit/FOUNDER_SIGNAL_WAR_ROOM.md`](../sales-kit/FOUNDER_SIGNAL_WAR_ROOM.md) وقت الإرسال. — Log the touch at send time.
6. **اطلب الدليل المناسب** للمرحلة (طبقة الـ Proof Stack)، ثم رقِّ المنتج فقط بعد حدث إثبات مُسجَّل. — Request stage-appropriate proof, then upsell only after a recorded proof event.
7. **استخدم أسئلة discovery** لتأهيل، لا لإغلاق ضاغط. — Use the discovery questions to qualify, not to high-pressure close.

> إيقاع التواصل: 5 جهات دافئة في اليوم، رسالة واحدة لكل جهة، لا متابعة ثانية بلا رد أو نافذة متفق عليها (راجع `WARM_LIST_WORKFLOW.md`).
> Outreach cadence: 5 warm contacts/day, one message each, no second message without a reply or an agreed window.

---

## ترتيب القطاعات ومنطقه — Sector ordering and its rationale

الترتيب مقصود: نبدأ بالقطاعات التي تملك **ليدز/استفسارات/متابعات متكررة** حيث تظهر قيمة Dealix بسرعة (ترتيب، scoring، مسودات، تتبّع pipeline)، ثم ننتقل للقطاعات الأطول دورة أو الأكثر تعقيداً.
The order is deliberate: start where recurring leads, inquiries, and follow-ups make Dealix value show fast (prioritization, scoring, drafts, pipeline tracking), then move to longer-cycle or more complex sectors.

| # | القطاع | الملف | لماذا في هذا الموضع |
|---|---|---|---|
| 1 | وكالات التسويق | [MARKETING_AGENCIES_AR.md](MARKETING_AGENCIES_AR.md) | تدفّق ليدز عالٍ، فهم سريع للقيمة، متابعات يومية — أسرع إثبات. |
| 2 | شركات التدريب | [TRAINING_COMPANIES_AR.md](TRAINING_COMPANIES_AR.md) | استفسارات دورات متكررة، قوائم مهتمين تحتاج ترتيباً وscoring. |
| 3 | العيادات | [CLINICS_AR.md](CLINICS_AR.md) | استفسارات حجز متكررة + متابعات؛ حساسية PDPL عالية تُبرز حوكمة Dealix. |
| 4 | فرق العقار | [REAL_ESTATE_TEAMS_AR.md](REAL_ESTATE_TEAMS_AR.md) | حجم ليدز كبير، فوضى متابعة، أولوية واضحة لمن نتصل أولاً. |
| 5 | وكالات التوظيف | [RECRUITMENT_AGENCIES_AR.md](RECRUITMENT_AGENCIES_AR.md) | قاعدتا عملاء ومرشحين، dedupe وscoring قيمته مباشرة. |
| 6 | الخدمات المهنية | [PROFESSIONAL_SERVICES_AR.md](PROFESSIONAL_SERVICES_AR.md) | إحالات وفرص حسابات؛ دورة أطول لكن قيمة عالية للفرصة. |
| 7 | مجموعات المطاعم | [RESTAURANT_GROUPS_AR.md](RESTAURANT_GROUPS_AR.md) | عقود B2B (تموين/امتياز/مورّدين) خلف واجهة B2C — ترتيب الفرص. |
| 8 | مزوّدو التعليم | [EDUCATION_PROVIDERS_AR.md](EDUCATION_PROVIDERS_AR.md) | مواسم تسجيل، استفسارات قبول، متابعات؛ دورة موسمية. |
| 9 | شركات اللوجستيك | [LOGISTICS_COMPANIES_AR.md](LOGISTICS_COMPANIES_AR.md) | حسابات شحن B2B، عروض أسعار ومناقصات؛ بيانات أثقل. |
| 10 | SaaS المحلي | [LOCAL_SAAS_AR.md](LOCAL_SAAS_AR.md) | فرق نمو ناضجة بياناتياً؛ تباع لها لمسة أعلى مباشرة غالباً. |

> الانتقال من 1 إلى 10 = من «قيمة سريعة بمنتج خفيف» إلى «قيمة أعمق بلمسة أعلى». ابدأ من حيث الإثبات أسرع.
> Moving 1 → 10 = from "fast value with a light product" to "deeper value with a higher-touch product." Start where proof comes fastest.

---

## ما لا نعرضه في أي قطاع — What we never offer in any sector

- جمع/كشط بيانات (scraping) أو قوائم مشتراة. — Scraping or purchased lists.
- إرسال واتساب بارد آلي، أو أتمتة LinkedIn، أو إرسال نيابة عن العميل بلا موافقة صريحة. — Cold WhatsApp automation, LinkedIn automation, or sending on the client's behalf without explicit approval.
- أرقام مبيعات/تحويل/ROI كحقيقة. — Sales/conversion/ROI numbers as fact.
- إحصاءات سوق مُختلقة — الاتجاهات نوعية فقط. — Invented market statistics; trends are qualitative only.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
