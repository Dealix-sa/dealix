# Distribution OS — نظام التصريف والتسويق التجاري
<!-- PHASE 10 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **القاعدة الذهبية:** Dealix لا يُباع بشرح المنتج كله. يُباع باختيار مشترٍ
> واضح، ألمٍ واضح، workflow واحد، Proof Pack واحد، وسلّم بيع يقلّل المخاطرة.
>
> **Golden rule:** Dealix is not sold by explaining the whole product. It is
> sold by choosing one clear buyer, one clear pain, one workflow, one Proof
> Pack, and a sales ladder that lowers risk.

> **حدود غير قابلة للتفاوض — Non-negotiables.** هذا النظام يخضع للـ11 بنداً
> في `.claude/agents/dealix-pm.md`: لا scraping، لا واتساب بارد آلي، لا
> أتمتة LinkedIn، لا ضمانات نتائج، لا ادعاءات بلا مصدر. كل قناة هنا تعمل
> ضمن هذه الحدود.

---

## 1. لماذا هذا النظام موجود — Purpose

كثير من مادة التصريف موجودة فعلاً في المستودع لكنها متفرّقة (سلم الخدمات،
برنامج الشركاء، قنوات التواصل، Proof Pack، التقارير القطاعية). هذا النظام
**لا يكرّر** تلك المادة — بل يربطها في خيط واحد ويضيف فقط القطع الناقصة:
علم نفس المشتري، قمع الدخول وعكس المخاطرة، قواعد الاستبعاد، sprint التوسع
30 يوماً، ومحرك الإثبات والمعايير.

This subsystem is an **orchestration layer**. Canonical figures live in
`docs/OFFER_LADDER_AND_PRICING.md` and `docs/AGENCY_PARTNER_PROGRAM.md` — this
folder never restates prices or rev-share percentages as new values.

---

## 2. السردية الفئوية — Category Narrative

> Dealix يُثبت ماذا يحدث **بعد** وصول العميل المحتمل، ويحكم استخدام AI،
> ويحوّل المتابعة الفوضوية إلى تشغيل إيرادي موثّق.
>
> Dealix proves what happens **after the lead**, governs AI actions, and
> turns messy follow-up into evidence-backed revenue operations.

Dealix لا يُصرَّف كمنتج تقني عام، ولا كـ CRM بديل، ولا chatbot، ولا أداة
أتمتة. يُصرَّف كـ **طبقة إثبات وتشغيل وحوكمة لما بعد الـlead**.

---

## 3. مصفوفة الرسائل حسب الشخصية — Persona → Message

الشخصيات الكاملة ومعايير ICP في
[`docs/POSITIONING_AND_ICP.md`](../POSITIONING_AND_ICP.md) و
[`docs/29_sales_os/ICP_SCORECARD.md`](../29_sales_os/ICP_SCORECARD.md). هذه
المصفوفة تختصر **الرسالة الواحدة** لكل شخصية فقط.

| الشخصية | الرسالة الواحدة |
|---------|------------------|
| صاحب وكالة تسويق | "Proof Pack لما بعد الحملة — فتبيع تشغيل متابعة وإثبات، لا إعلانات فقط." |
| مؤسس / CEO | "نكشف أين تضيع الفرص ونحوّلها إلى next actions موثّقة." |
| مدير المبيعات | "نوضّح من يحتاج متابعة الآن، وما الرسالة التالية، وما الدليل على الحركة." |
| COO / العمليات | "نحوّل المتابعة من رسائل متناثرة إلى workflow بمراحل وموافقات." |
| مستشار CRM / AI | "طبقة diagnostic/proof قبل التنفيذ — تدخل العميل بتنفيذ أوضح." |
| VC / مسرّعة أعمال | "مراجعة جاهزية AI & Revenue Ops لشركات المحفظة مع proof packs." |

---

## 4. معمارية القنوات — Channel Architecture

لكل قناة وظيفة وحد يومي. القوالب التفصيلية في
[`docs/business/CHANNEL_TEMPLATES.md`](../business/CHANNEL_TEMPLATES.md) و
[`docs/sales-kit/MULTI_CHANNEL_OUTREACH_PACK.md`](../sales-kit/MULTI_CHANNEL_OUTREACH_PACK.md).
المسودات المُدرَجة للموافقة في
[`docs/sales-kit/OUTREACH_DRAFTS_QUEUED.md`](../sales-kit/OUTREACH_DRAFTS_QUEUED.md).

