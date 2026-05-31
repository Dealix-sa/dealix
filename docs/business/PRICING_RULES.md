# Dealix — Pricing Rules — قواعد التسعير

This document codifies how Dealix prices, discounts, and decides when to scale, build, prepare, or wait on an offer. It governs internal behavior and is referenced in customer Commercial Terms.

تُقنّن هذه الوثيقة كيف يسعّر ديلكس، ومتى يخصم، ومتى يوسّع، ومتى يبني، ومتى يهيّئ، ومتى ينتظر. وتُحكم السلوك الداخلي ويُحال إليها في الشروط التجارية للعميل.

---

## 1. The Five Pricing Rules — قواعد التسعير الخمس

1. **Outcome before price.** Every offer is anchored to a written outcome. If the outcome is not in writing, the price is not on the table.
   **النتيجة قبل السعر.** كل عرض مُثبَّت بنتيجة مكتوبة. إن لم تُكتب النتيجة، لا يُطرح السعر.
2. **No discount without an Evidence Pack.** A discount is a response to evidence — never a response to pressure. The Evidence Pack must be delivered, dated, and reviewed.
   **لا خصم بلا حقيبة أدلة.** الخصم استجابة للدليل لا للضغط. حقيبة الأدلة مُسلَّمة ومؤرّخة ومُراجَعة.
3. **Founder-approval gate on enterprise discounts.** Any reduction on enterprise tiers requires founder sign-off. The approval is logged in the Approval Center.
   **بوابة اعتماد المؤسس للخصومات المؤسسية.** أي تخفيض في فئات المؤسسات يستوجب اعتماد المؤسس، ويُسجَّل في مركز الموافقات.
4. **Bundles compound; prices stack.** Pilot + Trust Kit + Retainer is priced as a sequence with explicit transition criteria, not as one negotiated lump.
   **الباقات تتراكم؛ والأسعار تتجاور.** الباكورة + حقيبة الثقة + الاشتراك تُسعَّر كتسلسل بمعايير انتقال صريحة، لا كحزمة تفاوضية واحدة.
5. **Methodology-only sector data; no confidential metrics in pricing logic.** Market Radar and sector reports inform pricing through methodology and aggregated patterns, never through confidential customer metrics.
   **بيانات قطاعية بالمنهجية فقط.** رادار السوق وتقارير القطاعات تُغذّي منطق التسعير بالمنهجية والأنماط المُجمَّعة، لا بمؤشرات سرية لأي عميل.

---

## 2. Revenue Stream Quality Matrix — مصفوفة جودة قنوات الإيراد

This matrix decides which streams Dealix scales, builds, prepares, or shelves.

تحدّد هذه المصفوفة أيّ قنوات يوسّعها ديلكس، ويبنيها، ويهيّئها، أو يؤجّلها.

| Stream — القناة | Margin — الهامش | Repeatability — التكرارية | Evidence Strength — قوة الدليل | Decision — القرار |
|---|---|---|---|---|
| Revenue Hunter Pilot | Medium-High — متوسط مرتفع | High — مرتفع | High — مرتفع | **Scale** — توسيع |
| AI Trust Kit | High — مرتفع | High — مرتفع | High — مرتفع | **Scale** — توسيع |
| AI Trust Diagnostic | Medium — متوسط | Very high — عالية جدًا | Medium-High — متوسط مرتفع | **Scale** — توسيع |
| Workshop | Medium — متوسط | Medium — متوسط | Medium — متوسط | **Prepare** — تهيئة |
| Revenue Command (retainer) | High — مرتفع | High — مرتفع | Medium-High — متوسط مرتفع | **Build** — بناء |
| Governance OS Retainer | Very high — عالية جدًا | Medium-High — متوسط مرتفع | High — مرتفع | **Build** — بناء |
| Agentic Control Plane Setup | High — مرتفع | Medium — متوسط | High — مرتفع | **Build** — بناء |
| Agency White-label Kit | Medium-High — متوسط مرتفع | Medium-High — متوسط مرتفع | Medium — متوسط | **Prepare** — تهيئة |
| Market Radar | Medium — متوسط | High — مرتفع | Low-Medium — منخفض-متوسط | **Prepare** — تهيئة |
| Executive PMO | High — مرتفع | Low-Medium — منخفض-متوسط | Medium — متوسط | **Later** — لاحقًا |
| Bespoke advisory (one-off) | Variable — متغيّر | Low — منخفض | Low — منخفض | **Later** — لاحقًا |

### Decision logic — منطق القرار

