# Dealix — Launch Control Tower

> Daily go/no-go cockpit. Open this first every morning. Keep it honest.
> Pair with `docs/05_founder/DEALIX_EXECUTION_BOARD.md` and `reports/launch/launch_blockers.md`.

## Today's launch state

| Field | Value |
|---|---|
| Launch status | _Internal Ready / Private Launch Ready / Public Limited Ready / No-Go_ |
| Current ICP | Saudi SMEs & mid-market with existing opportunities, unclear follow-up/proof |
| Current offer | Dealix Command Sprint (7-day, fixed scope) |
| Current price | _set in `sales/COMMAND_SPRINT_ONE_PAGER.md`_ |
| Pages ready | see CTA map / `verify_dealix_cta_map.py` |
| Growth assets ready | see `verify_dealix_growth_assets.py` |
| Sales kit ready | see `sales/` |
| Delivery readiness | see `customers/_template/` |
| Proof readiness | see `customers/_template/10_proof_pack.md` |
| Governance readiness | see `docs/governance/CLAIMS_REGISTER.md` |
| Verification status | see `reports/launch/launch_blockers.md` |

## Go / No-Go verdict

| Verdict | Meaning | Action |
|---|---|---|
| **No-Go** | Blockers open | Do not sell. Close blockers first. |
| **Internal Ready** | Internals consistent, no customer-facing proof | Prepare internally only. |
| **Private Launch Ready** | Sprint page, start page, sales kit, customer template, proof pack template, claims register, approval policy all exist; no unsafe claims; founder can deliver first 3 sprints manually | Start first 3 Command Sprints. |
| **Public Limited Ready** | ≥1 paid sprint + ≥1 proof pack delivered; claims clean | Limited public launch after proof. |

## Private Launch readiness checklist (gate to start selling)

- [ ] `/command-sprint` page exists with one CTA
- [ ] `/start` page exists with one CTA
- [ ] Sales kit exists (`sales/` six files)
- [ ] `customers/_template/` exists (12 files)
- [ ] Proof Pack template exists (`customers/_template/10_proof_pack.md`)
- [ ] Claims Register exists (`docs/governance/CLAIMS_REGISTER.md`)
- [ ] Human Approval policy exists (`docs/governance/APPROVAL_MATRIX.md`, `HUMAN_IN_THE_LOOP_MATRIX.md`)
- [ ] No guaranteed-revenue claims (`verify_dealix_positioning.py` green)
- [ ] No auto-send language anywhere
- [ ] Founder can manually deliver the first 3 sprints

## Public Launch is FORBIDDEN if any are true

- 0 paid sprints · 0 proof packs
- a future module is shown as live
- claims are unsafe
- build is broken without a logged blocker note
- privacy/security incomplete
- no delivery path · no proof path

## Top blockers
_(maintained in `reports/launch/launch_blockers.md`)_

## Next founder actions
_(maintained in `docs/05_founder/DEALIX_EXECUTION_BOARD.md`)_
