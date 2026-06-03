# حواجز التسعير — Dealix Pricing Guardrails

> **مصدر الحقيقة للأسعار:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) و `autonomous_growth/product_catalog.py`. هذا الملف **لا يخترع أسعاراً جديدة** — يحدّد فقط الحدود والصلاحيات والموافقات.
>
> **Pricing source of truth:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) and `autonomous_growth/product_catalog.py`. This file defines bands, authority, and approvals only.

هذا الملف هو الحارس التجاري للسعر: ما الحد الأدنى والأعلى المعتمد، وحدود المفاوضة (للمؤسس فقط)، وما الذي يتطلب موافقة، وقاعدة «لا خصم تحت الأرضية».

This file is the commercial guardrail for price: approved floor and ceiling, negotiation limits (founder-only), what requires approval, and the "no discount below floor" rule.

روابط / Related: [PRODUCT_CATALOG_AR.md](PRODUCT_CATALOG_AR.md) · [OFFER_LADDER_AR.md](OFFER_LADDER_AR.md) · [APPROVAL_POLICY_AR.md](APPROVAL_POLICY_AR.md) · [../distribution/PROPOSAL_FACTORY_AR.md](../distribution/PROPOSAL_FACTORY_AR.md) · [../distribution/PAYMENT_HANDOFF_AR.md](../distribution/PAYMENT_HANDOFF_AR.md)

---

## النطاقات المعتمدة / Approved bands

كل سعر في العرض (`price_min_sar` / `price_max_sar` على كيان `proposal`) يجب أن يقع داخل هذه الحدود. القيم من المصدرين أعلاه.

Every offered price (`price_min_sar` / `price_max_sar` on the `proposal` entity) must fall within these bands. Values come from the two sources above.

| المنتج / Product | الأرضية (Floor) SAR | السقف القياسي / Standard ceiling SAR | سقف المفاوضة (مؤسس فقط) / Founder-only stretch SAR |
|---|---:|---:|---:|
| تشخيص مجاني / Free Diagnostic | 0 | 0 | 0 (لا مفاوضة) |
| سبرينت ذكاء الإيرادات / Revenue Intelligence Sprint | 499 | 499 | 499 (سعر ثابت) |
| حزمة البيانات / Data Pack | 1,500 | 1,500 | 1,500 (سعر ثابت) |
| العمليات المُدارة / Managed Ops | 2,999/شهر | 4,999/شهر | 4,999/شهر |
| حل ذكاء اصطناعي مخصص / Custom AI | 5,000 | 25,000 | 25,000 |
| Revenue Diagnostic | 3,500 | 3,500 | ~4,500 |
| Lead Intelligence Sprint | 9,500 | 9,500 | ~18,000 |
| Pilot Conversion Sprint | 22,000 | 22,000 | ~45,000 |
| Monthly RevOps OS | 15,000/شهر | 35,000+/شهر | حسب SOW |
| Enterprise AI Revenue OS | 85,000 إعداد | حسب SOW | حسب SOW |

> سقوف المفاوضة الموسّعة (Diagnostic ~4,500؛ Sprint ~18,000؛ Pilot ~45,000) مذكورة في [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) **للمؤسس فقط، ولا تُعلَن ككل العروض**.

---

## حدود المفاوضة — للمؤسس فقط / Negotiation limits — founder only

1. أي سعر **فوق** السقف القياسي وحتى سقف المفاوضة = صلاحية **المؤسس وحده**، بموافقة موثَّقة على `proposal.approval_status`. / Any price above standard ceiling up to the stretch ceiling = founder authority only, with a documented approval.
2. أي مفاوضة على نطاق متغيّر (Managed Ops, Custom AI, RevOps OS) تحتاج موافقة مؤسس **لكل عرض**. / Negotiation within a variable band needs founder approval per offer.
3. الذكاء الاصطناعي **لا يفاوض** ولا يقترح سعراً نهائياً — يقترح ضمن النطاق المعتمد فقط ويترك القرار للمؤسس. / The AI does not negotiate or set a final price — it proposes within the approved band and defers to the founder.
4. لا التزام بسعر شفهي؛ السعر النهائي يثبَّت كتابياً في `proposal` المعتمَد. / No verbal price commitment; the final price is fixed in the approved `proposal`.

---

## قاعدة «لا خصم تحت الأرضية» / No discount below floor

- **الأرضية حدّ نهائي.** لا يُعرَض أي سعر أقل من Floor لأي سبب — لا «بادئ»، لا «صديق»، لا «أول عميل». / The floor is absolute. No price below it, for any reason.
- الأسعار الثابتة (Sprint 499، Data Pack 1,500، Revenue Intelligence Sprint، Revenue Diagnostic 3,500، Lead Intelligence Sprint 9,500، Pilot 22,000) **لا تُخصَم**. / Fixed prices are not discounted.
- بدل الخصم، نزيد القيمة ضمن النطاق أو نعرض درجة أدنى مناسبة من [OFFER_LADDER_AR.md](OFFER_LADDER_AR.md). / Instead of discounting, add value within band or offer a lower suitable rung.
- أي استثناء عن الأرضية = قرار مؤسس موثَّق صراحةً، ويبقى استثناءً لا قاعدة. / Any floor exception = an explicitly documented founder decision, an exception not a rule.

---

## ما الذي يتطلب موافقة / What requires approval

| الحالة / Case | الموافقة المطلوبة / Required approval |
|---|---|
| سعر داخل النطاق الثابت (Sprint/Data Pack/Diagnostic/Sprint/Pilot) | طابور موافقة قياسي على العرض |
| سعر داخل نطاق متغيّر (Managed Ops/Custom AI/RevOps OS) | موافقة مؤسس لكل عرض |
| سعر فوق السقف القياسي (مفاوضة) | موافقة مؤسس صريحة |
| أي اقتراب من الأرضية أو طلب خصم | موافقة مؤسس + توثيق السبب |
| استثناء تحت الأرضية | قرار مؤسس موثَّق (استثناء نادر) |
| تسعير Enterprise / SOW | موافقة مؤسس على كل بند + SOW موقَّع |
| التجديد وتغيير السعر الشهري | موافقة مؤسس عبر [../distribution/RENEWAL_ENGINE_AR.md](../distribution/RENEWAL_ENGINE_AR.md) |

> لا تحصيل مالي يتم بواسطة الذكاء الاصطناعي. الدفع يمر عبر [../distribution/PAYMENT_HANDOFF_AR.md](../distribution/PAYMENT_HANDOFF_AR.md) بعد كل الموافقات. / No charging is performed by the AI. Payment runs through the payment handoff after all approvals.

---

## قواعد ملزمة / Binding rules

1. لا سعر خارج النطاقات أعلاه. / No price outside the bands above.
2. لا ضمان أرقام أو ROI مقابل السعر — القيمة تُوصَف كـ«فرص مُثبتة بأدلة». / No guaranteed numbers or ROI tied to price.
3. السعر النهائي دائماً بموافقة مؤسس عند أي خروج عن السعر القياسي الثابت. / Final price always founder-approved on any deviation from a fixed standard price.
4. كل عرض مربوط بمنتج (`product_id`) من [PRODUCT_CATALOG_AR.md](PRODUCT_CATALOG_AR.md). / Every offer links to a catalog product.
5. حدود المفاوضة سرّية للمؤسس ولا تُكتب في أي عرض أو صفحة عامة. / Negotiation limits stay confidential to the founder.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
