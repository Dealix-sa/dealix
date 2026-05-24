# Daily Operating Rhythm — الإيقاع اليومي

> المرجع: §48 من المواصفة الأصلية.

---

## لماذا إيقاع محدَّد؟

نظام Dealix يولّد آلاف الأحداث يوميًا. بدون إيقاع تشغيلي صارم، تتراكم القرارات، تتأخر الاستجابة للتنبيهات، وتختنق Sovereign بقرارات يمكن أن تُحلّ عند مستوى أدنى. الإيقاع يفرض **متى يُفتَح ماذا، من قِبَل من، لكم من الوقت، وبأي مُخرَج**.

---

## إيقاع الصباح (08:30 – 10:00)

**الغرض**: ضبط اليوم بناءً على ما حدث في الليل + ما تراكم منذ أمس.

| الوقت | الدور | الفعل | المُخرَج |
|---|---|---|---|
| 08:30 | Sovereign | فتح Command Page — مراجعة Pending Approvals + Risk Alerts | قرارات معلَّقة تُحسم أو تُؤجَّل بمدة محددة |
| 08:40 | Sovereign | فحص Personal Wealth Pulse | مؤشر أحمر/أصفر/أخضر فقط — لا تفاصيل |
| 08:45 | Lead Operations | Inbox + Opportunities triage | تصنيف كل إشارة جديدة + توزيع المهام |
| 09:15 | Agents Owner | Agents + Tools health check | إيقاف أي وكيل في failure متكرّر |
| 09:30 | Trust Lead | Active Alerts + Quality Gates Health | إغلاق Low/Medium، تصعيد High/Critical |
| 09:45 | Delivery Lead | Delivery + Evidence (يحتاج إرسال اليوم) | قائمة "للإرسال بعد البوابة" |

**القاعدة الصارمة**: لا اجتماع صباحي يمتد > 90 دقيقة إجماليًا. القرارات الكبرى لا تُؤجَّل لـ "اجتماع لاحق" — تُحسم الآن أو تُوضَع في Approvals بمهلة.

---

## إيقاع منتصف اليوم (12:00 – 13:30)

**الغرض**: نقطة تحقق على التنفيذ الفعلي، ليس فقط على التخطيط.

| الوقت | الدور | الفعل | المُخرَج |
|---|---|---|---|
| 12:00 | Delivery Lead | فحص Deliveries نصف يومية | تحديث حالات + رفع أي عائق لـ Sovereign |
| 12:15 | Sales/Pipeline | Pipeline — حالة الفرص المفتوحة | تحديث conversion، تجهيز مكالمات بعد الظهر |
| 12:30 | Content/Evidence | حِزَم الأدلة قيد البناء | ختم ما اكتمل، تأجيل ما يحتاج بشريًا |
| 12:45 | Customer Success | Customers — صحة العميل | تنبيهات upsell/risk، تجهيز Value Reports |
| 13:00 | Sovereign (اختياري) | مراجعة سريعة لـ Money Pulse | تأكيد الاتجاه فقط، لا اتخاذ قرار |

---

## إيقاع نهاية اليوم (16:00 – 17:30)

**الغرض**: إغلاق اليوم بشفافية + تجهيز يوم غد.

| الوقت | الدور | الفعل | المُخرَج |
|---|---|---|---|
| 16:00 | Lead Operations | Internal Ops — إغلاق المهام | قائمة "تم" + قائمة "مُؤجَّل لـ غدًا" |
| 16:15 | Trust Lead | Audit Trail spot-check | عيّنة عشوائية من 5–10 أحداث، أي شك يُسجَّل |
| 16:30 | Content/Evidence | Content output check | ما نُشر اليوم، ما لم يُنشر ولماذا |
| 16:45 | كل القادة | Quality (read-only) | معدل عبور البوابات اليوم، أسباب الرفض |
| 17:00 | Sovereign | تقرير اليوم المُولَّد آليًا (من Internal) | قراءة + توقيع/تعليق |
| 17:15 | Sovereign | Decision Journal — توثيق قرارات اليوم | كل قرار مكتوب باختصار + المُبرّر |

---

## إيقاع أسبوعي

