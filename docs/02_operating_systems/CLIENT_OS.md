# Client OS — Client memory and renewal system — نظام العميل

## Purpose — الغرض

Client OS is the long-term memory for every relationship after the first project ships. It records what was promised, what was delivered, what the client cares about, and when the next follow-up or renewal is due, so no commitment is forgotten and no renewal arrives as a surprise. AI analyzes the client history and recommends the next contact and a renewal angle grounded in delivered results; deterministic workflows schedule follow-ups, surface lapsing relationships, and maintain the client record; the human approves any message before it reaches the client. The system carries promises forward from Delivery OS and pulls supporting evidence from Proof OS, so every renewal conversation is anchored in what was actually done rather than in optimism. It does not contact clients automatically and does not invent satisfaction it cannot source.

نظام العميل هو الذاكرة طويلة الأمد لكل علاقة بعد تسليم المشروع الأول. يسجّل ما وُعد به، وما سُلّم، وما يهتم به العميل، وموعد المتابعة أو التجديد التالي، بحيث لا يُنسى التزام ولا يصل تجديد كمفاجأة. يحلّل الذكاء الاصطناعي تاريخ العميل ويوصي بالتواصل التالي وبزاوية تجديد مبنية على نتائج مُسلَّمة؛ وتجدول المسارات الحتمية المتابعات، وتُظهر العلاقات المتعثّرة، وتحفظ سجل العميل؛ ويعتمد الإنسان أي رسالة قبل وصولها إلى العميل. يحمل النظام الوعود من نظام التسليم، ويسحب الأدلة الداعمة من نظام الإثبات، بحيث ترتكز كل محادثة تجديد على ما أُنجز فعلاً لا على التفاؤل. لا يتواصل مع العملاء تلقائياً ولا يختلق رضاً لا يستطيع إسناده.

## Status — الحالة

Client OS | INTERNAL | Client memory / renewal tracking, not yet customer-facing

نظام العميل | INTERNAL | ذاكرة العميل / تتبّع التجديد، غير موجّه للعميل بعد

## Inputs — المدخلات

- Delivered scope and promises from Delivery OS — النطاق المُسلَّم والوعود من نظام التسليم
- Supporting results from Proof OS — النتائج الداعمة من نظام الإثبات
- Consent and retention records from Data OS — سجلات الموافقة والاحتفاظ من نظام البيانات
- Renewal pricing inputs from Finance OS — مدخلات تسعير التجديد من النظام المالي

## Outputs — المخرجات

- Client record: promises, delivered results, preferences, history — سجل العميل: الوعود، النتائج المُسلَّمة، التفضيلات، التاريخ
- Follow-up and renewal schedule with due dates — جدول المتابعة والتجديد بمواعيده
- Drafted renewal notes pending approval — مذكّرات تجديد مصاغة بانتظار الاعتماد

## Guardrails — الضوابط

- No external action without approval (8): every client message is human-approved — لا إجراء خارجي بلا اعتماد
- No PII in logs (6): operational logs use anonymized labels — لا بيانات شخصية في السجلات
- No fake or un-sourced claims (4): renewal value traces to the Proof Register — لا ادعاءات مزيّفة أو بلا مصدر
- No guaranteed sales outcomes (5): renewals are framed as estimated value, not promised returns — لا ضمان لنتائج البيع

## Cross-links — روابط

- [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)
- [`DELIVERY_OS.md`](./DELIVERY_OS.md) · [`PROOF_OS.md`](./PROOF_OS.md) · [`FINANCE_OS.md`](./FINANCE_OS.md) · [`DATA_OS.md`](./DATA_OS.md) · [`GOVERNANCE_OS.md`](./GOVERNANCE_OS.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
