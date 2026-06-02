# Founder GTM Control Room — غرفة قيادة السوق

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../market_os/MARKET_PRODUCTION_OS_AR.md)

> شاشة واحدة تعطي المؤسس قرار اليوم: ماذا نرسل، من نتابع، أي قطاع نوقفه — وكلها بموافقة.

---

## 1. النطاق والتكامل

هذه الغرفة طبقة قيادة فوق المحرّكات القائمة، لا واجهة جديدة منفصلة. الواجهات الموجودة في الريبو:
`/[locale]/ops/founder` (cockpit) · `/ops/war-room` · `/ops/marketing` · `/ops/sales` · `/ops/partners` ·
`/ops/approvals` · `/ops/evidence`. الـ Control Room يوحّد إشاراتها في عرض GTM واحد. المسار المقترح عند بناء
الواجهة: `/[locale]/ops/gtm-control`. حتى ذلك الحين، المخرج التشغيلي هو التقرير اليومي
[reports/gtm/DAILY_GTM_REPORT.md](../../reports/gtm/DAILY_GTM_REPORT.md) المُولّد من `scripts/verify_market_production_os.py`.

---

## 2. التبويبات (Tabs)

Brand · Products · Sectors · Prospects · Drafts · Approvals · Sending · Replies · Job Signals ·
Content · Press · Partners · WhatsApp · Metrics · Risks.

كل تبويب يربط مباشرة بوثيقته في Market Production OS وبمخططه في `schemas/`.

---

## 3. أعلى الشاشة — Today's GTM Command

- **Top 50 drafts** المرشّحة (من Draft Factory بعد الـ gates).
- **Approved sending batch** المقترحة (ضمن سقف التدرّج، لا 250 دفعة واحدة).
- **Positive replies** التي تنتظر إجراء.
- **High-risk items** التي تحتاج قرارًا.
- **Best sector today** + **Tomorrow recommendation**.

---

## 4. قرارات المؤسس من الغرفة

approve · reject · rewrite · shorten · make more formal · change offer · move to nurture · do_not_contact ·
approve sending batch · suppress · route positive reply to WhatsApp/booking.

كل قرار يُسجّل (`approval_action`) وكل إجراء خارجي يمرّ عبر `approval_center`/`safe_send_gateway`.

---

## 5. بوابات السلامة المعروضة دائمًا

- لا إرسال يتجاوز سقف التدرّج لليوم.
- لا batch بلا approval.
- تحذيرات opt-out / bounce / domain health ظاهرة أعلى الشاشة.
- لا إجراء خارجي بلا موافقة.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
