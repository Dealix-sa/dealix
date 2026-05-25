# Dealix Growth Engine — محرك النمو الموحّد

> هذه الوثيقة الأصل (section 32). تشرح المكوّنات الـ13 لمحرك النمو، مسؤول كل مكوّن، مخرجاته، ومؤشّرات نجاحه.
> Module path: `dealix/growth_os/`

---

## مقدّمة — Introduction

محرك النمو في Dealix ليس "تسويق". هو نظام تشغيلي يربط الإشارة السوقية بالإيراد المُتحقَّق عبر طبقات حوكمة. كل مكوّن له مدخلات واضحة، مخرجات قابلة للتدقيق، ووكيل/فريق مسؤول.

The Dealix Growth Engine is not "marketing". It is an operating system that connects market signal to verified revenue under governance. Each component has explicit inputs, auditable outputs, and a responsible agent or team.

---

## 1) Market Signal Radar — رادار الإشارات السوقية

**EN one-liner.** Detect changes in sectors, regulation, hiring, and AI demand before competitors.

**التعريف.** يلتقط الرادار إشارات من المصادر العامة (تنظيم SDAIA، إعلانات توظيف، أخبار قطاعية، اتجاهات بحث) ويصنّفها إلى فرص قابلة للعمل.

- **Inputs:** RSS قطاعية، صفحات حكومية معلنة، lists JSON محفوظة محليّاً.
- **Outputs:** `SignalCard` يحتوي (sector, signal_type, source_url, urgency, suggested_offer).
- **Owner:** Growth Researcher Agent.
- **KPIs:** عدد إشارات/أسبوع، نسبة تحويل الإشارة إلى محادثة، median time-to-action.
- **Dealix example.** إشارة "نشر SDAIA لإطار جديد" تتحوّل تلقائياً إلى مسودة محتوى GEO و3 رسائل ABM موجّهة لقطاع التأمين.

`dealix/growth_os/signal_radar/`

---

## 2) ICP Intelligence — استخبارات العميل المثالي

**EN one-liner.** Continuously refine who we serve and why they buy.

**التعريف.** قاعدة معرفة حيّة لـ 7 ICPs (راجع `ICP_MATRIX_AR.md`)، تُحدَّث بعد كل محادثة بيع أو رفض.

- **Inputs:** سجلات CRM، ملاحظات المكالمات، تعليقات العملاء.
- **Outputs:** `ICPProfile` يحتوي (pain, offer, qualification_questions, disqualifiers).
- **Owner:** Sales Ops + Founder.
- **KPIs:** ICP fit score متوسط، نسبة الصفقات المغلقة من ICPs الأساسية، عدد الـ disqualifiers الموثَّقة.
- **Dealix example.** بعد 10 محادثات مع وكالات، أُضيفت "هل لديك عميل ينتظر تقرير AI خلال 14 يوم؟" كسؤال تأهيل.

`dealix/growth_os/icp_intelligence/`

---

## 3) Offer-Market Fit — مطابقة العرض بالسوق

**EN one-liner.** Test, price, and refine offers until repeat buyers exist.

**التعريف.** كل عرض يمر بدورة (draft → priced → tested → validated → scaled أو killed). لا عرض يُسوَّق قبل أن يُختبر على 3 محادثات حقيقية.

- **Inputs:** ICPProfile، benchmark تسعير محلي، تكلفة تسليم تقديريّة.
- **Outputs:** `OfferCard` (name, price_band, deliverables, sla, decision).
- **Owner:** Founder + Delivery Lead.
- **KPIs:** offer→deal conversion، median proposal-to-signature، retainer rate.
- **Dealix example.** "AI Governance Snapshot" بسعر `<TBD: founder fill>` ر.س اختُبر على 3 وكالات قبل النشر.

`dealix/growth_os/offer_market_fit/`

---

## 4) ABM Engine — محرك الحسابات المستهدفة

**EN one-liner.** Account-based motion with metadata enrichment only, no automated external sends.

