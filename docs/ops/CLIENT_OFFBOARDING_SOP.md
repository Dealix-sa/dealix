# إجراءات إنهاء خدمة العميل — Client Offboarding SOP

> **الغرض / Purpose:** إجراءات موحَّدة لإنهاء علاقة العميل بنظام وحماية البيانات واستخلاص الدروس في 30 يوماً. كل خطوة مُرتبطة بالتزامات PDPL وسياسة الحوكمة.
>
> Standardised procedure for ending a client relationship with order, data protection, and lesson extraction within 30 days. Every step is tied to PDPL obligations and governance policy.
>
> **مرجع متقاطع / Cross-references:** [PDPL_RETENTION_POLICY.md](./PDPL_RETENTION_POLICY.md) · [APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) · [SPRINT_DELIVERY_CHECKLIST.md](./SPRINT_DELIVERY_CHECKLIST.md) · [CUSTOMER_ONBOARDING_DAY_BY_DAY.md](./CUSTOMER_ONBOARDING_DAY_BY_DAY.md)

---

## متى يبدأ الإنهاء — When to Offboard

يبدأ مسار الإنهاء في حالة واحدة من ثلاث:
Offboarding is triggered by one of three conditions:

1. **إلغاء العميل:** قدّم العميل طلب إلغاء خطياً أو شفهياً مؤكداً.
   **Client cancellation:** client submits a written or verbally confirmed cancellation request.
2. **انتهاء العقد بدون تجديد:** مرّت 14 يوماً على نهاية فترة العقد بدون تجديد أو تواصل.
   **Contract expiry without renewal:** 14 days have passed since contract end with no renewal or communication.
3. **العلاقة غير قابلة للاستمرار:** طلب العميل خدمات خارج نطاق Dealix أو انتهكت الشراكة حدوداً غير قابلة للتفاوض (مثل طلب الإرسال التلقائي بدون موافقة).
   **Non-viable relationship:** client has requested services outside Dealix's scope, or the partnership has violated non-negotiable boundaries (e.g., requesting automated sends without approval).

---

## بوابة الموافقة الأولى — APPROVAL_FIRST Gate

**لا يُرسَل أي تواصل للعميل حول الإنهاء قبل موافقة المؤسس المُسجَّلة.**
**No client communication about offboarding is sent before the founder's logged approval.**

- [ ] توثيق سبب الإنهاء (واحدة من الحالات الثلاث أعلاه) في سجل المشاريع. / Document the offboarding reason (one of the three conditions above) in the engagement record.
- [ ] مراجعة المؤسس للوضع كاملاً: هل هناك خيار استبقاء لم يُجرَّب بعد؟ / Founder reviews the full situation: is there an untried retention option?
- [ ] **تسجيل موافقة المؤسس** على المضي في مسار الإنهاء. / **Log founder approval** to proceed with the offboarding path.
- [ ] تحديد المسؤول عن التواصل مع العميل في كل خطوة. / Assign the responsible person for client communication at each step.

---

## قائمة الإنهاء على 30 يوماً — 30-Day Offboarding Checklist

### اليوم 0–7: محاولة الاستبقاء — Day 0–7: Retention Attempt

هذه نافذة أخيرة للاستبقاء — ليست بيعاً بالضغط.
This is a final retention window — not a pressure sale.

- [ ] تسليم آخر حزمة إثبات مكتملة إن لم تُسلَّم بعد. / Deliver the final complete Proof Pack if not yet delivered.
- [ ] جدولة مكالمة مع صانع القرار التنفيذي: ما الذي لم يعمل؟ ما الذي يمكن تعديله؟ / Schedule a call with the executive decision-maker: what didn't work? What can be adjusted?
- [ ] إذا كان السبب تقنياً أو في نطاق الخدمة: اعرض تعديلاً محدداً بجدول زمني واضح. / If the reason is technical or scope-related: offer a specific adjustment with a clear estimated timeline.
- [ ] إذا رفض العميل الاستمرار بعد المكالمة: انتقل إلى المرحلة التالية بدون ضغط إضافي. / If the client declines to continue after the call: advance to the next phase without further pressure.
- [ ] توثيق قرار الاستبقاء أو الإنهاء في سجل المشاريع. / Document retention outcome (continue or proceed to offboard) in the engagement record.

