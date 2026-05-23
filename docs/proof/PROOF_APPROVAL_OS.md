# Proof Approval OS

How Dealix turns shipped outcomes into proof — with customer consent,
brand voice, and audit-ready provenance.

## 1. Proof artifact types

- Consented case study (PDF + bilingual).
- Sector pulse update that names the customer (with consent).
- Founder console screenshot (redacted).
- Quote card (one customer-approved sentence).

## 2. Consent gate

- Every proof artifact requires a `proof_consent` row from the customer.
- The row records: who consented, when, what they consented to,
  and the expiration date.
- No proof leaves Dealix without that row.

## 3. Ledgers

`revenue/proof_register.csv`:
```
proof_id,account_id,artifact_type,consent_id,consent_expires_at,
artifact_url,published_at,status (draft/approved/expired/withdrawn)
```

## 4. Publication

- Proof is **not** auto-published by Dealix.
- Publication is a deliberate founder action.
- A withdrawn or expired consent immediately moves the proof to
  `expired` and blocks any pending share drafts that reference it.

## 5. KPIs

- Proof artifacts created per quarter.
- % of closed deals that produce a proof artifact.
- Consent-coverage of every artifact in market.

## 6. Banned patterns

- ❌ Using a customer logo without consent.
- ❌ Inflated numbers.
- ❌ Composite "results" mixing multiple unnamed customers.
- ❌ Re-using proof past its consent expiration.
