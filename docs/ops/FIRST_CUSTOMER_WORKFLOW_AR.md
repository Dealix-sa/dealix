# Dealix — مسار أول عميل (عربي)

هدف هذا الملف: من أول touch إلى Proof Pack بمسار واضح، متوافق مع Level 1 (يدوي + موافقات + أدلة).

---

## هدف أول عميل

- عميل واحد يمر بالكامل: intake → Mini Diagnostic → عرض Pilot → (اختياري) دفع sandbox/يدوي → تسليم مختصر → Proof Pack.

---

## قنوات الدخول

- Google Form (موصى به للتتبع).
- رابط WhatsApp (`wa.me`) بعد أن يبدأ العميل المحادثة (inbound فقط).
- LinkedIn / X / إحالة — سجّل `source` في اللوحة.

---

## فلو WhatsApp inbound

- العميل يضغط الرابط أو يرسل الكلمة المفتاحية → ترد برسالة أهداف (1 عملاء / 2 اجتماعات / 3 شراكات).
- لا بث جماعي؛ لا قائمة باردة. التفاصيل: [WHATSAPP_OPERATOR_FLOW.md](../WHATSAPP_OPERATOR_FLOW.md).

---

## البيانات المطلوبة

- الاسم، الشركة، القطاع، الهدف، طريقة التواصل، **موافقة صريحة**.
- إن نقصت بيانات: `diagnostic_status = waiting_data` و `next_step` = سؤال واحد محدد.

---

## Mini Diagnostic خلال 24 ساعة

- توليد `diagnostic_card` (من السكربت أو قالب يدوي) → مراجعة بشرية → إرسال → `diagnostic_status = sent`.

---

## Pilot 499 خلال 48 ساعة

- عند الإشارة للاهتمام: عرض 499 ريال / 7 أيام مع مخرجات واضحة.
- `pilot_status = offered` ثم `accepted` / `paid` / `declined` حسب الواقع.

---

## التسليم خلال 7 أيام

- بعد القبول/الالتزام: فرص، رسائل عربية، متابعات، ملاحظات مخاطر قنوات — حسب ما وُعد به في العرض.

---

## Proof Pack

- الحقول والقالب: [GOOGLE_SHEET_MODEL_AR.md](full_ops_pack/GOOGLE_SHEET_MODEL_AR.md) (تبويب `04_Proof_Pack`).
- عند الإكمال: `proof_pack_status = delivered`.

---

## DoD أول عميل

- صف في `02_Operating_Board` كامل الحقول الحرجة (انظر قائمة القبول).
- لقطة أو مستند Proof؛ حالة واضحة في اللوحة.

---

## Guardrails

- لا cold WhatsApp؛ لا Gmail خارجي تلقائي؛ لا تقويم خارجي بدون موافقة — متوافق مع سياسة المنتج Dealix v3.

---

## مرجع إضافي (إنجليزي)

- [FIRST_CUSTOMER_ONBOARDING_CHECKLIST.md](FIRST_CUSTOMER_ONBOARDING_CHECKLIST.md)
- [FIRST_CUSTOMER_DELIVERY_TEMPLATE.md](FIRST_CUSTOMER_DELIVERY_TEMPLATE.md)

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
