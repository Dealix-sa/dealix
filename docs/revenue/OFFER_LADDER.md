# سُلَّم العروض — Offer Ladder

> Five rungs. Prices. Scope. Deliverables. Qualifying criteria.

## Purpose
Make the offers explicit, ordered, and qualifying-gated. Buyers and the team see the same ladder.

## Owner
Founder/CEO.

## Inputs
- Revenue model (`REVENUE_MODEL.md`).
- Pipeline stages (`PIPELINE_STAGES.md`).
- Delivery playbook (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`).
- ICP definition (`docs/strategy/ICP_STRATEGY.md`).

## Outputs
- This file (canonical ladder).
- Proposal templates (`templates/PROPOSAL_*.md.j2`).

## Rules
1. Customers enter at the lowest applicable rung. The default entry is Signal Sample.
2. Higher rungs are sold only after qualifying criteria are met — no skipping.
3. Each rung has: price band, scope, exclusions, deliverables, payment terms, disclosure footer.
4. Customizations beyond ±15% scope require a new proposal, not a verbal add-on.
5. No rung guarantees revenue, conversion, or ROI. Outputs are operational, evidenced, and estimated.

## Metrics
- Distribution of revenue across rungs.
- Rung-to-rung upgrade rate.
- Average days from rung N to rung N+1.

## Cadence
Reviewed Quarterly.

## Evidence
This file, proposals issued, customer records.

## Verifier
`make offer-ladder-verify` — checks each rung has all required fields.

## Runtime Command
`make offer-ladder-refresh`

---

## Rung 1 — Signal Sample

| Field | Value |
|---|---|
| Price | SAR 15,000 – 25,000 |
| Duration | 5–10 working days |
| Scope | A focused diagnostic on one operational question (e.g., commercial pipeline leak, delivery throughput, one workflow audit) |
| Deliverable | A written sample report (10–20 pages) with: findings, recommended sprint shape, case-safe template |
| Exclusions | Implementation, tool deployment, training |
| Payment | 100% upfront |
| Disclosure | Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة |
| Qualifying | ICP-fit ≥ 5; DM identified; meeting completed |

## Rung 2 — Revenue Sprint

| Field | Value |
|---|---|
| Price | SAR 75,000 – 150,000 |
| Duration | 4–6 weeks |
| Scope | One operational problem solved with templated delivery; documentation handed over |
| Deliverable | Outcome (operational improvement) + transferrable playbook + case-safe artifact for Dealix evidence library |
| Exclusions | Ongoing operations (covered by Revenue Desk); custom software builds |
| Payment | 50% on signing, 50% on acceptance |
| Disclosure | Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة |
| Qualifying | Signal Sample completed OR equivalent diagnostic agreed; written scope confirmed |

## Rung 3 — Managed Pilot

| Field | Value |
|---|---|
| Price | SAR 100,000 – 200,000 |
| Duration | 6–8 weeks |
| Scope | Productized variant of a proven Revenue Sprint shape; faster delivery with standardized template |
| Deliverable | Same as Revenue Sprint but with pre-built artifacts and benchmark comparison from `docs/sector-reports/` |
| Exclusions | Same as Revenue Sprint |
| Payment | 50% on signing, 50% on acceptance |
| Disclosure | Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة |
| Qualifying | Customer in a sector where Managed Pilot is productized (≥ 5 prior successful Sprint runs) |

## Rung 4 — Revenue Desk (Retainer)

| Field | Value |
|---|---|
| Price | SAR 25,000 – 60,000 / month |
| Duration | 3-month minimum, then month-to-month |
| Scope | Ongoing operational discipline: monthly review, quarterly recalibration, on-call advisory |
| Deliverable | Monthly operating report (case-safe template); quarterly recalibration document |
| Exclusions | Build work (separate Sprint); cannot replace customer's operational team |
| Payment | Monthly in advance |
| Disclosure | Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة |
| Qualifying | Revenue Sprint completed with acceptance |

## Rung 5 — Dealix OS

| Field | Value |
|---|---|
| Price | SAR 100,000 / year + services (TBD) |
| Duration | Annual license |
| Scope | Productized template library + light services; per-customer instance of the operating system this repo describes |
| Deliverable | Access + onboarding sprint + quarterly update |
| Exclusions | Custom development; integration beyond agreed connectors |
| Payment | Annual in advance |
| Disclosure | Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة |
| Qualifying | Customer has run ≥ 1 Revenue Sprint successfully; product has reached 10 successful Sprint runs in the sector |

## Proposal language patterns to avoid
- "Guaranteed" → use "evidenced opportunity" or "estimated".
- "AI-powered" → use the concrete noun (e.g., "pipeline scoring", "anomaly detection").
- "Transform your business" → state the specific operational metric expected to move, labeled as estimated.

## Customization policy
- Up to ±15% scope adjustment without re-pricing.
- Beyond ±15%: new proposal.
- White-label, off-brand, or anonymity-only engagements: A2 Go/No-Go gate (because they prevent evidence creation).

## القواعد العربية
1. الدخول من الدرجة الأدنى المناسبة، الافتراضي عينة الإشارة.
2. لا قفز فوق درجة دون استيفاء معايير الترقية.
3. لا درجة تضمن إيرادًا أو تحويلًا. النواتج تشغيلية، مُدلَّلة، وتقديرية.

## Cross-links
- `REVENUE_MODEL.md`
- `PIPELINE_STAGES.md`
- `REVENUE_CONTROL_SYSTEM.md`
- `OFFER_EVOLUTION_SYSTEM.md`
- `docs/strategy/ICP_STRATEGY.md`
