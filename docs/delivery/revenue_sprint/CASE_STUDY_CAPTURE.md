---
title: Case Study Capture
owner: Delivery Lead
status: active
last_review: 2026-05-23
---

# Case Study Capture — التقاط دراسة الحالة

## Purpose

How Dealix turns a finished sprint into a case-safe summary without leaking the buyer. Consent first. Redact second. Publish last.

## Sequence

1. **Consent.** Request post-handover, never before. Written, time-bound, revocable.
2. **Capture.** Pull the operational facts: scope, time, output counts, what was used.
3. **Redact.** Remove names, contacts, exact figures tied to the named buyer.
4. **Frame.** Use approved language ([docs/trust/SAFE_LANGUAGE_LIBRARY.md](../../trust/SAFE_LANGUAGE_LIBRARY.md)).
5. **Approve.** A2 minimum; A3 if any revenue or compliance claim.
6. **Publish or shelve.** Buyer reviews the final draft if they consented to being named; otherwise the case-safe template ships labeled "Hypothetical / case-safe template" or "Anonymized — consent on file."

## Consent template

Sent after the handoff note, never as part of the original engagement:

```
Subject — Optional: case capture for {{client_name}}

We learned useful patterns during your sprint. With your consent, we would like to capture a short summary for our records and potential future publication.

Two consent levels you can pick from:

A) Anonymized only — we use the patterns; no name, sector specifics, or numbers tied to you appear externally.
B) Named — your company name may appear in a case study, after you review and approve the final draft.

You can decline both. Either way, the operational evidence pack remains private to us per our terms.

Reply with A, B, or "decline." This consent expires in 12 months and you may withdraw any time.
```

AR version sent in parallel.

## What goes into an anonymized case-safe summary

- Sector descriptor (one level of abstraction up if needed).
- Geography descriptor (region, not city) unless city is essential to context.
- Tier delivered.
- Number of opportunities surfaced (banded if necessary).
- One pattern Dealix learned that other operators can use.
- Estimated value framing.
- The label "Hypothetical / case-safe template."

## What never appears in a public case study without explicit consent

- Company name, logo, or identifying details.
- Founder or buyer names.
- Specific revenue figures.
- Verbatim buyer quotes (paraphrase + label as paraphrase).
- Internal metrics, MRR, or pipeline value.

## Redaction checklist

- [ ] Company name removed or replaced with sector label.
- [ ] Personal names removed.
- [ ] Any number tied to the buyer banded or removed.
- [ ] Source links generalized (sector type, not the specific source).
- [ ] AR + EN versions parallel.
- [ ] Final line includes: "Estimated value is not Verified value."

## Storage

- Consent file: `dealix-ops-private/consents/<sprint_id>.md`.
- Draft case study: in the public repo only after A2 approval, in [docs/case-studies/](../../case-studies/) (if directory exists) or labeled clearly.

## Cross-links

- [HANDOFF_TEMPLATE.md](./HANDOFF_TEMPLATE.md)
- [docs/trust/PUBLIC_PRIVATE_BOUNDARY.md](../../trust/PUBLIC_PRIVATE_BOUNDARY.md)
- [docs/trust/NO_OVERCLAIM_POLICY.md](../../trust/NO_OVERCLAIM_POLICY.md)
- [docs/07_proof_os/CASE_SAFE_SUMMARY.md](../../07_proof_os/CASE_SAFE_SUMMARY.md)

## Owner & cadence

- Delivery Lead. Reviewed quarterly. Consent template legally reviewed annually.

## AR — ملخّص

التقاط القصة بعد التسليم لا قبله: موافقة مكتوبة وقابلة للسحب، ثم التقاط الحقائق التشغيلية، ثم تنقية الأسماء والأرقام والاقتباسات، ثم صياغة بلغة آمنة، ثم موافقة A2 (أو A3 لأي ادّعاء إيراد أو امتثال). الملخّص العام يحمل ملصق "نموذج افتراضي / مُجمَّع آمن" أو "مُجمَّع — موافقة محفوظة" حسب مستوى الإذن. القيمة التقديرية ليست قيمة مُتحقَّقة.
