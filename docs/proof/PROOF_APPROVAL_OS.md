# Proof Approval OS

The Proof Approval OS is the gate that decides whether evidence about Dealix work may be published, shown to a prospect, or referenced in a proposal. Nothing about a real customer leaves Dealix without passing this gate.

**Source of truth:** `$PRIVATE_OPS/proof_approval_log.csv`
**Owner:** Founder
**Trust gate:** A2 — proof publishing is one of the protected founder-only decisions.

## Categories of proof

| Category | Example | Default visibility |
|----------|---------|--------------------|
| Public case study | Named client, verified metrics | Public after written consent |
| Case-safe summary | Anonymised pattern | Public; no PII; no re-identifiable metric |
| Internal artifact | Working deliverable | Private; never external |
| Investor proof pack | Aggregated portfolio metrics | Selective; under NDA |
| Sector pattern | Aggregated multi-client pattern | Public; no client identifiable |

## Process

1. Producer (Customer Success, Delivery, or Marketing) drafts the proof artifact.
2. Provenance check: every claim traces to a source in `docs/04_data_os/DATA_PROVENANCE.md`.
3. PII scan: zero PII (see `docs/04_data_os/PII_CLASSIFICATION.md`).
4. Claim-safety lint (`docs/marketing/COPYWRITING_RULES.md`).
5. If the artifact names a client, written consent must exist on file and be current.
6. Bilingual EN + AR parity check.
7. Founder approves at A2. Approval is logged with `approved_by`, `approved_at`, `scope` (where it may be used), `expires_at`.
8. Artifact is published or distributed.

## Consent

Client consent is collected on a standard form (EN + AR) that names:

- The exact artifact wording.
- Where it may be used.
- The duration of consent.
- The client's right to revoke.

Consent is stored in `$PRIVATE_OPS/consent_records/` with checksum. A revocation pulls the artifact within 5 business days.

## Anonymisation standard

A case-safe summary anonymises:

- Client name and trading name.
- Logo and brand colours.
- Sector if the sector has fewer than 20 plausible candidates in the relevant region.
- Metrics if a metric range would reverse-identify the client.

The standard lives in `docs/07_proof_os/CASE_SAFE_SUMMARY.md`.

## Failure modes

- **Stale consent:** an artifact is in market past its expiry. Detection: nightly job. Recovery: pull, re-obtain consent.
- **PII leak:** a published artifact contains a name or contact. Detection: scan, or client report. Recovery: pull within 24 hours, written apology, root cause filed.
- **Estimate published as verified:** a metric labelled Verified is actually Estimated. Detection: monthly audit against Value Ledger. Recovery: pull, re-label, re-publish if appropriate.

## Recovery path

If proof governance is in doubt (consent records lost, provenance broken), the founder pauses all external proof publication until governance is restored. Existing public artifacts are reviewed under a 5-business-day window.

## Metrics

- Proof artifacts approved this quarter.
- Median time from draft to approval.
- Consent revocations per year.
- PII-leak incidents per year (target: 0).

## Disclaimer

Proof reflects past, specific engagements. Published metrics are clearly tagged Estimated or Verified. Dealix does not guarantee future outcomes. Estimated value is not Verified value.
