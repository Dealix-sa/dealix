# Daily Revenue Machine — آلة الدخل اليومية

## الغرض (AR)
يصف هذا المستند كيف يبدأ يوم المؤسس داخل نظام تنفيذ الإيرادات: كيف تُولّد الفرص، كيف يختار المؤسس أفضل 50 فرصة، كيف يحوّلها إلى إجراءات يدوية آمنة، وكيف يُسجّل الردود. **لا إرسال تلقائي — كل تواصل يدوي وبموافقة المؤسس.**

## Purpose (EN)
This document describes how the founder's day starts inside the Revenue Execution OS: how opportunities are generated, how the founder picks the top 50, how those convert into safe manual actions, and how replies are recorded. **No automated sending — every contact is manual and founder-approved.**

## بداية اليوم / How the Day Starts
1. تُجمّع المسودات المُولّدة من اليوم السابق والفرص الجديدة في قائمة واحدة.
2. يفتح المؤسس لوحة المؤشرات (`scripts/founder_revenue_dashboard.py`) لمراجعة الحالة.
3. تُرتّب الفرص حسب الجودة والقطاع والقناة.

Drafts and new opportunities are consolidated; the founder opens the dashboard and reviews ranked opportunities by quality, vertical, and channel.

## اختيار أفضل 50 / Picking the Top 50
المعايير / Criteria:
- ملاءمة القطاع (vertical fit) وقابلية الوصول.
- وجود مسودة عالية الجودة جاهزة للمراجعة.
- عدم وجود إشارات استبعاد (suppressed) أو رفض سابق.
- إمكانية تحويلها لتشخيص مدفوع.

The founder selects 50 opportunities daily based on fit, draft quality, absence of suppression flags, and diagnostic potential.

## التحويل إلى إجراءات يدوية / Converting to Manual Actions
- يراجع المؤسس كل مسودة ويعدّلها يدويًا حسب الحاجة.
- يعتمد المؤسس الإجراء (manual_action_selected) ويختار القناة المناسبة.
- **يقوم المؤسس بنفسه** بنسخ الرسالة وإرسالها يدويًا عبر القناة — النظام لا يرسل شيئًا.
- لا كشط، لا تعبئة نماذج تلقائية، لا إرسال آلي.

The founder edits each draft, approves the action, picks the channel, then **manually copies and sends** the message. The system never sends anything.

## تسجيل الردود / Recording Replies
بعد كل تواصل يدوي، يُسجّل المؤسس النتيجة في سجل الأحداث اليدوية (`data/revenue_manual_events.jsonl`):

| الحدث / Event | المعنى / Meaning |
|---|---|
| manual_send_recorded | تم الإرسال يدويًا / Manually sent |
| reply_positive | رد إيجابي / Positive reply |
| reply_negative | رد سلبي / Negative reply |
| discovery_booked | حُجزت مكالمة / Call booked |

Replies are logged manually; no inbound automation reads or sends on the founder's behalf.

## إيقاع يومي مقترح / Suggested Daily Rhythm
- صباحًا: مراجعة المسودات واختيار الـ50.
- منتصف اليوم: تنفيذ الإجراءات اليدوية.
- مساءً: تسجيل الردود وتحديث المراحل.

Morning: review and select. Midday: execute manual actions. Evening: record replies and update stages.
