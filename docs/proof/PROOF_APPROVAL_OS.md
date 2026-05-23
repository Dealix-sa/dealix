# Proof Approval OS

> Every claim → every evidence → every customer signature → every audit entry. No exceptions.

## 1. Why this exists

Dealix's strongest distribution is **trustable proof**. Proof requires consent. A proof artifact without a stored customer consent record is a brand and trust violation — and a potential legal risk.

## 2. Lifecycle

```
Outcome delivered
    ↓
Draft proof produced (Delivery Copilot)
    ↓
Brand & accuracy QA (Delivery QA OS)
    ↓
Customer review and signature
    ↓
Consent record stored alongside artifact
    ↓
Audit event appended
    ↓
Proof published (manual)
    ↓
Routed to Proof-to-Demand Machine
```

## 3. Consent record schema

```yaml
consent_id: c_xxxx
customer_id: cust_xxxx
artifact_id: proof_xxxx
signatory_name: <human>
signatory_role: <human>
date: YYYY-MM-DD
claims_approved:
  - <claim 1>
  - <claim 2>
channels_approved:
  - landing
  - linkedin
  - sales_deck
expiry_date: YYYY-MM-DD
revocation_path: <link>
notes:
```

## 4. Forbidden

- Publishing a proof without a stored consent record.
- Editing an approved claim and re-publishing without a new signature.
- Sharing a proof in a channel not in `channels_approved`.

## 5. Storage

- Artifacts: `clients/<customer>/proof/`
- Consent: `clients/<customer>/proof/consents/`
- Public-facing copy under `docs/case-studies/` only after consent + audit.

## 6. KPI

- Consent-on-file rate for all published proof: **100 %**.
- Time from outcome to published proof (for green customers): tracked.

## 7. Trust

The Proof Approval OS reports to the Trust Center.
