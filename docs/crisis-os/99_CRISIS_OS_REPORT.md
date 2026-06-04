# تقرير أدلة نظام الأزمات | Crisis OS Evidence Report

## الغرض | Purpose

**عربي:** هذا التقرير هو سجل الأدلة لنظام الأزمات في Dealix. يوثّق وجود السياسات والأدلة، ويُستخدم لتسجيل أي حادث فعلي، القرارات المتخذة، وموافقات المؤسس على الاستئناف. كل حادث يُسجّل هنا حتى يُغلق رسميًا.

**English:** This report is the evidence log for Dealix's Crisis OS. It documents the existence of policies and playbooks and is used to record any actual incident, decisions taken, and founder approvals to resume. Every incident is logged here until formally closed.

---

## المبدأ الحاكم | Governing Principle

> الذكاء الاصطناعي يُجهّز، المؤسس يوافق، الإجراء يدوي فقط، لا إرسال خارجي تلقائي.
> AI prepares, Founder approves, Manual action only, No automated external sending.

---

## جرد مكونات النظام | Component Inventory

| المكوّن Component | الملف File | الحالة Status |
|---|---|---|
| نظرة عامة Overview | `00_CRISIS_OS.md` | موجود Present |
| مفاتيح الإيقاف Kill switches | `01_KILL_SWITCH_POLICY.md` | موجود Present |
| إيقاف التواصل Outreach stop | `02_OUTREACH_STOP_POLICY.md` | موجود Present |
| الحوادث الأمنية Security | `03_SECURITY_INCIDENT_PLAYBOOK.md` | موجود Present |
| حوادث السمعة Reputation | `04_REPUTATION_INCIDENT_PLAYBOOK.md` | موجود Present |
| فشل التسليم Delivery failure | `05_CLIENT_DELIVERY_FAILURE_PLAYBOOK.md` | موجود Present |

---

## التحقق من السلامة | Safety Verification

- [x] لا إرسال آلي للبريد/واتساب/لينكدإن. No automated sending.
- [x] لا كشط بيانات. No scraping.
- [x] لا إرسال أو نشر تلقائي. No auto-submit / auto-publish.
- [x] لا إطلاق إعلانات مدفوعة حية. No live paid-ads launch.
- [x] لا أرقام وهمية ولا ضمان عائد. No fake traction / guaranteed ROI.
- [x] لا أسرار أو مفاتيح API في المخرجات. No secrets/API keys in outputs.

---

## سجل الحوادث | Incident Log

| المعرّف ID | التاريخ Date | النوع Type | الشدة Severity | الإجراء المتخذ Action | موافقة الاستئناف Resume Approval |
|---|---|---|---|---|---|
| — | — | — | — | لا حوادث مسجلة No incidents logged | — |

> يُضاف صف لكل حادث فعلي. لا يُحذف صف بعد إغلاقه (سجل دائم).

---

## نموذج إدخال حادث | Incident Entry Template

```
المعرّف ID:
التاريخ/الوقت Date/Time:
النوع Type (أمني/سمعة/تسليم/تشغيلي):
الشدة Severity (P1–P4):
الوصف Description:
المفاتيح المُفعّلة Kill switches engaged:
الأثر Impact:
السبب الجذري Root cause:
الإجراء التصحيحي Remediation:
قرار الإشعار (PDPL) Notification decision:
موافقة المؤسس على الاستئناف Founder resume approval:
الحالة Status (مفتوح/مغلق Open/Closed):
```

---

## الاستئناف | Resumption Record

- لا يُستأنف أي نشاط دون توقيع/تأكيد المؤسس مسجّل في هذا الملف.
- No activity resumes without founder confirmation recorded in this file.

> هذا الملف هو مصدر الحقيقة لجاهزية نظام الأزمات وسجل حوادثه.
