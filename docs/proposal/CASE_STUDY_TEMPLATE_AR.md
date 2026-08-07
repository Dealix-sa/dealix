# Case Study Template

> **Status:** Used only after client permission.
> **Schema:** `schemas/launch/proof_pack.schema.json` (the case_study variant).
> **Companion:** `PROOF_PACK_TEMPLATE_AR.md` + `BEFORE_AFTER_TEMPLATE_AR.md`.

## The structure (4 sections, max 2 pages)

### 1. The client (anonymized unless permission)

- Industry + city + size range.
- The decision maker (anonymized unless permission).
- The trigger: what made them reach out.

### 2. The before (1 page)

- The pain: specific, named, dated.
- The leak: the cost they were incurring.
- The metric (if measurable): "X leads per week" or "Y hours per day".

### 3. The after (1 page)

- The intervention: which offer(s) from the ladder.
- The duration: how long it took.
- The result: the new metric, with proof.
- The surprise: something they did not expect.

### 4. The founder quote (with permission)

- 1–3 sentences, in the client's words.
- The signature (name + role) — only with permission.

## The hard rules

1. **Client name** only with written permission.
2. **Client logo** only with written permission.
3. **Decision maker name** only with written permission.
4. **Numbers** must be real and verifiable.
5. **Time-bound:** the case study is dated. If the result is older than 12 months, refresh or retire.
6. **Anonymized** is the default.

## The permission record

```json
{
  "permission_id": "perm_001",
  "case_study_id": "case_2024_agency_001",
  "client_name": "Agency X",
  "decision_maker_name": "Sara",
  "logo_allowed": true,
  "name_allowed": true,
  "quote_allowed": true,
  "granted_at_iso": "2024-12-01",
  "expires_iso": "2025-12-01",
  "revocable": true,
  "source": "signed_consent_record"
}
```

If the permission is missing or expired, the case study is treated as anonymized.

## The first case study

The first case study is the hardest because:

- The client may not want to be named.
- The numbers are still fresh and may change.
- The case study may turn into a "failure case" later.

Approach:

- Get the permission BEFORE you write the case study.
- Use anonymized excerpts if the permission is not yet signed.
- Re-approve the case study 90 days later, when the result is stable.

## When to write a case study

- After a successful pilot (the client has seen the value).
- After a successful renewal (the client is committed long-term).
- After a measurable improvement (a specific metric moved).

Do not write a case study:

- After a one-off audit (not enough data).
- After a failed pilot (write an internal post-mortem, not a case study).
- Before the client has signed off.

## The library

The case studies live in `data/launch/case_studies/<case_id>.md` (Markdown for readability) with a parallel `<case_id>.json` (machine-readable, with permission, evidence_level, and the proof pack fields).

## When to update

- Every new successful engagement = new case study.
- Every 6 months = review for expiry.
- Every loss of permission = anonymize or remove.
