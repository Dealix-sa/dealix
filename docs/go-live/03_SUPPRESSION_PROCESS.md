# Suppression Process — عملية الاستبعاد

The suppression list is the do-not-contact record. It is checked before every send and updated immediately on any signal to stop. No address on the list is ever contacted again.

قائمة الاستبعاد هي سجل "عدم التواصل". تُفحَص قبل كل إرسال وتُحدَّث فورًا عند أي إشارة للتوقف. لا يُعاد التواصل مع أي عنوان عليها أبدًا.

## What goes on the list — ما يُضاف للقائمة

- Any explicit unsubscribe or opt-out request.
- Any complaint or spam report.
- Every hard bounce. See [01_DOMAIN_EMAIL_READINESS.md](01_DOMAIN_EMAIL_READINESS.md).
- Any "do not contact" request received by any channel.
- Any address the founder judges should not be contacted.

## Suppression entry schema — مخطط الإدخال

```json
{
  "address": "string",
  "reason": "unsubscribe | complaint | hard_bounce | manual_request | founder_judgment",
  "added_at": "YYYY-MM-DDThh:mm:ssZ",
  "added_by": "founder@dealix.sa | system",
  "source_ref": "string",
  "permanent": true
}
```

Entries are permanent by default. Removal requires a documented, verified opt-in from the contact and founder approval.

## Pre-send check — فحص ما قبل الإرسال

Before any manual send, the recipient is checked against the suppression list. A match is a hard stop: do not send. This check is mandatory and logged.

## Update timing — توقيت التحديث

- Unsubscribe / complaint / do-not-contact: added **immediately** on receipt.
- Hard bounces: added on the next bounce sync, no later than same day.
- No batching that delays suppression.

## Honoring across channels — احترام عبر القنوات

A suppression applies across all channels, not just the one it came from. An opt-out by email also stops any other approved channel.

## Audit — التدقيق

- Every suppression entry is auditable: reason, time, source.
- Every send log records that the pre-send check passed.
- A monthly review confirms no suppressed address was contacted.

## Boundaries — الحدود

The system enforces the pre-send check but never sends. The founder confirms suppression compliance before each manual send.

## Related — مراجع

- Privacy basis: [04_PRIVACY_LEGAL_READINESS.md](04_PRIVACY_LEGAL_READINESS.md)
- Complaints: [06_INCIDENT_AND_COMPLAINT_PROCESS.md](06_INCIDENT_AND_COMPLAINT_PROCESS.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
