# Incident & Complaint Process — معالجة الحوادث والشكاوى

How Dealix responds when something goes wrong: a complaint, a spam report, a deliverability problem, or a data incident. Fast, honest, logged, and resolved.

كيف يستجيب ديليكس عند حدوث خطأ: شكوى، بلاغ بريد مزعج، مشكلة تسليم، أو حادثة بيانات. سريع وصادق ومُسجَّل ومُعالَج.

## What counts as an incident — ما يُعدّ حادثة

- A recipient complaint or spam report.
- Spam rate at or near 0.3% in Google Postmaster.
- A rising bounce or deliverability drop.
- A suspected data breach or PII exposure.
- A "do not contact" request not honored in time.

## Immediate response — الاستجابة الفورية

1. **Pause.** Hold the outreach ramp. See [02_MANUAL_OUTREACH_RAMP.md](02_MANUAL_OUTREACH_RAMP.md).
2. **Suppress.** Add the complainant to the suppression list immediately. See [03_SUPPRESSION_PROCESS.md](03_SUPPRESSION_PROCESS.md).
3. **Acknowledge.** Reply to the complainant honestly within one business day; no defensiveness, no fabricated excuses.
4. **Contain.** For a data incident, contain access and assess scope before anything else.

## Complaint handling — معالجة الشكاوى

- Honor the request fully: stop contact, suppress, confirm.
- If the complaint is about a claim, check it against claim safety. See [../05_governance_os/CLAIM_SAFETY.md](../05_governance_os/CLAIM_SAFETY.md).
- Record the complaint, the response, and the resolution.

## Data incident handling — معالجة حوادث البيانات

- Contain, then assess what data and whose.
- Follow the DPA breach-notification obligations. See [04_PRIVACY_LEGAL_READINESS.md](04_PRIVACY_LEGAL_READINESS.md).
- Notify affected clients per the agreement and PDPL-aware obligations.

## Incident log schema — مخطط سجل الحادثة

```json
{
  "incident_id": "string",
  "type": "complaint | spam_report | deliverability | data_incident | suppression_failure",
  "opened_at": "YYYY-MM-DDThh:mm:ssZ",
  "severity": "low | medium | high",
  "ramp_paused": true,
  "action_taken": "string",
  "resolved_at": "YYYY-MM-DDThh:mm:ssZ | null",
  "logged_by": "founder@dealix.sa"
}
```

## Resume conditions — شروط الاستئناف

Resume the ramp only when: the cause is fixed and verified; suppression is confirmed; spam and bounce rates are healthy; and the incident is logged as resolved.

## Reporting — الإبلاغ

Open and resolved incidents feed `safety_violations` and `compliance_rejections` where applicable, and appear in the monthly board report. See [../analytics-os/04_MONTHLY_BOARD_REPORT.md](../analytics-os/04_MONTHLY_BOARD_REPORT.md).

## Boundaries — الحدود

No automated external response. Every reply to a complainant is reviewed and sent manually. No fabricated reassurance; only what is true.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
