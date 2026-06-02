# سلم العروض — Dealix Offer Ladder

> **مصدر الحقيقة للأسعار:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) و `autonomous_growth/product_catalog.py`. هذا الملف **لا يخترع أسعاراً جديدة**.
>
> **Pricing source of truth:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) and `autonomous_growth/product_catalog.py`.

سلم العروض يحدّد **الدرجة التالية المنطقية** لكل عميل، و**متى** يحق له الصعود — والقاعدة واحدة: لا صعود إلا بعد دليل. كل درجة مربوطة بمنتج عبر `product_id` من [PRODUCT_CATALOG_AR.md](PRODUCT_CATALOG_AR.md).

The offer ladder defines the **next logical rung** for each customer and **when** they may move up — under one rule: no upward move without proof. Each rung links to a product via `product_id` from [PRODUCT_CATALOG_AR.md](PRODUCT_CATALOG_AR.md).

روابط / Related: [PRODUCT_CATALOG_AR.md](PRODUCT_CATALOG_AR.md) · [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md) · [../distribution/RENEWAL_ENGINE_AR.md](../distribution/RENEWAL_ENGINE_AR.md) · [../distribution/PROOF_PACK_FACTORY_AR.md](../distribution/PROOF_PACK_FACTORY_AR.md)

---

## المبدأ / The principle

الصعود درجة لا يحدث إلا عند توفر **دليل** بمستوى كافٍ (`evidence_level`، راجع [../distribution/PROOF_PACK_FACTORY_AR.md](../distribution/PROOF_PACK_FACTORY_AR.md)). الدليل = نتيجة موثَّقة من الدرجة الحالية، لا وعد ولا تقدير.

Moving up a rung happens only with sufficient **evidence** (`evidence_level`). Evidence = a documented result from the current rung — not a promise, not an estimate.

```text
لا دليل ⇒ لا صعود. / No proof ⇒ no upward move.
```

---

## السلم الأول — الخدمة الذاتية / Ladder 1 — Self-serve

| الدرجة / Rung | المنتج / Product | السعر SAR | شرط الصعود من هنا / Move-up condition |
|---|---|---:|---|
| 0 | تشخيص مجاني / Free Diagnostic (`prod_diagnostic_v1`) | 0 | اهتمام مؤكَّد + نقطة ألم واضحة (`evidence_level ≥ L1`) |
| 1 | سبرينت ذكاء الإيرادات / Revenue Intelligence Sprint (`prod_sprint_v1`) | 499 | تسليم خريطة + قبول العميل لإحدى الفرص (`≥ L1`) |
| 2 | حزمة البيانات / Data Pack (`prod_data_pack_v1`) | 1,500 | استخدام الـ ICP فعلياً + طلب عمق أكبر (`≥ L2`) |
| 3 | العمليات المُدارة / Managed Ops (`prod_managed_ops_v1`) | 2,999–4,999/شهر | نتيجة متكرّرة + جهة قرار + رغبة تشغيل (`≥ L3`) |
| 4 | حل ذكاء اصطناعي مخصص / Custom AI (`prod_custom_ai_v1`) | 5,000–25,000 | حاجة مخصصة مثبتة + جدوى تقنية + SOW (`≥ L3`، يفضَّل L4) |

## السلم الثاني — عقود RevOps / Ladder 2 — Higher-touch RevOps

| الدرجة / Rung | المنتج / Product | السعر SAR | شرط الصعود من هنا / Move-up condition |
|---|---|---:|---|
| A | Revenue Diagnostic (`revops_diagnostic`) | 3,500 | تقرير سلّم + قبول الانتقال للـ Sprint (`≥ L1`) |
| B | Lead Intelligence Sprint (`revops_sprint`) | 9,500 | تسليم Top 50 + خطة إجراءات + فرص مقبولة (`≥ L2`) |
| C | Pilot Conversion Sprint (`revops_pilot`) | 22,000 | Proof pack Sprint + رغبة تشغيل 30 يوماً (`≥ L3`) |
| D | Monthly RevOps OS (`revops_os_monthly`) | 15k/25k/35k+ | Proof pack Pilot ختامي + قرار استمرار (`≥ L3`) |
| E | Enterprise AI Revenue OS (`revops_enterprise`) | 85k+ إعداد | 3–5 عملاء ناجحين + جاهزية مؤسسية (`≥ L4`) |

