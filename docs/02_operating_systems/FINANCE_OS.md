# Finance OS — Pricing, invoicing and margin system — النظام المالي

## Purpose — الغرض

Finance OS holds the commercial arithmetic of Dealix: pricing for the Command Sprint and managed work, invoice scaffolding, monthly recurring revenue, and margin per engagement. It gives the founder one honest view of what the business earns and keeps, traceable to real, sourced events rather than projections. AI analyzes cost and pricing context and recommends a price band; deterministic workflows generate invoice drafts and roll up MRR and margin; the human approves every price and every invoice before it is issued. The system is ZATCA-aware — it is designed with Saudi Fatoora e-invoicing requirements in mind — but it is not a certified e-invoicing provider, and must never be presented as one until it is actually built and certified. All figures are recorded as estimated until backed by a real, dated transaction.

النظام المالي يحمل حساب Dealix التجاري: تسعير سبرنت القيادة والعمل المُدار، هيكل الفواتير، الإيراد الشهري المتكرّر، وهامش كل ارتباط. يمنح المؤسس عرضاً صادقاً واحداً لما يكسبه العمل ويحتفظ به، مرتبطاً بأحداث حقيقية موثّقة لا بتوقّعات. يحلّل الذكاء الاصطناعي سياق التكلفة والتسعير ويوصي بنطاق سعر؛ وتنشئ المسارات الحتمية مسودات الفواتير وتجمّع الإيراد المتكرّر والهامش؛ ويعتمد الإنسان كل سعر وكل فاتورة قبل إصدارها. النظام مُدرك لمتطلّبات هيئة الزكاة والضريبة (مصمَّم على وعي بمتطلّبات الفوترة الإلكترونية "فاتورة") لكنه ليس مزوّداً معتمداً للفوترة الإلكترونية، ولا يجوز تقديمه كذلك حتى يُبنى ويُعتمد فعلاً. كل الأرقام تُسجَّل كتقديرية حتى تدعمها معاملة حقيقية مؤرَّخة.

## Status — الحالة

Finance OS | INTERNAL | Pricing + invoice scaffolding; ZATCA-aware, not certified

النظام المالي | INTERNAL | تسعير وهيكل فواتير؛ مُدرك لمتطلّبات هيئة الزكاة والضريبة، غير معتمد

## Inputs — المدخلات

- Approved offers and scope from Revenue OS — العروض والنطاق المعتمدة من نظام الإيراد
- Price authority bands from go-to-market docs — نطاقات سلطة السعر من وثائق الذهاب إلى السوق
- Delivered engagements and renewals from Delivery OS and Client OS — الارتباطات المُسلَّمة والتجديدات من نظام التسليم ونظام العميل

## Outputs — المخرجات

- Invoice drafts pending approval (ZATCA-aware, not certified) — مسودات فواتير بانتظار الاعتماد (مُدركة لمتطلّبات الهيئة، غير معتمدة)
- MRR and margin roll-up from sourced transactions — تجميع الإيراد المتكرّر والهامش من معاملات موثّقة
- Pricing inputs handed back to Revenue OS — مدخلات التسعير المُعادة لنظام الإيراد

## Guardrails — الضوابط

- No fake or un-sourced claims (4): figures trace to real, dated transactions — لا ادعاءات مزيّفة أو بلا مصدر
- No guaranteed sales outcomes (5): MRR projections are labeled estimated — لا ضمان لنتائج البيع
- No external action without approval (8): no invoice issues without sign-off — لا إجراء خارجي بلا اعتماد
- No PII in logs (6): financial records avoid personal identifiers in operational logs — لا بيانات شخصية في السجلات

## Cross-links — روابط

- [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)
- [`../01_go_to_market/PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md)
- [`REVENUE_OS.md`](./REVENUE_OS.md) · [`DELIVERY_OS.md`](./DELIVERY_OS.md) · [`CLIENT_OS.md`](./CLIENT_OS.md) · [`GOVERNANCE_OS.md`](./GOVERNANCE_OS.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