| القناة | الوظيفة | الحد اليومي |
|--------|---------|-------------|
| LinkedIn | ثقة + محادثات دافئة | 5 تعليقات، 5 طلبات اتصال، 2 رسالة يدوية، 1 منشور |
| Email | استهداف وكالات/شركاء | 5 رسائل مستهدفة بسبب واضح وCTA واحد |
| WhatsApp | warm فقط (علاقة قائمة / inbound / إحالة / opt-in) | لا حد — حسب الردود |
| مكالمات الشركاء | مضاعفة الثقة | 1 محادثة شريك |

> **محظور في كل القنوات:** scraping، رسائل LinkedIn آلية، واتساب بارد جماعي.
> الإعلانات المدفوعة لا تُفتح بقوة قبل 3–5 demos واعتراضين متكرّرين ورسالة
> واضحة وأول التزام مدفوع.

---

## 5. إعادة تأطير المنافسة — Competitor Reframe

> Dealix لا يستبدل أدواتكم. Dealix **يحكم workflow حول** أدواتكم.

CRM يخزّن — Dealix يحرّك. الوكالة تجيب الاهتمام — Dealix يثبت ما حدث بعده.
Dashboard يعرض أرقاماً — Dealix يجهّز next action ودليلاً. التفصيل في
[`docs/sales-kit/dealix_competitor_battlecards_v2.md`](../sales-kit/dealix_competitor_battlecards_v2.md)
و[`docs/COMPETITIVE_POSITIONING.md`](../COMPETITIVE_POSITIONING.md).

---

## 6. ملفات هذا النظام — Subsystem Files

| ملف | موضوع |
|------|--------|
| [BUYER_PSYCHOLOGY.md](BUYER_PSYCHOLOGY.md) | علم نفس المشتري — لماذا يشتري فعلاً |
| [ENTRY_FUNNEL_AND_RISK_REVERSAL.md](ENTRY_FUNNEL_AND_RISK_REVERSAL.md) | قمع الدخول المجاني وعكس المخاطرة |
| [DISQUALIFICATION.md](DISQUALIFICATION.md) | متى لا تبيع — قواعد الاستبعاد |
| [EXPANSION_SPRINT_30_DAY.md](EXPANSION_SPRINT_30_DAY.md) | sprint التوسع 30 يوماً والـAgency Wedge |
| [AUTHORITY_AND_BENCHMARK_ENGINE.md](AUTHORITY_AND_BENCHMARK_ENGINE.md) | محرك الإثبات والمعايير السوقية |

---

## 7. روابط للمادة القائمة — Cross-links to canonical docs

ما يلي مغطّى بالفعل؛ هذا النظام يربط إليه ولا يكرّره:

| الموضوع | المصدر القانوني |
|---------|------------------|
| محرك التشغيل الذاتي (Full Ops) | [`docs/full_ops_sales_os/`](../full_ops_sales_os/README.md) |
| سلم الخدمات والأسعار | [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) |
| برنامج الشركاء وrev-share | [`docs/AGENCY_PARTNER_PROGRAM.md`](../AGENCY_PARTNER_PROGRAM.md) |
| برنامج الإحالة والإفصاح | [`docs/sales-kit/dealix_referral_program.md`](../sales-kit/dealix_referral_program.md) |
| لوحة التصريف اليومية | [`docs/ops/daily_scorecard.md`](../ops/daily_scorecard.md) |
| onboarding وأول 48 ساعة | [`docs/sales-kit/dealix_customer_onboarding.md`](../sales-kit/dealix_customer_onboarding.md) |
| نظام Proof والـcase studies | [`docs/PROOF_AND_CASE_STUDY_SYSTEM.md`](../PROOF_AND_CASE_STUDY_SYSTEM.md) |
| قالب Proof Pack | [`docs/templates/proof_pack.md`](../templates/proof_pack.md) |
| التقرير القطاعي / المعايير | [`docs/sales-kit/SAUDI_AI_GTM_REPORT_2026.md`](../sales-kit/SAUDI_AI_GTM_REPORT_2026.md) |
| تأهيل المبيعات والاعتراضات | [`docs/29_sales_os/`](../29_sales_os/README.md) |

---

*Version 1.0 | No guaranteed claims | Figures defer to canonical docs |
Orchestration layer — gaps only.*
