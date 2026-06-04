# Manual Outreach Ramp — التدرّج اليدوي في التواصل

A slow, manual ramp that protects sender reputation. Volume increases only when authentication holds and the spam rate stays under 0.3%. Every message is sent by hand after founder approval.

تدرّج بطيء يدوي يحمي سمعة المُرسِل. يزيد الحجم فقط عند ثبات المصادقة وبقاء معدل البريد المزعج تحت 0.3%. كل رسالة تُرسَل يدويًا بعد موافقة المؤسس.

## Principle — المبدأ

The ramp governs how many manual messages the founder sends per day. The system never sends; it only drafts and ranks. This document caps human volume to protect reputation.

## Ramp schedule (manual sends per day) — جدول التدرّج

The numbers below are a conservative starting frame, not a target to rush. Hold each step until the gate conditions pass.

| Week | Suggested daily cap | Advance only if |
|---|---|---|
| 1 | Low (single digits) | SPF/DKIM/DMARC pass; 0 spam complaints |
| 2 | Slightly higher | Spam rate < 0.3%; bounce rate low |
| 3 | Higher | Replies healthy; suppression honored |
| 4+ | Step up gradually | All gates green for the prior full week |

Treat the caps as ceilings, not quotas. Quality of targeting beats volume.

## Advance conditions — شروط التقدّم

Advance to the next step only when all hold for the prior week:

- Spam rate under 0.3% in Google Postmaster.
- Bounce rate low and stable.
- No suppression-list violation.
- No complaint open. See [06_INCIDENT_AND_COMPLAINT_PROCESS.md](06_INCIDENT_AND_COMPLAINT_PROCESS.md).

## Pause conditions — شروط الإيقاف

Pause the ramp and hold volume if any occurs:

- Spam rate reaches or approaches 0.3%.
- Bounce rate rises.
- A complaint is received.
- DMARC reports show alignment failures.

Resume only after the cause is fixed and verified.

## Targeting discipline — انضباط الاستهداف

- Only contacts with a legitimate basis to be contacted; no scraped or purchased lists.
- Relevant, specific, bilingual where appropriate. No fabricated urgency.
- Each message references the approved message library, not improvised claims.

## Boundaries — الحدود

- AI drafts and ranks; the founder reviews, approves, and sends manually.
- The system never sends externally and never schedules automated sends.
- Every send is logged: recipient basis, approval, timestamp.

## Related — مراجع

- Auth setup: [01_DOMAIN_EMAIL_READINESS.md](01_DOMAIN_EMAIL_READINESS.md)
- Suppression: [03_SUPPRESSION_PROCESS.md](03_SUPPRESSION_PROCESS.md)
- Channel policy: [../05_governance_os/CHANNEL_POLICY.md](../05_governance_os/CHANNEL_POLICY.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
