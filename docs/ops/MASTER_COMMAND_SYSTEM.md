# Master Command System

## Purpose
Single index of every Make target Dealix exposes. If a target is not listed here, it is not part of the operating contract.

## Core sprint checks
- `make implementation-check` — runs the full pack verifier and the master verifiers.
- `make company-check` — runs company data architecture verifier + private data quality.
- `make security-check` — runs security/reliability/supply-chain + public safety + data boundary verifiers.

## Daily commands
- `make mission-control` — refresh `dealix-ops-private/founder/mission_control.md`.
- `make ceo-action-queue` — refresh `dealix-ops-private/founder/ceo_action_queue.md`.
- `make control-tower` — refresh `dealix-ops-private/founder/control_tower_brief.md`.

## Weekly commands
- `make ceo-weekly` — produce the weekly CEO loop output.
- `make weekly-close` — close the week, write metrics history.
- `make business-score` — refresh `business_audit/ceo_business_score.md`.
- `make assurance` — refresh `evidence/execution_assurance_report.md`.

## Revenue ops commands
- `make revenue-ops` — run the revenue ops chain (lead → cadence → proposal → payment).

## Delivery commands
- `make delivery` — initialize a new client folder from `clients/_template/`.

## Finance commands
- `make finance-full` — generate finance command report + pricing review.

## Trust commands
- `make trust-full` — generate trust review + AI risk register check.

## Content commands
- `make content` — scan claims + refresh content calendar status.

## Productization & people
- `make productization` — generate productization review.
- `make people` — generate people / delegation report.
- `make partners` — generate partner pipeline report.

## Bootstrap
- `make bootstrap-private` — create the `dealix-ops-private/` working tree skeleton (idempotent).

## Operating rule
Every Make target must:
1. Be deterministic when run twice in a row.
2. Print PASS or FAIL clearly.
3. Touch only its documented inputs and outputs.
4. Refuse to overwrite private artifacts without an explicit `--force` flag.