**التعريف.** خط أنابيب 10 مراحل (راجع `ABM_PLAYBOOK_AR.md`) من اكتشاف الحساب إلى التحويل. كل خطوة تتطلّب موافقة بشرية قبل أي تواصل خارجي.

- **Inputs:** قائمة حسابات مستهدفة، SignalCard مُطابق، ICPProfile.
- **Outputs:** `AccountCard` + رسائل مسوّدة (drafted, not sent).
- **Owner:** ABM Operator + Founder approval.
- **KPIs:** accounts_engaged، meetings_booked، proposals_drafted.
- **Dealix example.** 25 وكالة في الرياض → 10 AccountCards → 4 رسائل مسوّدة → 2 اجتماع بعد موافقة المؤسّس.

`dealix/growth_os/abm_engine/`

---

## 5) Content-to-Revenue Engine — محتوى يُترجَم إلى إيراد

**EN one-liner.** Every content asset maps to a CTA, offer, and tracked outcome.

**التعريف.** 5 أنواع محتوى (trust, revenue, partner, executive, market_radar). القاعدة: لا محتوى بدون CTA، ولا CTA بدون عرض، ولا عرض بدون tracking، ولا tracking بدون نتيجة.

- **Inputs:** SignalCard، OfferCard، topic backlog.
- **Outputs:** `ContentAsset` + tracking link + attribution tag.
- **Owner:** Content Lead.
- **KPIs:** asset→meeting، asset→proposal، content_assisted_revenue.
- **Dealix example.** مقال GEO "AI Governance for Saudi Companies" → CTA حجز Governance Snapshot → 3 lead قابلة للقياس.

`dealix/growth_os/content_to_revenue/`

---

## 6) Direct Outreach Engine — التواصل المباشر المحوكم

**EN one-liner.** Human-approved, source-attributed, one-to-one only. No bulk, no scraping.

**التعريف.** رسائل مسوّدة بواسطة وكلاء، تُراجَع وتُرسَل يدويّاً من المؤسّس أو ممثّل مفوَّض. كل رسالة مرتبطة بـ SignalCard ومصدر علني.

- **Inputs:** AccountCard، SignalCard، قالب رسالة.
- **Outputs:** سجلّ outreach يحتوي (recipient_handle, channel, approved_by, sent_at).
- **Owner:** Founder.
- **KPIs:** reply_rate، meeting_rate، disqualification_rate.
- **Dealix example.** 10 رسائل/أسبوع، كلّها بموافقة المؤسّس، مع رابط إلى مصدر إشارة عام.

`dealix/growth_os/direct_outreach/`

---

## 7) Partner Growth Engine — النمو عبر الشركاء

**EN one-liner.** Agencies and consultants resell governed Dealix sprints.

**التعريف.** نظام Partner-Led Growth (راجع `PARTNER_LED_GROWTH_AR.md`) — وكالات تبيع Dealix sprints تحت علامتها مع طبقة حوكمة موحّدة.

- **Inputs:** Partner Application، Partner Tier Card.
- **Outputs:** `PartnerDealRecord` + commission ledger.
- **Owner:** Partner Lead.
- **KPIs:** partner_sourced_revenue، active_partners، partner_NPS.
- **Dealix example.** "Agency X" تبيع Governance Snapshot لـ 3 من عملائها وتحصل على عمولة `<TBD: founder fill>`%.

`dealix/growth_os/partner_growth/`

---

## 8) Paid Growth Engine — النمو المدفوع المحوكم

**EN one-liner.** Paid only after organic offer is validated; capped budget, attribution-first.

**التعريف.** لا حملات مدفوعة قبل validation organic. الميزانية مُقيَّدة بسقف شهري. كل إعلان مرتبط بعرض موثَّق.

- **Inputs:** OfferCard مُصادَق عليه، landing page بـ tracking، daily cap.
- **Outputs:** `PaidCampaignCard` (channel, spend, leads, qualified_leads, cost_per_qualified).
- **Owner:** Growth Ops.
- **KPIs:** CPQL، payback_period_days، LTV/CAC تقديري.
- **Dealix example.** حملة LinkedIn Sponsored بسقف `<TBD>` ر.س/شهر تستهدف "AI governance lead" في الرياض.

