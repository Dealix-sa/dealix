# Autonomy Policy

## Purpose
Limit how autonomously any Dealix system, agent, or script can act on the world.

## Owner
Sami / Trust owner.

## Review Cadence
Weekly.

## Principles
1. Autonomy is earned by passing evals, not assumed.
2. Every agent has a default action class (see APPROVAL_MATRIX.md).
3. Higher autonomy requires explicit registration and observable tracing.
4. Any agent must be able to stop, hand off, or refuse.

## Tiers
- **Tier 0 — Read only.** Cannot write external state.
- **Tier 1 — Drafts only.** Writes drafts to internal queues; no send.
- **Tier 2 — Send with approval.** Sends only after founder approves the specific draft.
- **Tier 3 — Send within policy.** Sends within a pre-approved policy window and template.
- **Tier 4 — Reserved.** Currently disabled. Requires explicit charter.

## Default Tier per Surface
| Surface | Default Tier |
|---------|--------------|
| Outbound DM/email | 1 |
| Proposal generation | 1 |
| Pipeline edits | 0 (read) for agents; 1 for humans through CLI |
| Public content publishing | 1 |
| Payments / charges | 1 (draft only) |
| Compliance claims | 1 (draft only) |

## Escalation
Any attempt to exceed a tier is logged and surfaced in `founder/decision_queue.md`.

## Linked Systems
- docs/trust/APPROVAL_MATRIX.md
- docs/trust/TRUST_CONTROL_SYSTEM.md

## Last Reviewed
2026-05-23
