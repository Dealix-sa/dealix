# SaaS Candidate Rules — معايير ترشيح المنتج SaaS

## Purpose
Formal criteria for promoting an automated workflow into a SaaS candidate. Promotion does not mean SaaS will be built — it means the workflow has earned a candidate brief and a Build/Defer/Kill decision at the SaaS level.

## Owner
Founder. Decision quarterly, never ad-hoc.

## Inputs
- 10+ automated run logs from `docs/product/PRODUCTIZATION_ENGINE.md`.
- Margin proof from `docs/finance/`.
- Escalation log from delivery analyst.
- Client willingness-to-pay signals (written, paid renewals).
- Competitive scan (1-page summary, not a deck).

## Outputs
- SaaS candidate brief stored at `docs/product/candidates/SC-<id>.md`.
- Routed to `docs/product/BUILD_DEFER_KILL.md` at SaaS scope.

## Promotion Gates — All Must Pass
| Gate | Threshold | Evidence |
|---|---|---|
| Automated runs | ≥ 10 successful | Run logs |
| Margin | ≥ 60% gross per run | Finance pack |
| Escalations | ≤ 1 per 10 runs | Escalation log |
| Distinct clients | ≥ 5 | Signed SOWs |
| Renewal evidence | ≥ 2 paid renewals on the workflow | Contracts |
| Demand pull | ≥ 3 inbound requests citing the workflow | Email or signed inquiries |
| Founder time | < 4 hours per run | Time log |
| Compliance | PDPL + AI policy clean | `docs/14_trust_os/` |

## Rules
1. All eight gates must pass; no exceptions.
2. A candidate that fails one gate goes back to Automation stage for one more quarter, then re-tested.
3. SaaS marketing copy is forbidden until a Build decision is recorded.
4. No "SaaS-soon" narrative to investors before this gate.
5. Estimated TAM figures labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Candidate Brief Contents
- Workflow name + ID.
- Run statistics (10+ runs).
- Margin table.
- Client list (anonymized or with written consent).
- Competitive scan.
- Build scope estimate (T-shirt sizing).
- Kill criterion.
- Decision deadline (≤ 30 days).

## Metrics
- Candidates promoted per year (target: 1-2).
- Candidates killed at SaaS gate (target ≥ 30%).
- Build-decision time (median ≤ 30 days).
- Post-build adoption (90-day retention).

## Cadence
- Quarterly promotion review.
- 30-day Build/Defer/Kill window per candidate.

## Evidence
- `docs/product/candidates/SC-<id>.md`.
- Linked evidence under `evidence/productization/`.

## Verifier
Founder. Delivery analyst supplies counts.

## Runtime Command
`make saas-candidate-check ID=<workflow_id>` — verifies all eight gates, prints missing evidence, refuses promotion if any gate fails.

## Arabic Summary — ملخص عربي
ترقية مهمة آلية إلى مرشح SaaS تتطلب ثماني بوابات تجتاز كاملة. لا استثناءات. لا تسويق SaaS قبل قرار البناء. القيم التقديرية ليست مُتحقَّقة.
