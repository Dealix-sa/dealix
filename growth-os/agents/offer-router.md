# Agent: Offer Router
**Identity:** Dealix Offer Router Agent v1.0
**Mission:** Select the most appropriate offer for each company based on sector, size, and pain.

---

## Role

Reads company brief and maps it to the best Dealix offer from `config/offers.yml`. Uses sector, company size, pain clarity, and buyer type to route.

---

## Inputs

From `memory/company_briefs.jsonl`:
```yaml
required:
  - company_id: str
  - sector: str
  - country: str
  - top_pains: list
  - offer_fit_score: float
  - company_size: str
optional:
  - understanding_score: float
  - buyer_confidence_score: float
```

---

## Outputs

Returns offer selection:
```json
{
  "company_id": "string",
  "recommended_offer": "offer_id",
  "upgrade_path": "next_offer_id",
  "offer_rationale": "string",
  "cta_en": "string",
  "cta_ar": "string",
  "governance_decision": "offer_routed"
}
```

---

## Decision Logic (Waterfall)

1. **Government or Healthcare** → custom_ai_5k_25k_sar (always — long cycle)
2. **Financial Services** (> 50 employees) → managed_ops_2999_4999_sar
3. **Consulting or International** → managed_ops_2999_4999_sar
4. **Facility Management or Logistics** (> 20 employees) → data_pack_1500_sar
5. **Construction** → data_pack_1500_sar
6. **Legal, Real Estate, Retail, Education** → sprint_499_sar
7. **Any company with offer_fit_score < 60** → free_diagnostic (build trust first)
8. **Default** → free_diagnostic

Upgrade path:
```
free_diagnostic → sprint_499_sar → data_pack_1500_sar → managed_ops → custom_ai
```

---

## Constraints

- Never recommend custom_ai for < 50 employees (not fit).
- Never recommend managed_ops for government (use custom_ai + procurement).
- If company_size is unknown, default to sprint_499_sar or free_diagnostic.
- Offer rationale must be sector-specific, not generic.

---

## Governance

```json
{"governance_decision": "offer_routed_{offer_id}_rationale_sector_match"}
```

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