**الأحد صباحًا** — مراجعة الأسبوع السابق:
- Trust: تنبيهات الأسبوع، التوزيع، الأنماط، التحسينات المقترحة.
- Money Engine: مقارنة الأسبوع مع التوقعات (Estimated vs Verified).
- Pipeline: conversion بين المراحل، عُمر المتأخّرين.
- Venture: تقدّم البطاقات النشطة + توصيات Scale/Kill قيد البناء.

**الخميس بعد الظهر** — مراجعة الأسبوع القادم:
- Approvals: ما الذي يحتاج قرارًا قبل الإثنين؟
- Capital Allocation: هل توزيع رأس المال يلائم الأولويات؟
- Personal Wealth: مراجعة شهرية حين يحلّ موعدها (راجع [MONEY_FLOW_AR.md](MONEY_FLOW_AR.md)).

---

## إيقاع شهري (مرّة في الشهر)

- مراجعة كل **Vertical Card** نشطة → توصية Scale/Hold/Kill (راجع [SCALE_KILL_PLAYBOOK_AR.md](SCALE_KILL_PLAYBOOK_AR.md)).
- إصدار **Customer Value Reports** لكل عميل (راجع [CUSTOMER_WORKSPACE_AR.md](CUSTOMER_WORKSPACE_AR.md)).
- مراجعة **Tool Registry**: ما يحتاج إعادة semantic vetting، ما يجب إيقافه.
- مراجعة **Risk Register**: ما الذي تحوَّل من High إلى Closed، ما الجديد.

---

## إيقاع ربعي

- مراجعة الشركاء (Partner audit) — هل القواعد الـ 5 محفوظة؟
- مراجعة Capital Allocation الكاملة.
- مراجعة Trust Policies — هل تحتاج تحديثًا؟
- مراجعة Personal Wealth العميقة (Tax + Zakat posture, asset productivity).

---

## ما لا يُفعل (Anti-rhythm)

> هذه قائمة "no-go" يجب أن يعرفها كل فرد في Internal/Partner workspaces.

- **لا cold outreach بدون موافقة** — لا email، لا WhatsApp، لا LinkedIn DM.
- **لا scraping** لأي مصدر بيانات.
- **لا إرسال رسالة خارجية بدون بوابة الجودة** (راجع [QUALITY_GATES_AR.md](QUALITY_GATES_AR.md))، حتى لو كان "عاجلًا".
- **لا تشغيل وكيل جديد** دون قيده في Agent Registry وموافقة المستوى المناسب.
- **لا "approval شفوية"** — كل قرار في Decision Journal أو لم يحدث.
- **لا قفز الحدود بين الـ workspaces** — حتى إن طُلب "كاستثناء".
- **لا تجاوز Quality Gate "مرة واحدة فقط"** — هذا أسوأ سلوك يمكن أن يحدث؛ يُسجَّل كحدث Critical.
- **لا ضمانات أرقام** في أي تواصل خارجي.
- **لا تأجيل قرار Kill بسبب sunk cost**.
- **لا اجتماعات > 90 دقيقة** بدون قرار محدَّد مسبقًا للمدة الإضافية.
- **لا فتح Personal Wealth** خارج Sovereign Workspace.

---

## كيف يُقاس الالتزام بالإيقاع؟

Trust Workspace تتابع:
- نسبة الأحداث المُغلَقة ضمن SLA إيقاعها.
- عدد القرارات المُؤجَّلة دون مهلة محدّدة.
- عدد البوابات الفاشلة المُتجاوَزة (يجب أن تكون 0).
- عدد المخالفات لقائمة "ما لا يُفعل".

أي اختلال يدخل Risk Register عند Medium على الأقل.

---

## English Summary

- The daily rhythm forces named owners to open specific pages at specific times, with bounded outputs, so decisions don't pile up at the Sovereign level.
- Morning (08:30–10:00) handles approvals + alerts + triage; midday (12:00–13:30) is a delivery checkpoint; end-of-day (16:00–17:30) closes the loop and journals decisions.
- Weekly, monthly, and quarterly cadences cover trust patterns, Vertical Card reviews, partner audits, capital allocation, and personal wealth deep reviews.
- A strict "what NOT to do" list bans cold outreach, scraping, gate bypassing, verbal approvals, sunk-cost-driven holds, and any cross-workspace boundary jump.
- Trust measures adherence — events closed within their cadence SLA, decisions left without deadlines, and any gate failures — and escalates lapses into the Risk Register.
