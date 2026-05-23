# Revenue Risk Model — Dealix

## الدور — Role

مخاطر تحويل العمل إلى كاش.

## فهرس المخاطر — Indexed risks

| ID | Description | Severity | Likelihood | Mitigation |
| --- | --- | --- | --- | --- |
| REV-001 | اعتماد مفرط على عميل واحد (>30% من cash) | high | medium | تنويع pipeline، حد 30% |
| REV-002 | تأخير payment بعد proposal | high | high | دفع جزئي مقدم + ZATCA invoice فوري |
| REV-003 | proposal بدون discovery حقيقي | medium | high | لا proposal بدون call ≥30 دقيقة |
| REV-004 | تسعير غير منضبط (خصومات عشوائية) | medium | medium | pricing card + لا قرار خصم > 15% بدون founder |
| REV-005 | فقدان عميل بعد sample بدون follow-up | high | medium | followup queue يومي |
| REV-006 | recognition مبكر للإيرادات | medium | low | finance_os يلتزم بالاستلام الفعلي |
| REV-007 | refund/chargeback غير متوقع | medium | low | sample واضح + Done definition قبل البيع |

## القياس — Measurement

- `revenue_forecast.md` يربط كل risk بـ cash اعتمادًا على `cash_collected.csv`.
- Forecast confidence ينخفض كلما زاد الـ open risk.

## الملكية — Ownership

- Owner: Founder.
- Reviewer: Finance.
