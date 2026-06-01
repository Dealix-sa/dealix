# Incident Response Playbook — دليل الاستجابة للحوادث

**Version:** 1.0 | **Owner:** Founder | **Effective Date:** 2026-06-01 | **Review:** Annually

Cross-links: [DATA_HANDLING_POLICY.md](DATA_HANDLING_POLICY.md) | [AI_USAGE_POLICY.md](AI_USAGE_POLICY.md) | [HUMAN_APPROVAL_MATRIX.md](HUMAN_APPROVAL_MATRIX.md) | [../delivery/RISK_REGISTER_TEMPLATE.md](../delivery/RISK_REGISTER_TEMPLATE.md)

---

## Severity Levels — مستويات الخطورة

| Level — المستوى | Definition — التعريف | Examples — أمثلة |
|---|---|---|
| **P0 — Critical** | Active breach or loss of client data. Legal or regulatory consequences likely. Client operations may be affected. | Unauthorized access to client production system, confirmed data exfiltration, credentials leaked publicly |
| **P1 — High** | Potential breach or significant system failure. Client operations at risk. Immediate action needed. | API key exposed in code commit, client data found in incorrect storage location, complete system outage affecting live client |
| **P2 — Medium** | Operational failure or AI output error. No breach but delivery quality affected. | AI model produces incorrect outputs delivered to client, QA system fails silently, project system goes offline temporarily |
| **P3 — Low** | Minor issue. No data risk. Delivery quality marginally affected. | Minor UI/formatting error in report, delayed notification, low-impact configuration error |

---

## Response SLAs — الأوقات المعيارية للاستجابة

| Severity | Founder Notified | Client Notified | Initial Containment | Root Cause Report |
|---|---|---|---|---|
| P0 | Immediately (< 15 min) | Within 1 hour | Within 1 hour | Within 72 hours |
| P1 | Within 1 hour | Within 24 hours | Within 4 hours | Within 5 business days |
| P2 | Within 4 hours | If delivery affected: within 24 hours | Within 24 hours | Within 5 business days |
| P3 | Same day | If client-visible: within 48 hours | Within 3 business days | At next project review |

---

## Incident Types and Response Steps — أنواع الحوادث وخطوات الاستجابة

### Type 1 — Data Breach | اختراق البيانات

**Definition:** Any confirmed or suspected unauthorized access to, disclosure of, or loss of client data.

**Steps:**

1. **Stop:** Immediately suspend the affected system, access, or data transfer. Do not delete anything.
2. **Notify Founder:** Within 15 minutes for P0, within 1 hour for P1. Message: "Possible data breach — [system/data] — [what was observed]."
3. **Scope assessment:** Founder and relevant team member determine: which data was involved, who had access, how long the exposure lasted, how it was discovered.
4. **Contain:** Revoke compromised credentials. Isolate affected system. Secure remaining data.
5. **Notify Client:** Founder notifies client contact directly — within 1 hour for P0, within 24 hours for P1. Message template below.
6. **Document:** Record incident in incident register — what happened, when, scope, containment actions.
7. **PDPL notification:** If Saudi personal data is involved, assess PDPL regulatory notification requirements.
8. **Root cause and remediation:** Identify the cause. Implement fix. Confirm fix before resuming operations.

**Client notification template — قالب إشعار العميل:**

*EN:* "We are writing to inform you of a [potential / confirmed] security incident affecting [description of data]. We identified this on [date/time]. We have taken the following immediate steps: [containment actions]. We are continuing to investigate and will provide a full report within [X] hours/days. Your designated contact at Dealix is [Founder role]."

*AR:* "نكتب لإطلاعكم على حادثة أمنية [محتملة / مؤكدة] تتعلق بـ [وصف البيانات]. اكتشفنا ذلك في [التاريخ والوقت]. اتخذنا الإجراءات الفورية التالية: [إجراءات الاحتواء]. نواصل التحقيق وسنقدم تقريراً كاملاً خلال [X] ساعة/يوم. نقطة اتصالكم في ديليكس هي [دور المؤسس]."

---

### Type 2 — AI Output Error | خطأ مخرجات الذكاء الاصطناعي

**Definition:** An AI agent produces an incorrect, misleading, or harmful output that was or could have been delivered to a client.

**Steps:**

1. **Stop delivery:** If output has not been sent to client — halt. If sent — identify exactly what was received.
2. **Assess impact:** Was the output acted on? Did it affect a client decision, action, or process?
3. **Notify Founder:** Include: what was output, what was correct, how the error occurred.
4. **Notify Client:** If the incorrect output reached the client and may have influenced any action — notify within 24 hours and provide the corrected output.
5. **Investigate:** Which prompt, data, or system condition caused the error? Is it repeatable?
6. **Fix:** Correct the prompt, data quality issue, or system configuration. Test fix before resuming.
7. **Document:** Record in incident register. Add to quality checklist if the error pattern is systemic.

---

### Type 3 — System Outage | توقف النظام

**Definition:** A Dealix-built client system becomes unavailable or non-functional.

**Steps:**

1. **Notify Founder:** Immediately on detection.
2. **Assess:** Is this a Dealix-side issue (code/hosting) or a dependency issue (client API, third-party service)?
3. **Notify Client:** P0/P1: within 1 hour. P2: within 4 hours. Include estimated resolution time.
4. **Restore:** Restore service using last known-good configuration if root cause not yet identified.
5. **Root cause:** Once restored, investigate and document root cause.
6. **Prevention:** Update [../delivery/RISK_REGISTER_TEMPLATE.md](../delivery/RISK_REGISTER_TEMPLATE.md) with mitigation.

---

### Type 4 — Client Complaint | شكوى العميل

**Definition:** Client raises a formal objection about delivery quality, timeline, communication, or conduct.

**Steps:**

1. **Acknowledge:** Respond to client within 4 hours — acknowledge receipt, do not defend or minimize.
2. **Notify Founder:** Immediately.
3. **Investigate:** What specifically is the complaint? Is it factually accurate? What is the gap between expectation and delivery?
4. **Meet:** Schedule a call with the client within 24-48 hours to hear the complaint in full.
5. **Respond formally:** Provide Dealix's assessment and proposed resolution in writing within 3 business days.
6. **Resolve or escalate:** If agreeable resolution found — document and implement. If dispute remains — refer to SOW dispute resolution clause.
7. **Learn:** What process gap caused this? Update the relevant SOP, template, or checklist.

---

## Incident Register — سجل الحوادث

Maintain a running log. Do not delete entries.

| Incident ID | Date | Type | Severity | Project | Description | Status | Root Cause | Resolved Date |
|---|---|---|---|---|---|---|---|---|
| INC-[YYYY]-001 | [Date] | [Type 1-4] | [P0-P3] | [Project label] | [Brief description] | [Open/Closed] | [Root cause] | [Date or Open] |

---

## Post-Incident Review — مراجعة ما بعد الحادثة

For every P0 and P1 incident, a post-incident review is completed within 5 business days:

- What happened? (factual timeline)
- What was the impact? (client, data, project)
- What did we do well in response?
- What should we have done differently?
- What specific changes to process, tooling, or policy will prevent recurrence?

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
