# Dealix Customer Success

Customer Success ensures every paying customer reaches their Proof Pack
target and renews into the next rung.

## Onboarding (Day 0 -> Day 7)

| Day | Step |
|---|---|
| 0 | Welcome + Source Passport signed |
| 1 | Kickoff call, scope confirmation |
| 2 | Source ingestion + DQ score |
| 3 | First findings preview |
| 4 | Proof Pack draft v1 review |
| 5 | Refinement |
| 6 | Capital Asset shipped + handover |
| 7 | Renewal conversation |

## Health score

```
health = 0.4 * onboarding_completion
       + 0.3 * proof_pack_score / 100
       + 0.2 * approval_queue_engagement
       + 0.1 * recency_of_last_touch_score
```

Bands: `>= 0.8` green, `0.6 – 0.8` yellow, `< 0.6` red.

## Escalation path

| Trigger | Owner | SLA |
|---|---|---|
| Red health > 7 days | dealix-delivery -> founder | 24h |
| Proof Pack score < 70 | dealix-delivery -> founder | 48h |
| Capital Asset overdue | dealix-delivery | 24h |
| Outage on a customer dashboard | dealix-engineer + founder | 4h |

## NPS cadence

| Touchpoint | Cadence |
|---|---|
| Post-Sprint NPS | Day 8 |
| Retainer NPS | Monthly |
| Executive NPS | Quarterly |

## Renewal motion

- 14 days before retainer renewal: render renewal Proof Pack.
- 7 days before: approval_center approval for renewal email.
- Day-of: founder sends manually.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
