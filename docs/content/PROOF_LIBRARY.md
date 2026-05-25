---
title: Proof Library
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Proof Library — مكتبة الأدلة

## Purpose
Index of every approved proof — screenshot, metric, quote, artefact — that can be referenced in customer-facing content. If a claim cannot point to a row here, the claim does not get published.

## Schema (each row)
```yaml
id: PROOF-YYYY-NNN
type: screenshot | metric | quote | artefact_link
sector: real_estate | industrial | education | healthcare | gov_adjacent | cross_sector
client_label: anonymized label or "Hypothetical / case-safe template"
title: short noun phrase
description: 1-2 sentences
source: link to original artefact in repo or storage
consent_status: anonymized_no_consent_needed | a2_written_consent_yes | a2_written_consent_yes_bounded
consent_record: link to consent message or A2 entry (if applicable)
approved_uses: linkedin | x | case_study | sector_report | proposal | deck
expiry_date: YYYY-MM-DD or "indefinite for anonymized"
created_date: YYYY-MM-DD
created_by: founder | analyst label
```

## What counts as a proof
- A screenshot of an artefact Dealix produced (with PII redacted).
- A metric value pulled from a delivery log, with the log row linked.
- A client quote, verbatim or summary, with consent record.
- A signed proposal or contract reference (counts internally only).
- A published source for a sector claim.

## What does not count
- A composite or "representative" number not tied to a row.
- A memory of a meeting without a written note.
- A screenshot edited beyond redaction.
- A quote attributed without consent and without anonymization.

## Rules
- Each proof must be reviewable. If a reviewer cannot get from the proof row to a source in <5 minutes, the row is incomplete.
- Consent-based proofs auto-expire on the consent expiry date. Expired proofs are pulled from active content.
- Anonymized proofs are indefinite unless the underlying engagement requested removal.
- PII redaction per `docs/governance/PII_REDACTION_POLICY.md` is mandatory before storage.
- Proofs used in published content must be re-linked from the published item back to the proof row.

## Operations
- New proofs added on engagement close, on weekly content review, or on sector report build.
- Monthly: founder prunes expired or no-longer-valid proofs.
- Quarterly: founder audits a random 10% of proofs to verify source links resolve.

## Evidence
- The library itself is the evidence layer.

## Owner & cadence
- Owner: Founder.
- Cadence: continuous add; monthly prune; quarterly audit.

## Cross-links
- [`CONTENT_STRATEGY.md`](CONTENT_STRATEGY.md)
- [`CASE_STUDY_SYSTEM.md`](CASE_STUDY_SYSTEM.md)
- [`SECTOR_REPORT_SYSTEM.md`](SECTOR_REPORT_SYSTEM.md)
- [`docs/governance/PII_REDACTION_POLICY.md`](../governance/PII_REDACTION_POLICY.md)

---

## القسم العربي

**الغرض:** فهرس كل دليل معتمد يمكن الاستناد إليه في المحتوى. إذا لم يربط الادعاء بصف هنا، لا يُنشر.

**مخطط الصف (أعلاه YAML):** id، نوع، قطاع، تصنيف العميل، عنوان، وصف، مصدر، حالة الموافقة، سجل الموافقة، استخدامات معتمدة، تاريخ انتهاء، إنشاء.

**يُحتسب دليلًا:** لقطة لقطعة أنتجناها (بعد تنقية PII)، قيمة مقياس مربوطة بسجل التسليم، اقتباس عميل مع موافقة، مرجع عقد موقّع (داخلي)، مصدر منشور لادعاء قطاعي.

**لا يُحتسب:** رقم "تمثيلي" بلا صف، ذاكرة اجتماع بلا ملاحظة، لقطة معدلة بأكثر من التنقية، اقتباس بلا موافقة وبلا تجهيل.

**القواعد:** كل دليل قابل للمراجعة في 5 دقائق. الموافقات المرتبطة تنتهي تلقائيًا في تاريخ الانتهاء. المجهولة دائمة ما لم يطلب العميل الإزالة. تنقية PII إلزامية قبل التخزين. المحتوى المنشور يربط للصف.

**المالك:** المؤسس. **الإيقاع:** إضافة مستمرة، تقليم شهري، تدقيق 10% ربعيًا.
