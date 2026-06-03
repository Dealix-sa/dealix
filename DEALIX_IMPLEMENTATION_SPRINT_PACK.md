# Dealix Implementation Sprint Pack

## Purpose
Convert the Dealix Master Operating Blueprint into practical implementation sprints. This pack is the bridge between the broad operating system documents and real, measurable market execution.

## Owner
Sami / Founder CEO.

## Principle
Build the minimum complete operating company system, then move it into market execution. Do not chase perfection: chase enough structure to support paying customers.

## Sprint Order
| Sprint | Name | Goal |
|---:|---|---|
| 0 | Repo Safety | protect repo, secrets, branch, public/private boundary |
| 1 | Master Blueprint | integrate all operating systems |
| 2 | Data + Private Ops | create source of truth and private data contracts |
| 3 | CEO Control | mission control, score, assurance, stage |
| 4 | Revenue Ops | leads, DMs, samples, proposals, payment path |
| 5 | Delivery + Client Success | intake, QA, handoff, feedback, retainer |
| 6 | Finance + Trust | pricing, cash, approvals, AI risk |
| 7 | Content + Proof | proof library, content system, safe claims |
| 8 | Productization + People | automation candidates, delegation, partners |
| 9 | Market Execution | 25 leads, 25 DMs, 3 samples, 1 proposal |
| 10 | First Delivery | paid/approved sprint delivery and feedback |

## Rule
Do not start Sprint 9 until Sprints 0–8 have enough structure to support execution.
Do not start SaaS until Sprint 10 produces repeated evidence.

## How to use this pack
1. Open `DEALIX_IMPLEMENTATION_MASTER_CHECKLIST.md` and treat it as the authoritative todo list.
2. For each sprint, complete the files listed in that sprint's section of this document.
3. Run the sprint verifier (`python scripts/verify_<sprint>.py`) before moving on.
4. Run `python scripts/verify_implementation_sprint_pack.py` to verify the whole pack.
5. Run `make implementation-check` to run the integrated check pipeline.

## Daily cadence guidance
- Day 1: Sprint 0 + Sprint 1
- Day 2: Sprint 2 + Sprint 3
- Day 3: Sprint 4 + Sprint 5
- Day 4: Sprint 6 + Sprint 7
- Day 5: Sprint 8
- Day 6–7: Sprint 9 market execution

## Definition of "Done" for the pack
- All sprint verifier scripts exit 0.
- The implementation sprint pack verifier exits 0.
- `make implementation-check` passes locally and in CI.
- Sprint 9 has produced at least one paying or written-approved deliverable.

## Non-negotiables (carried over from operating doctrine)
- Public/private boundary respected.
- No PII or proprietary client data committed to the public repo.
- Founder-led sales motion; no automated cold outreach.
- No overclaim in content or proposals.
- All revenue evidence is dual-logged: action log + capital asset register.
- Trust workflow approvals required for any external-facing claim.
