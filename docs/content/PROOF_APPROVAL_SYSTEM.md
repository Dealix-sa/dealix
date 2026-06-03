# Proof Approval System

## Purpose
Decide whether and how to reuse a client outcome as proof in marketing.

## Inputs
- Source: `clients/<slug>/proof_approval.md`.
- Client written approval (email is acceptable).
- Trust workflow approval in `trust/claim_review_log.csv`.

## Proof levels
| Level | What can be shown |
|---|---|
| Opinion | Founder's view; no client attribution |
| Method | Generic methodology; no client-specific numbers |
| Anonymized case | Sector + role + outcome; no name |
| Named case | Client name with explicit written approval |

## Required artifact set per named case
- Client's written approval (email screenshot or signed).
- Trust workflow approval row.
- Case study draft following `docs/content/CASE_STUDY_SYSTEM.md`.

## Promotion rules
- An anonymized case can be published with client verbal approval.
- A named case requires written approval.
- Any number quoted in a case must be cited and verifiable from `unit_economics.csv` or the delivery report.

## Decay
- After 24 months, proof needs a refresh approval from the client.

## Anti-overclaim
- No "we generated X SAR for client Y" unless we can show the math.
- No "Y trusts us with their data" unless Y has confirmed this language.