### اليوم 7–14: تجهيز تصدير البيانات — Day 7–14: Data Export Preparation

- [ ] تجهيز ملف تصدير البيانات الكامل بصيغة JSON و CSV وفق DPA الموقَّعة. / Full data export prepared in JSON and CSV format per the signed DPA.
- [ ] التحقق من أن الملف يشمل كل البيانات التي قدّمها العميل طوال فترة التعاقد. / Verify the export includes all data the client provided throughout the engagement.
- [ ] تشفير الملف بكلمة مرور AES-256 وإعداد قناة تسليم آمنة. / File encrypted (AES-256) and secure delivery channel prepared.
- [ ] لا يُرسَل الملف بعد — ينتظر تأكيد الخطوة القانونية من الخطوة التالية. / File is not sent yet — awaiting legal confirmation from the next phase.
- [ ] توثيق قائمة تفصيلية لكل مجموعة بيانات مُصدَّرة في سجل الحوكمة. / Detailed inventory of every exported dataset documented in the governance log.

### اليوم 14–21: نقل المعرفة وإلغاء الصلاحيات — Day 14–21: Knowledge Transfer + Access Revocation Plan

- [ ] جلسة نقل المعرفة (45 دقيقة) مع العميل: شرح كيفية قراءة مخرجات حزمة الإثبات باستقلالية. / 45-minute knowledge transfer session with the client: explain how to read Proof Pack outputs independently.
- [ ] توثيق جميع عمليات الوصول النشطة (API keys، اعتمادات التكامل، صلاحيات المستخدمين). / Document all active access (API keys, integration credentials, user permissions).
- [ ] إعداد خطة إلغاء الصلاحيات: تاريخ محدد لسحب كل صلاحية. / Access revocation plan prepared: specific date for revoking each access credential.
- [ ] إرسال ملف تصدير البيانات المشفَّر للعميل. توثيق الإرسال في سجل الحوكمة. / Encrypted data export file sent to client. Delivery documented in governance log.
- [ ] تأكيد استلام العميل للملف خطياً. / Written confirmation of client's receipt of the export file obtained.

### اليوم 21–28: الفاتورة النهائية وسحب الصلاحيات وجدول الحذف — Day 21–28: Final Invoice + Access Revocation + Deletion Schedule

- [ ] إصدار الفاتورة النهائية (إن وُجدت مبالغ مستحقة) وفق معايير ZATCA المرحلة الثانية. / Final invoice issued (if any balance due) per ZATCA Phase 2 requirements.
- [ ] سحب جميع صلاحيات الوصول في التاريخ المحدد: API keys، حسابات المستخدمين، التكاملات. / All access credentials revoked on the scheduled date: API keys, user accounts, integrations.
- [ ] إشعار العميل بجدول حذف البيانات: الحذف التام يتم في اليوم 60 من بدء الإنهاء وفق PDPL. / Client notified of data deletion schedule: full deletion occurs on Day 60 of offboarding per PDPL.
- [ ] الاحتفاظ بسجلات الحوكمة (governance logs) وفق جدول الاحتفاظ القانوني (24 شهراً لسجلات التدقيق). / Governance logs retained per legal retention schedule (24 months for audit logs).

### اليوم 28–30: إغلاق سجل الحوكمة وملاحظات ما بعد المشروع — Day 28–30: Governance Log Closure + Post-Mortem Notes

- [ ] إغلاق سجل المشروع بشكل رسمي: تحديث الحالة إلى `status=offboarded` في سجل المشاريع. / Engagement record formally closed: status updated to `status=offboarded` in engagement registry.
- [ ] كتابة ملاحظات ما بعد المشروع: ما الذي سار جيداً؟ ما الذي لم يسر جيداً؟ أي إشارة مبكرة أُهملت؟ / Post-mortem notes written: what worked? What didn't? Which early signal was missed?
- [ ] تحديث حالة سجل الحوكمة: كل المهام مكتملة، التواريخ مُسجَّلة، المسؤوليات موثَّقة. / Governance log status updated: all tasks complete, dates recorded, responsibilities documented.
- [ ] جدولة تاريخ تنفيذ الحذف التام للبيانات (اليوم 60) في النظام. / Data deletion date (Day 60) scheduled in the system.

