# Dealix — Sample Incident Response Playbook — دليل الاستجابة للحوادث (نموذج)

> Bilingual playbook for AI agent misbehavior. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الغرض
يضع هذا الدليل إجراءات الاستجابة عندما يتصرّف وكيل AI خارج النطاق المُعلَن، أو يُولّد مخرجًا ضارًا، أو يخرق سياسة.

### تعريف الحادث
- إرسال خارجي بدون موافقة.
- استخدام أداة من `denied` في مصفوفة الصلاحيات.
- تسرّب PII في سجل أو مخرج.
- مخرج يحتوي على معلومات مفبركة دون مصدر.
- اختراق أمني محتمل أو فعلي.

### مستويات الحدّة
- **S1 (حرج)** — تسرّب PII أو إرسال خارجي مُنفَّذ.
- **S2 (مرتفع)** — استخدام أداة ممنوعة أو خرق سياسة دون أثر خارجي.
- **S3 (متوسط)** — انحراف Agent Registry أو Tool Permission Matrix.
- **S4 (منخفض)** — مخرج غير مرغوب لكن مُحتوى داخليًا.

### الاستجابة (T+0 → T+72h)
- **T+0 إلى T+1h**: اكتشاف عبر AI Run Ledger أو بلاغ بشري. تشغيل kill-switch للوكيل المعني.
- **T+1h إلى T+4h**: تجميد Tool Permission Matrix للوكيل. حفظ Evidence Pack الحادث.
- **T+4h إلى T+24h**: تحقيق سببي. إخطار DPO إذا كان S1. إخطار العميل المُتأثّر.
- **T+24h إلى T+72h**: تقرير حادث رسمي مع جذر السبب وخطّة تصحيح. مراجعة Agent Registry. تحديث سياسة إذا لزم.

### الأدوار
- **مستجيب أوّل** — مسؤول الحوكمة.
- **مالك الوكيل** — يفسّر النية والـ context.
- **DPO** — مسؤول PDPL والإخطار الخارجي.
- **المؤسس** — يوقّع على أي إجراء يمس عميلًا.

### الإخطار الخارجي
- خرق بيانات شخصية → خلال 24 ساعة (PDPL).
- إجراء خارجي غير مُصرَّح به → فورًا للعميل المُتأثّر.
- لا إخطار علني قبل اكتمال التحقيق.

### مخرجات ما بعد الحادث
- تحديث Agent Registry.
- تحديث Tool Permission Matrix.
- تحديث AI Use Policy إذا كشف الحادث ثغرة سياسة.
- إدخال في AI Run Ledger يربط الحادث بالتصحيح.

---

## English

### Purpose
This playbook defines the response when an AI agent acts outside declared scope, generates harmful output, or violates a policy.

### Incident Definition
- External send without approval.
- Use of a `denied` tool from the permission matrix.
- PII leakage in a log or output.
- Output containing fabricated information without a source.
- Suspected or actual security breach.

### Severity Levels
- **S1 (critical)** — PII leak or external send executed.
- **S2 (high)** — denied tool used or policy breach without external impact.
- **S3 (medium)** — Agent Registry or Tool Permission Matrix drift.
- **S4 (low)** — unwanted output contained internally.

### Response Timeline (T+0 → T+72h)
- **T+0 to T+1h**: detection via AI Run Ledger or human report. Trigger kill-switch for the agent.
- **T+1h to T+4h**: freeze the Tool Permission Matrix for the agent. Preserve the incident Evidence Pack.
- **T+4h to T+24h**: causal investigation. Notify DPO if S1. Notify affected customer.
- **T+24h to T+72h**: formal incident report with root cause and remediation plan. Review Agent Registry. Update policy if required.

### Roles
- **First responder** — governance lead.
- **Agent owner** — explains intent and context.
- **DPO** — owns PDPL and external notification.
- **Founder** — signs off on any action affecting a customer.

### External Notification
- Personal data breach → within 24 hours (PDPL).
- Unauthorized external action → immediately to the affected customer.
- No public notice before investigation is complete.

### Post-Incident Outputs
- Agent Registry update.
- Tool Permission Matrix update.
- AI Use Policy revision if a policy gap is found.
- AI Run Ledger entry linking the incident to its remediation.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
