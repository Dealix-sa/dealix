# Post-launch backlog — Dealix Level 1+

بنود تُؤجَّل عن التشغيل اليدوي الأول. كل بند فيه **Blocked until** لتجنب البناء قبل الأدلة.

---

## B1 — WhatsApp Cloud API inbound

- ربط ويب هوك، قوالب Meta، نافذة خدمة 24 ساعة، موافقات الإرسال.
- **Blocked until:** Level 1 يعمل يدوياً + سياسة موافقات موقعة + `WHATSAPP_ALLOW_LIVE_SEND` واضح لكل بيئة.

---

## B2 — Dealix API integration

- إنشاء lead من الفورم عبر API بدلاً من أو بالتوازي مع Sheet.
- **Blocked until:** عقد الحدث والحقول في الـ API مستقر؛ staging يمر smoke كاملاً.

---

## B3 — Proof Pack generator

- توليد PDF/Doc من بيانات اللوحة تلقائياً.
- **Blocked until:** قالب Proof ثابت + مراجعة قانونية للعبارات (لا مبالغة في الوعود).

---

## B4 — CRM

- مزامنة HubSpot/Pipedrive أو جدول موحد.
- **Blocked until:** تعريف مراحل الصفقة ومصدر الحقيقة (Sheet vs CRM).

---

## B5 — Billing automation

- فواتير Moyasar عبر API بدون يدوي.
- **Blocked until:** `MOYASAR_MODE` production + مفاتيح في secrets فقط + webhook موقّع ومختبر.

---

## B6 — Partner dashboard

- لوحة للوكالات الشركاء.
- **Blocked until:** هوية وصلاحيات + بيانات تجريبية معزولة.

---

## External references (repo)

- [INTEGRATIONS_NEEDED.md](INTEGRATIONS_NEEDED.md)
- [PRODUCT_ROADMAP.md](../PRODUCT_ROADMAP.md)
- [WHATSAPP_OPERATOR_FLOW.md](../WHATSAPP_OPERATOR_FLOW.md)

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