---

## التزامات البيانات (PDPL) — Data Obligations per PDPL

| الالتزام | الجدول الزمني | ملاحظة |
|---|---|---|
| إعادة بيانات العميل الكاملة | اليوم 14–21 من بدء الإنهاء | JSON + CSV مشفَّر |
| حذف بيانات العميل من الأنظمة الأساسية | اليوم 60 من بدء الإنهاء | حذف تام، لا إخفاء هوية فقط |
| الاحتفاظ بسجلات الحوكمة | 24 شهراً من تاريخ الإغلاق | وفق جدول احتفاظ سجلات التدقيق |
| الاحتفاظ بسجلات المالية والعقود | 7 سنوات من انتهاء العقد | قانون ضريبة القيمة المضافة السعودي + ZATCA |

| Obligation | Timeline | Note |
|---|---|---|
| Return all client data | Day 14–21 of offboarding start | Encrypted JSON + CSV |
| Delete client data from primary systems | Day 60 of offboarding start | Hard delete, not anonymisation only |
| Retain governance logs | 24 months from closure date | Per audit log retention schedule |
| Retain financial records and contracts | 7 years from contract end | Saudi VAT law + ZATCA |

---

## طلب الإحالة — Referral Ask

حتى في مرحلة الإنهاء، الباب مفتوح للتوصية. هذا السؤال يُطرح مرة واحدة، بدون ضغط، في مكالمة نقل المعرفة (اليوم 14–21).
Even during offboarding, a referral ask is appropriate. It is asked once, without pressure, during the knowledge transfer session (Day 14–21).

"هل تعرف شركة أخرى تعاني من نفس التحديات في جودة البيانات أو تسريبات الإيرادات؟ سنكون سعيدين بتقديم التشخيص المجاني لها."

"Do you know another company facing the same challenges in data quality or revenue leakage? We would be glad to offer them the free diagnostic."

---

## تحليل الإلغاء — Churn Analysis

تحليل الإلغاء إلزامي لكل حالة إنهاء. يُعبأ في سجل ما بعد المشروع بالمكوّنات الأربعة:
Churn analysis is mandatory for every offboarding. It populates the post-mortem with four components:

1. **الإشارة المُهملة:** هل كانت هناك علامات مبكرة على عدم الرضا؟ متى ظهرت؟ / **Missed signal:** Were there early signs of dissatisfaction? When did they appear?
2. **العامل الجذري:** هل السبب في الجودة، النطاق، التوقعات، أم العوامل الخارجية؟ / **Root cause:** Was the cause quality, scope, expectations, or external factors?
3. **خط منع التكرار:** ما الإجراء المُضاف للعملية لمنع نفس السبب مستقبلاً؟ / **Prevention line:** What process addition prevents the same cause in future?
4. **تسجيل النمط:** إضافة النمط الموحَّد (مجهول الهوية) إلى سجل أنماط الإلغاء. / **Pattern registration:** Add the anonymised pattern to the churn pattern log.

---

## سياسة إعادة الانضمام — Re-Engagement Policy

الإنهاء ليس إغلاقاً دائماً. العميل الذي ألغى يمكنه إعادة البدء بسبرنت جديد في أي وقت.
Offboarding is not a permanent closure. A cancelled client can restart with a new Sprint at any time.

الشرط الوحيد: اتفاقية معالجة بيانات جديدة (DPA) وجواز مصدر جديد قبل استيراد أي بيانات.
The only condition: a new DPA and new Source Passport before any data is imported.

يُبلَّغ العميل بهذا الخيار صراحةً في رسالة الإغلاق النهائية.
The client is explicitly informed of this option in the final closure message.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
