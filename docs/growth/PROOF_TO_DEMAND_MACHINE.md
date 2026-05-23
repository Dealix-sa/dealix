# Proof-to-Demand Machine

> Turns delivered work into shareable proof artefacts and warm-list demand.

## 1. Purpose

Every delivered Sprint or Retainer should produce:

1. An **anonymised** proof artefact (case study, sample pack, sector report section).
2. A **warm-list update** — accounts in the same sector who should see the proof.
3. A **landing/proof-page update** — public proof surface refreshed.

## 2. Input

- Delivery outputs from Revenue Sprints and Retainers (in private ops).
- Customer-approved disclosure scope (what we can publish, anonymisation requirements).
- Sector + persona of the delivered account.

## 3. Output

- Anonymised proof markdown drafted in `docs/proof-packs/` (private mirror in ops).
- Warm-list candidates appended to `data/growth/warm_list.csv`.
- Updated landing proof page content draft.
- Content calendar entries that reference the proof.

## 4. Approval class

**A1** for proof publishing; **A2** if the customer logo or any identifying detail is included (requires customer + founder co-sign).

## 5. Owner

Distribution Operator + founder + customer-side approver.

## 6. Worker name

`proof_to_demand_worker`.

## 7. KPI

- Proof artefacts published per delivered Sprint: ≥ 0.5 (every other Sprint).
- Time from delivery to proof publication: median ≤ 21 days.
- Warm-list lift per published proof: ≥ 5 new candidate accounts.

## 8. Doctrine

- Anonymisation is the default. Customer logo only with explicit written approval.
- Every proof artefact carries: scope, period, metrics, methodology, what we will NOT claim.
- Every proof artefact is bilingual.

## 9. Failure modes

| Failure                                          | Recovery                                        |
|--------------------------------------------------|-------------------------------------------------|
| Proof references customer-identifying details    | Refuse; require customer co-sign                |
| Proof claims a result beyond the scope           | Verifier rejects; founder reviews               |
| Warm-list update collides with anti-ICP rules    | Refuse; document                                |
