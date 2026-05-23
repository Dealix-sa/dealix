# Proof Approval OS

The Proof Approval OS governs how Dealix publishes proof — case
studies, customer references, sample outputs, screenshots, named
quotes — without ever publishing without explicit, recorded approval
from the customer and the founder.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Build a library of approved, dated, attributable proof artefacts that
Dealix can use in samples, proposals, content, and outreach — without
exposing any client to risk. The OS makes proof a controlled asset.

## 2. Input

Sources:

- `delivery/sprint_log.csv` (engagement outcomes).
- `customer_success/client_health.csv` (only green-band clients are
  invited to be a named reference; others may be invited for redacted
  proof).
- `delivery/handoff_queue.csv` (completed artefacts).
- `customer_success/consent_log.csv` (consent posture per client).

Every potential proof candidate is recorded with an explicit consent
intent and a redaction posture.

## 3. Output

`proof/proof_library.csv` columns:

- `proof_id`
- `engagement_id`
- `account_id`
- `proof_type` — case_study | quote | screenshot | sample_output |
  reference_call
- `claim` — the headline factual claim made
- `metric` — the supporting metric (if any)
- `redaction_posture` — named | sector_only | fully_anonymous
- `consent_state` — none | verbal | written | revoked
- `consent_evidence_ref`
- `approval_state` — drafted | reviewed | approved | revoked
- `language` — ar | en | both
- `embedded_assets` — pipe-delimited files in `proof/{proof_id}/`
- `published_state` — internal | external_with_consent | not_published
- `last_reviewed_at`
- `reviewed_by`

`proof/proof_approval_queue.csv` mirrors the lifecycle:

- `queue_id`
- `proof_id`
- `requested_use` — sample | proposal | content | outreach | website
- `state` — drafted | reviewed | approved | rejected
- `approval_state`
- `notes`

## 4. Source of truth

`proof/proof_library.csv` for the canonical library;
`proof/proof_approval_queue.csv` for the lifecycle.

## 5. Approval class

A1 for proof intake and observation. A2 for any external use of proof.
A3 banned. Policy rule `public_proof_requires_approval` ensures that no
proof publication occurs without an approval state of `approved`.

## 6. Trust gate

- Consent integrity: no `named` or `sector_only` proof may be used
  externally without written consent recorded in
  `consent_evidence_ref`.
- Guarantee scan: no "guaranteed outcome" framing of the proof.
- Brand voice check.
- Redaction respect: drafts that use a proof must match the redaction
  posture exactly.
- Reversibility: consent may be revoked at any time; revocation
  immediately removes the proof from all queues and ledgers it
  appears in.
- Bilingual integrity (where applicable).
- Confidentiality scan: no other-customer data appears in any proof.

## 7. Owner

`proof_safety_agent` in `registries/agent_registry.yaml`. Allowed
write target: `proof/`.

## 8. Worker

`scripts/dealix_proof_approval.py` (planned). The worker:

1. Reads candidate engagements from delivery.
2. Drafts proof entries with stated redaction posture.
3. Routes for client consent (manual, by founder).
4. On consent + founder approval, sets `approval_state = approved`.
5. Maintains the queue and the trust ledger entries.
6. Triggers the Proof-to-Demand Machine when proof is freshly approved.

## 9. KPI

- Proof Library Size (approved entries).
- Approval Cycle Time (drafted -> approved).
- Bilingual Coverage (target: balanced).
- Redaction Compliance (target: 100%).
- Consent Revocation Honour (target: 100%, immediate).
- Sector Coverage (proof per active sector).

## 10. Failure mode

- Proof used without approval. Trust Guardian halts; critical incident
  opened.
- Consent missing but proof externally used. Critical incident; remove
  immediately; client notified.
- Redaction violated in a downstream draft. Trust Guardian halts.
- Consent revoked but proof still appears. Worker enforces immediate
  removal across all queues.
- Bilingual mismatch (Arabic and English say different things). Held.

## 11. Recovery path

- For unapproved use: immediate removal; ledger entry; client notified
  if applicable; root cause review.
- For consent miss: immediate removal; client outreach with apology.
- For redaction breach: immediate removal of the offending draft;
  incident opened.
- For revocation: removal across all queues within 1 working hour.
- For bilingual mismatch: copy aligned; reviewer rechecks.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Approval queue review |
| Weekly | New proof intake from delivery |
| Monthly | Library audit; freshness check |
| Quarterly | Consent re-confirmation (where appropriate) |

## 13. Saudi specifics

- Many Saudi customers prefer `sector_only` or `fully_anonymous`
  postures; the library treats these as first-class.
- Bilingual proof is the default for assets used in Saudi B2B.
- PDPL alignment is the floor; sector-specific data rules may add
  further constraints.
- Verbal consent is logged with a date and witness; written consent is
  preferred and is required for `named` use.

## 14. Non-negotiables

- No proof published without explicit approval.
- No "guaranteed" framing of proof.
- No use of revoked proof.
- No proof reveals other-customer data.
- A3 not used.

Proof is the strongest demand-creation asset in the system. The OS
treats it like the regulated asset it is.
