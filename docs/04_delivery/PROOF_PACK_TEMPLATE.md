# Proof Pack Template / قالب حزمة الإثبات

**Use:** copy this file into `clients/<customer>/proof_pack.md` for each
engagement. Standard: [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md).

> **Two flavors:** `internal_only` (any event lacks consent) vs
> `public_with_consent` (every event has `consent_for_publication=True` **and**
> founder approval recorded). Default audience = `internal_only`.

---

## 0. Pack metadata / بيانات الحزمة

| Field | Value |
|---|---|
| Engagement ID | `<engagement_id>` |
| Customer | `<customer>` |
| Audience | `internal_only` \| `public_with_consent` |
| Approval status | `approval_required` (until founder approves) |
| Proof score | `<0-100>` (must be ≥ 70 to deliver) |
| Date assembled | `<YYYY-MM-DD>` |
| Disclaimer | Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة |

---

## The 14 required sections / الأقسام الـ14 المطلوبة

Each section is mandatory; a missing section fails assembly.

1. **Intake** — what the customer asked for / ما طلبه العميل.
2. **Source Passport** — `owner`, `source_type` (`client_upload` / `crm_export`
   / `manual_entry` — never `scraped`), `allowed_use`, `pii_flag`,
   `sensitivity`, `retention_days`.
3. **Data Quality (DQ) score** — 6 dimensions: completeness, validity,
   uniqueness, consistency, timeliness, conformance.
4. **Dedupe** — duplicates found / removed.
5. **Scoring** — qualification scores + framework (BANT / MEDDPICC).
6. **Drafts** — drafted outputs (all `approval_required`).
7. **Governance decisions** — approved / blocked / redacted counts.
8. **Redactions** — what was redacted and why (PII).
9. **Approvals** — who approved, when (founder).
10. **Value-tier mapping** — Proof → measurable value tier.
11. **Capital asset registration** — data asset registered (Capital OS).
12. **Limitations** — honest caveats; what this does **not** prove.
13. **Methodology** — how each number was produced; `~` marks estimates.
14. **Signatures** — founder + (optional) customer; HMAC-SHA256 metadata sig.

---

## Estimates vs measurements / التقديرات مقابل القياسات

- `MEASURED` numbers: plain, with the event/ledger source.
- `ESTIMATE` numbers: prefixed `~`, with the disclaimer on the same page.

---

## Publish gate / بوابة النشر

```text
every event consent_for_publication = True
            AND
founder approval recorded in approval_center
            ⇩
ONLY THEN may this pack appear on a public surface
```

If either is missing → `audience = internal_only`, no external use.
