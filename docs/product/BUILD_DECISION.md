# Build Decision (Product)

**Golden rule:** do not build because it is “cool.” Build because it **repeated**, **paid**, or **reduced risk/time** at scale.

## Gate: 3 of 5

Build is justified only if **at least three** are true:

1. Repeated in **3+** projects (or same pattern 3+ times in ops)
2. A **customer paid** for the workflow / outcome it supports
3. **Reduces delivery time** materially
4. **Reduces governance** or quality risk
5. **Improves output quality** measurably

## Score (for prioritization among candidates)

| معيار | Weight |
|--------|--------|
| Repetition | 25 |
| Revenue impact | 20 |
| Time saved | 20 |
| Risk reduction | 15 |
| Quality improvement | 15 |
| Build simplicity | 5 |

| Band | Action |
|------|--------|
| **80+** | Build now |
| **60–79** | Backlog |
| **Below 60** | Do not build |

Log candidates in [`../company/FEATURE_CANDIDATE_LOG.md`](../company/FEATURE_CANDIDATE_LOG.md). Full rubric also in [`FEATURE_PRIORITIZATION.md`](FEATURE_PRIORITIZATION.md).

## Examples

| Idea | Verdict |
|------|---------|
| **Import preview** (Lead Intelligence) | Repeats, saves time, reduces errors, cross-service → **Build now** |
| **Full WhatsApp API** sending | High compliance / spam risk, approval-heavy, not MVP-critical → **Do not build now** |

## Decision record

- Feature name:
- 3-of-5 check: (which three)
- Score:
- Owner:
- Risk:
- Next action:

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