- **Scale — توسيع.** Margin medium-high or above, repeatable, evidence already exists. Push volume; codify the playbook; productize the artifacts.
- **Build — بناء.** High margin, repeatable, evidence emerging. Invest in tooling, templates, and a delivery runbook before pushing volume.
- **Prepare — تهيئة.** Promising stream with thin evidence. Run two to three controlled engagements to harden evidence before classifying as Build.
- **Later — لاحقًا.** Variable margin, low repeatability, or thin evidence. Park the stream; revisit on a documented trigger.

**AR.**
- **توسيع.** هامش متوسط مرتفع أو أعلى، قابل للتكرار، الدليل متوفر. ادفع الحجم، رمّز الـ Playbook، أنتج المستندات.
- **بناء.** هامش مرتفع، قابل للتكرار، الدليل ناشئ. استثمر في الأدوات والقوالب وكتاب التشغيل قبل دفع الحجم.
- **تهيئة.** قناة واعدة بدليل ضعيف. شغّل اثنين إلى ثلاثة ارتباطات محكومة لتقوية الدليل قبل النقل إلى "بناء".
- **لاحقًا.** هامش متغيّر، تكرارية منخفضة، أو دليل ضعيف. اركن القناة وراجعها على محفّز موثّق.

---

## 3. Founder-Approval Gates — بوابات اعتماد المؤسس

The following actions cannot proceed without recorded founder approval:

1. Discounts greater than ten percent on entry-tier offers.
2. Any discount, of any size, on enterprise-tier offers (Agentic Control Plane, Governance OS Retainer, Agency White-label Kit, Executive PMO).
3. Scope changes that alter data boundaries, residency, or kill-switch ownership.
4. Wiring of any new MCP server or external tool to a deployed agent.
5. Cross-tenant data flows of any kind.
6. Engagements with strategic accounts flagged by the founder office.

**AR.** الإجراءات التالية لا تمضي دون اعتماد مؤسس مُسجَّل: (١) خصم يتجاوز عشرة بالمئة في فئات الدخول. (٢) أي خصم بأي حجم في فئات المؤسسات. (٣) تغيير نطاق يمسّ حدود البيانات أو الإقامة أو ملكية مفتاح الإيقاف. (٤) توصيل أي خادم MCP أو أداة خارجية. (٥) أي تدفق بيانات عبر المستأجرين. (٦) ارتباطات مع حسابات استراتيجية موسومة من مكتب المؤسس.

---

## 4. The No-Discount-Without-Evidence-Pack Rule — قاعدة لا خصم بلا حقيبة أدلة

A discount is a response to a delivered outcome. If a customer asks for a discount before an outcome is delivered, the path is:

1. Document the request and the customer rationale.
2. Map the rationale to a measurable outcome and a date.
3. Deliver against that outcome and produce an Evidence Pack.
4. Route the discount through the Approval Center with the Evidence Pack attached.
5. Apply the discount on the next contract cycle, not retroactively.

**AR.** الخصم استجابة لمخرج مُسلَّم. إن طُلب الخصم قبل التسليم، فالمسار: (١) توثيق الطلب ومبرّر العميل. (٢) ربط المبرّر بمخرج قابل للقياس وتاريخ. (٣) التسليم وإصدار حقيبة الأدلة. (٤) توجيه الخصم عبر مركز الموافقات مع إرفاق الحقيبة. (٥) تطبيق الخصم في دورة التعاقد التالية، لا بأثر رجعي.

---

## 5. Payment & Commercial Defaults — افتراضيات الدفع والتجارة

- **Currency:** SAR for KSA engagements; other currencies require founder approval.
- **Payment terms:** 50% on signature, 50% on Evidence Pack v1 delivery (pilots). Retainers paid monthly in advance.
- **Late fees:** Two percent per month after 30 days net.
- **Refund posture:** No retroactive refunds. Disputes are resolved by re-scoping or by an additional Evidence Pack at no charge.
- **Indexation:** Annual review of retainer pricing; any increase requires written notice 60 days before renewal.

**AR.** العملة الافتراضية الريال السعودي للارتباطات المحلية. شروط الدفع: 50٪ عند التوقيع و50٪ عند تسليم حقيبة الأدلة الأولى للباكورات؛ والاشتراكات شهريًا مقدمًا. غرامات تأخير 2٪ شهريًا بعد 30 يومًا صافيًا. لا استرداد بأثر رجعي؛ تُحلّ النزاعات بإعادة النطاق أو بحقيبة أدلة إضافية دون رسوم. مراجعة سنوية للاشتراكات بإشعار 60 يومًا قبل التجديد.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/business/OFFER_CATALOG.json` · `/home/user/dealix/docs/business/SALES_NARRATIVES.md` · `/home/user/dealix/docs/enterprise/COMMERCIAL_TERMS_TEMPLATE.md`
