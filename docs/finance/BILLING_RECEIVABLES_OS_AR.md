# نظام الفوترة والمستحقات

> النسخة الإنجليزية القانونية: [`BILLING_RECEIVABLES_OS.md`](./BILLING_RECEIVABLES_OS.md).

## مرجع الدوكترين
- الالتزامات: #1 (موافقة على المدفوعات والاستردادات)، #2 (كل رقم إيراد مرتبط بحدث)، #5.
- القرارات المثبّتة: الموافقة-أولًا للأفعال الخارجية وغير القابلة للرجوع.

## الغرض

كل عرض يتحول إلى عمل مدفوع أو أمر شراء واضح، وكل سجل مدفوع ينتج أثرًا مدققًا من عرض → فاتورة → رابط دفع → إيصال → اعتراف إيراد.

## الكائنات

- العرض / Proposal.
- الفاتورة (`payments` table).
- رابط الدفع (Moyasar).
- الإيصال (webhook event + DB row).
- حدث الـ webhook (`event_store`).
- حالة الدفع (مشتقة).
- طلب استرداد (طابور موافقة).
- ملاحظة اعتراف إيراد (revenue event).

## القواعد الجوهرية

- لكل عرض مسار دفع (Moyasar، أمر شراء مكتوب، أو اتفاقية موقّعة). عرض بدون مسار دفع = draft.
- لكل دفعة حالة مرتبطة بـ webhook أو دليل مصدر مسجّل يدويًا.
- فشل webhook = حادث؛ الصمت غير مقبول.
- استرداد = A3 (لا رجوع)؛ موافقة المؤسس + سبب مكتوب.
- التسليم ما يبدأ بدون شرط بدء موثّق.
- لا يُعترف بإيراد بدون حدث نقد أو التزام مكتوب مقابل.

## بوابات الموافقة

إصدار رابط دفع، استرداد، شطب، استثناء سعر تحت الحد، شروط دفع مخصصة.

## الربط بالتشغيل

- `db/migrations/versions/20260512_005_payments_table.py`.
- `docs/BILLING_MOYASAR_RUNBOOK.md`, `docs/BILLING_RUNBOOK.md`.
- `/api/v1/checkout` (في `api/routers/`).
- Moyasar webhook (HMAC-verified) — في `docs/security/`.
- `auto_client_acquisition/revenue_memory/event_store.py`.
- `db/models.py::AuditLogRecord`.

## روابط ذات صلة

- `docs/BILLING_MOYASAR_RUNBOOK.md`
- `docs/BILLING_RUNBOOK.md`
- [`./PRICING_YIELD_MANAGEMENT_AR.md`](./PRICING_YIELD_MANAGEMENT_AR.md)
- [`./AI_UNIT_ECONOMICS_AR.md`](./AI_UNIT_ECONOMICS_AR.md)
- [`../founder/BOARD_LEVEL_KPI_STACK_AR.md`](../founder/BOARD_LEVEL_KPI_STACK_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)

## بنود مفتوحة

- عرض موحّد لتقادم المستحقات: غير موجود كـ panel واحد.
- أتمتة التذكير اللطيف للمدفوعات المتأخرة: غير موصولة.
- سير عمل الشطب: ما له نوع طابور موافقة مخصص.
- اعتراف الإيراد صحيح من حيث المبدأ (event-sourced) لكن ما يوجد سكربت مطابقة شهري.
