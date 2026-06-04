# Sector Classifier Prompt

Classify this company into the correct GCC sector for Dealix outreach.

## Company
Name: {{company_name}}
Description: {{description}}
Services: {{services_list}}
Country: {{country}}

## Available Sectors
- legal
- international_company
- facilities_management
- consulting
- real_estate
- healthcare_admin
- education_training
- contracting
- logistics
- b2b_services
- financial_services
- government_related

## Output
```json
{
  "sector": "legal",
  "sub_sector": "corporate_law",
  "confidence": 0.88,
  "reasoning": "Company provides corporate legal services..."
}
```

If confidence < 0.6, classify as b2b_services.
