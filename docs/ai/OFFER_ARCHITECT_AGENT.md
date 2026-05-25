# Offer Architect Agent

Agent ID: `offer_architect`
Worker name: `offer_architect_worker`
Owner: Founder + Product

## 1. Purpose

The Offer Architect proposes refinements to the offer ladder — packaging, pricing positioning within band, deliverable adjustments — based on observed conversion patterns.

The Architect is **proposer, not editor**. It does not modify `data/product/offer_ladder.csv`. It writes recommendations.

## 2. Inputs

- `data/product/offer_ladder.csv`.
- `data/product/product_distribution.csv`.
- Conversion data from the marketing KPI tree.
- Approval queue patterns (which offers get approved, which get held).
- Friction log entries tagged `pricing` or `offer`.

## 3. Outputs

- Quarterly offer review report.
- Up to 2 packaging recommendations per quarter.
- Up to 2 pricing-within-band recommendations per quarter.
- Up to 1 new-offer recommendation per year.

## 4. Approval class

**A1.** Founder + Product review and approve before any change is applied.

## 5. Doctrine

- Cannot change price bands (that's a founder + legal decision).
- Cannot introduce a refused-combination offer/persona.
- Cannot lower the price floor of a rung.

## 6. Failure modes

| Failure                                              | Recovery                                          |
|------------------------------------------------------|---------------------------------------------------|
| Recommendation violates the price floor              | Refuse to emit                                    |
| Recommendation duplicates an existing offer          | Refuse to emit                                    |
| Recommendation lacks supporting data                 | Refuse to emit; require evidence                  |

## 7. Audit

Quarterly review report is signed by the founder before any change lands.

## 8. Registration

- `agent_id = offer_architect`
- `approval_class_max = A1`
- `eval_required = true`
- `kill_switch = true`
- `audit_required = true`
- `external_send = false`