`dealix/growth_os/paid_growth/`

---

## 9) GEO / AI Search Engine — الظهور في محرّكات البحث التوليدية

**EN one-liner.** Be the answer cited by ChatGPT, Perplexity, and Gemini for Saudi AI questions.

**التعريف.** GEO يستبدل SEO التقليدي. (راجع `GEO_PLAYBOOK_AR.md`). 6 صفحات أساسية، كل صفحة بنية 8 أقسام موحّدة.

- **Inputs:** قائمة أسئلة AI شائعة في السوق السعودي، sources موثَّقة.
- **Outputs:** `GEOPage` (slug, sections, citations_count, last_refreshed).
- **Owner:** Content Lead + Founder review.
- **KPIs:** عدد الاستشهادات في AI engines (manual checks)، organic GEO traffic، GEO-attributed leads.
- **Dealix example.** صفحة `/ai-governance-saudi-companies` تظهر كمصدر في إجابة Perplexity عن "AI compliance KSA".

`dealix/growth_os/geo_engine/`

---

## 10) Conversion Engine — محرك التحويل

**EN one-liner.** Turn meetings into proposals into signed sprints.

**التعريف.** خط إنتاج موحّد للمقترحات. كل اجتماع يخرج بـ `ProposalDraft` خلال 48 ساعة. كل مقترح مرتبط بـ OfferCard معتمد.

- **Inputs:** Meeting notes، ICPProfile، OfferCard.
- **Outputs:** `ProposalRecord` (status, value, signed_at).
- **Owner:** Founder.
- **KPIs:** meeting→proposal، proposal→signature، median_cycle_days.
- **Dealix example.** اجتماع وكالة الاثنين → مقترح الأربعاء → توقيع الإثنين التالي.

`dealix/growth_os/conversion_engine/`

---

## 11) Revenue Attribution — نسبة الإيراد

**EN one-liner.** Know which channel, offer, asset, and agent caused each riyal.

**التعريف.** 7 أنواع attribution (راجع `ATTRIBUTION_AR.md`). كل صفقة لديها `AttributionRecord` يربطها بـ source signal.

- **Inputs:** RevenueRecord، touchpoints log.
- **Outputs:** `AttributionRecord` (deal_id, channel, asset, partner, agent, weight).
- **Owner:** Growth Ops.
- **KPIs:** % attributed revenue، blended CAC، channel ROAS.
- **Dealix example.** صفقة 30K ر.س مرتبطة بـ GEO page → meeting → proposal → close.

`dealix/growth_os/attribution/`

---

## 12) Retention & Upsell Engine — الإبقاء والترقية

**EN one-liner.** Sprint → Pilot → Retainer → Expansion, with proof at every gate.

**التعريف.** كل عميل يدخل دورة retention مع health score و proof pack ربعي.

- **Inputs:** ClientHealthScore، ProofPack، ExpansionOfferMap.
- **Outputs:** `RetentionRecord` (NRR، GRR، expansion_value).
- **Owner:** Delivery Lead.
- **KPIs:** NRR، GRR، logo_churn، expansion_revenue.
- **Dealix example.** عميل Snapshot → Pilot (30 يوم) → Retainer شهري `<TBD>` ر.س/شهر.

`dealix/growth_os/retention/`

---

## 13) Growth Learning Loop — حلقة التعلّم

**EN one-liner.** Every experiment, refusal, and win feeds the playbook.

**التعريف.** weekly review موثَّق. كل قرار (scale/optimize/reprice/bundle/partner_led/pause/kill) مدعوم بدليل من `ExperimentCard` أو `RevenueRecord`.

- **Inputs:** ExperimentCard، dashboard metrics، refusal log.
- **Outputs:** `LearningEntry` + تحديث ICPProfile/OfferCard/Playbook.
- **Owner:** Founder.
- **KPIs:** experiments_per_week، insights_acted_on، playbook_version.
- **Dealix example.** تجربة "سعر 5K vs 8K" → قرار scale السعر الأعلى → تحديث OfferCard.

`dealix/growth_os/learning_loop/`

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
