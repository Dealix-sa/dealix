# سياسة الاحتفاظ بالبيانات — Data Retention Policy

> **القاعدة / The Rule:** بيانات العميل ملك للعميل — لا تُستخدم لتدريب النماذج، وتُحذف عند الطلب.
> **Customer data belongs to the customer. It is never used to train models. It is deleted on request.**

Canonical: `CLAUDE.md` Hard rules, `docs/00_constitution/NON_NEGOTIABLES.md`,
`docs/00_constitution/WHAT_DEALIX_REFUSES.md`. PDPL framing shared with `NO_SPAM_POLICY.md`.

## التدريب / Model training

- **Customer data is never used to train, fine-tune, or improve any AI model** — Dealix's or a third party's.
- Customer data is processed **only** to deliver the service the customer engaged us for.
- Any aggregate/benchmarking insight must be fully de-identified and is still opt-in; it never exposes raw customer data.

## جواز المصدر والاستخدام المسموح / Source Passport & allowed-use

Every dataset Dealix holds carries a **Source Passport**:

| Field | Description |
|---|---|
| `source` | Where the data came from (customer upload, integration, public source) |
| `lawful_basis` | Consent / contract / legitimate documented relationship (PDPL-aligned) |
| `allowed_use` | The specific purposes permitted (e.g. "Sprint delivery only") |
| `forbidden_use` | Always includes: model training, resale, cross-customer reuse |
| `retention_window` | How long it is kept (see below) |
| `owner` | Accountable person |

Data may only be used within its `allowed_use`. No scraping behind login or of personal data ever enters the system
(see `NO_SPAM_POLICY.md`).

## نوافذ الاحتفاظ / Retention windows

| Data class | Default retention | Notes |
|---|---|---|
| Active engagement data (Sprint/project) | Duration of engagement + 12 months | For continuity and Proof Pack support |
| Proof Packs & deliverables | 24 months or contract term | Evidence backing `CLAIMS_REGISTER.md` |
| Leads / funnel submissions | 12 months from last contact | Then deleted or anonymized |
| Decision Passport / approval logs | 24 months (audit) | Immutable; supports `HUMAN_APPROVAL_POLICY.md` |
| Operational/system logs | 90 days | Security and debugging |

Windows are maximums. Data not needed is deleted earlier. Contractual terms may shorten these.

## الحذف عند الطلب / Deletion on request

- A customer may request deletion of their data at any time.
- We honor deletion within **30 days**, except where law requires retention (e.g. financial/invoice records).
- Deletion includes derived artifacts unless they are required, de-identified evidence.
- Opt-out and "stop contact" requests are honored immediately (`NO_SPAM_POLICY.md`).

## المعالجون الفرعيون / Subprocessors

- A current list of subprocessors (hosting, AI model providers, email/WhatsApp delivery) is maintained and available on request.
- Subprocessors are bound by equivalent **no-training** and confidentiality terms.
- New subprocessors require founder approval before any customer data flows to them.

## إطار PDPL / PDPL-aware framing

Aligned with Saudi PDPL: lawful basis, purpose limitation, data minimization, data residency where required,
breach notification, and the data subject's rights to access, correct, object, and delete.