---

## متى نصعد درجة — القاعدة بالتفصيل / When to move up a rung

1. **الدرجة الحالية سُلِّمت وقُبِلت.** المخرج النهائي مرّ بطابور الموافقة وقَبِله العميل كتابياً. / Current rung delivered and accepted in writing after passing the approval queue.
2. **هناك دليل موثَّق.** `evidence_level` يبلغ الحد المطلوب للدرجة التالية (انظر الجدولين). / Documented evidence meets the next rung's threshold.
3. **جهة القرار مؤكَّدة** للدرجات التي تتطلب التزاماً مالياً متكرّراً (Managed Ops, RevOps OS, Pilot, Enterprise). / Decision-maker confirmed for recurring-commitment rungs.
4. **المخاطر روجِعت** (`risk` على سجل العميل) ولا مانع امتثالي. / Risk reviewed, no compliance blocker.
5. **الموافقة على السعر** ضمن حدود [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md). / Price approved within guardrails.

> إن لم تتحقق هذه الشروط، الإجراء الصحيح هو **تكرار قيمة الدرجة الحالية** أو الانتقال إلى `nurture`، لا القفز درجة. / If unmet, repeat the current rung's value or move to `nurture` — do not skip a rung.

---

## مسار الترقية والبيع الإضافي / Upsell path

- **داخل السلم الواحد:** صعود درجة واحدة في كل مرة بعد دليل. لا قفز درجتين (مثلاً من تشخيص مجاني إلى Custom AI مباشرة) إلا باستثناء مؤسس موثَّق. / Within one ladder: one rung at a time after proof; no two-rung jumps except a documented founder exception.
- **بين السلمين:** عميل خدمة ذاتية أظهر حاجة أعمق يُنقَل إلى مسار RevOps من الدرجة المناسبة (غالباً Diagnostic أو Sprint) — بعرض جديد مربوط بمنتج RevOps. / Cross-ladder: a self-serve customer with deeper needs moves to the matching RevOps rung via a fresh RevOps-linked offer.
- **التجديد والتوسعة:** يُدار عبر [../distribution/RENEWAL_ENGINE_AR.md](../distribution/RENEWAL_ENGINE_AR.md) — التجديد يظهر بعد Proof pack ودورة قيمة مكتملة. / Renewal and expansion run through the renewal engine; renewal appears after a proof pack and a completed value cycle.

### نقاط البيع الإضافي الطبيعية / Natural upsell points

| من / From | إلى / To | المحفّز / Trigger |
|---|---|---|
| تشخيص مجاني | سبرينت / Sprint أو Diagnostic | نقطة ألم واضحة + اهتمام |
| سبرينت / Sprint | حزمة بيانات / Data Pack | حاجة لعمق ICP وقطاع |
| حزمة بيانات | العمليات المُدارة / Managed Ops | حاجة لتشغيل مستمر |
| Lead Intelligence Sprint | Pilot Conversion | فرص تستحق تشغيلاً 30 يوماً |
| Pilot Conversion | Monthly RevOps OS | قرار استمرار بعد Proof pack |
| Monthly RevOps OS | Enterprise AI Revenue OS | جاهزية مؤسسية + سجل نجاح |

---

## ما يمنع الصعود / What blocks a move-up

- لا دليل بالمستوى المطلوب. / Insufficient evidence level.
- لا جهة قرار مؤكَّدة لالتزام متكرّر. / No confirmed decision-maker for a recurring commitment.
- خطر امتثالي مفتوح (PDPL/مصدر بيانات). / Open compliance risk.
- طلب سعر أسفل الحد الأدنى (راجع [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md)). / Price request below floor.
- وعد بنتائج رقمية كمحفّز — مرفوض؛ المحفّز دائماً دليل لا وعد. / Numeric-result promise as trigger — rejected.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
