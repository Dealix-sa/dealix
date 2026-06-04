# Sector Classifier Agent

## Role
Maps each company to the correct sector from sectors.yml and selects the appropriate primary offer and entry offer.

## Classification Signals
- Website services description
- Company name keywords
- LinkedIn industry tag
- sector_hint from raw lead

## Output
```json
{
  "sector": "legal",
  "sub_sector": "corporate_law",
  "primary_offer": "legal_knowledge_os",
  "entry_offer": "ai_workflow_audit",
  "confidence": 0.88
}
```

## Fallback
If sector confidence < 0.6 → classify as "b2b_services" and use "ai_workflow_audit" as entry.
