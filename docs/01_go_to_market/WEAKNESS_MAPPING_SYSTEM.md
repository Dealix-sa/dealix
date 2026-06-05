# Weakness Mapping System

> النظام لا يقول فقط "هذه شركة جيدة" — بل يقول: ما نقطة الضعف التي يحلها Dealix؟

This is the most important judgment in the pipeline. Scoring says *pursue*;
weakness mapping says *why* and *with which OS*. Engine:
`scripts/targeting_weakness_mapper.py`. Signals: `data/targeting/signals.yml`.

---

## Weakness → indicators → Dealix OS angle

| Weakness | Indicators (signals) | OS angle | AR |
|----------|----------------------|----------|----|
| Revenue Leakage | weak CTA, unclear follow-up | `revenue_os` | تسرّب إيراد |
| Proof Gap | no case studies / results | `proof_os` | فجوة إثبات |
| Command Fog | many services, scattered decisions | `command_os` | ضبابية قيادة |
| Delivery Blindness | projects with no visibility | `delivery_os` | عمى تسليم |
| Client Memory Gap | many clients & promises | `client_os` | فجوة ذاكرة عميل |
| Support Recurrence | repeated support issues | `support_os` | تكرار دعم |
| Data Fragmentation | Excel / Forms / WhatsApp scattered | `data_os` | تشظّي بيانات |
| Governance Risk | AI / data claims, no governance | `governance_os` | مخاطرة حوكمة |
| Partner Potential | agency/consultancy serving many SMEs | `partner_os` | إمكانية شراكة |

---

## How it works

1. Read each pain/partner signal present on the profile.
2. Accumulate its points onto the mapped weakness.
3. Rank weaknesses by accumulated weight.
4. `primary_weakness` + `primary_os_angle` = the top one.

**Fallback:** if no observable weakness fires, the mapper falls back to the
sector's `default_angle` from `sectors.yml` and marks it `hypothesis: true` so the
draft stays honest (low confidence, no fabricated pain).

---

## Output

```python
{
  "company_name": "...",
  "primary_weakness": "proof_gap",
  "primary_os_angle": "proof_os",
  "weaknesses": [ {type, os_angle, weight, evidence, label_ar}, ... ]
}
```

`evidence` lists the exact signal fields that fired — so the claim "this company
has a proof gap" is always traceable to observed data.
