# دورة حياة العميل

> النسخة الإنجليزية القانونية: [`CUSTOMER_LIFECYCLE_OS.md`](./CUSTOMER_LIFECYCLE_OS.md).

## مرجع الدوكترين
- الالتزامات: #1، #2، #5.
- القرارات المثبّتة: الموافقة-أولًا.

## الغرض

إدارة كل عميل من أول لمسة إلى الاحتفاظ والإثبات والإحالة والتوسع كدورة حياة واحدة. ما في مرحلة بدون فعل تالي محدد، وما في مرحلة تُغلق بدون نتيجة مسجّلة.

## المراحل

1. **مكتشف** — حساب في قاعدة الذكاء.
2. **مؤهل** — تجاوز ICP والتصنيف.
3. **اتُّصل به** — تواصل معتمد أُرسل.
4. **رَد** — أي رد وُصِّف.
5. **عينة** — أصل عينة أُعدّ وأُرسل.
6. **عرض** — عرض صُيغ، اعتُمد، أُرسل.
7. **دفع / أمر شراء** — حدث إيراد مسجّل.
8. **تسليم** — عمل قيد التنفيذ.
9. **ملاحظات** — ملاحظات بعد التسليم.
10. **احتفاظ** — نطاق مستمر متفق عليه.
11. **إثبات** — أصل إثبات بموافقة كتابية.
12. **إحالة** — إحالة طُلبت واستُلمت.
13. **توسع** — نطاق إضافي بيع.

## القواعد الجوهرية

- لا مرحلة بدون `next_action`، `owner`، `due_date`.
- انتقال مرحلة يكتب حدثًا مع `causation_id`.
- التراجع مسموح ومسجّل؛ ما نخفي تراجعات.
- "إثبات" ما يُنشر بدون موافقة عميل كتابية مرتبطة كرابط دليل مصدر.
- "إحالة" ما تذكر عميلًا علنًا بدون نفس الموافقة.
- تجاوز SLA في التسليم يظهر في غرفة العمليات.

## الربط بالتشغيل

- `docs/delivery/DELIVERY_LIFECYCLE.md`، `docs/agentic_operations/AGENT_LIFECYCLE.md`.
- `auto_client_acquisition/lead_inbox.py`, `crm_v10/lead_scoring.py`.
- `db/models.py::OutreachQueueRecord`.
- موجّه الردود (جزئي).
- `auto_client_acquisition/revenue_memory/event_store.py`.
- `db/migrations/versions/20260512_005_payments_table.py`.

## روابط ذات صلة

- [`../runtime/REVENUE_FACTORY_RUNTIME_AR.md`](../runtime/REVENUE_FACTORY_RUNTIME_AR.md)
- `docs/delivery/DELIVERY_LIFECYCLE.md`
- [`./SUPPORT_SUCCESS_OS_AR.md`](./SUPPORT_SUCCESS_OS_AR.md)
- [`../finance/BILLING_RECEIVABLES_OS_AR.md`](../finance/BILLING_RECEIVABLES_OS_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)

## بنود مفتوحة

- المراحل 9–13 موصوفة هنا، لكن ما عندها جداول first-class في قاعدة البيانات؛ اليوم موزّعة عبر ملاحظات وصفحات Streamlit.
- موجّه الردود (مرحلة 4) stub جزئي.
- سير عمل الإثبات (مرحلة 11) يحتاج نوع طابور موافقة مخصص.
- تتبّع الإحالات (مرحلة 12) غير رسمي.
