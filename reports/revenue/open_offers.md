# Open Offers — العروض المفتوحة

Generated: _<set by founder>_

> Data: `data/revenue/offers.jsonl` · Terms: `sales/COMMAND_SPRINT_TERMS.md`
> الإيراد يُحتسب فقط بعد دليل دفع. لا ضمان إيراد.

| company | offer | price_sar | sent_date | payment_status | next_step | due_date |
|---------|-------|-----------|-----------|----------------|-----------|----------|
|  | Command Sprint |  |  | unpaid |  |  |

## payment_status values
`unpaid` · `invoice_sent` · `committed` (التزام، ليس إيرادًا) · `paid` (دليل دفع)

## Pending follow-ups / متابعات معلّقة
- 

## On `paid` / عند الدفع
→ `python scripts/create_customer_workspace.py --name <slug>` ثم تحديث المرحلة إلى `delivery_started`.
