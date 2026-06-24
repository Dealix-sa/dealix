# Buyer Mapper Prompt

Identify the best outreach target for this company.

## Company
Name: {{company_name}}
Sector: {{sector}}
Size: {{size}}
Team page info: {{team_page_summary}}
Default buyer titles for sector: {{sector_buyer_titles}}

## Rules
- Use team page info if available
- Fall back to first title in sector_buyer_titles
- If buyer name not public → use title + company context only (no personal email guessing)
- Flag personal emails as high_risk

## Output
```json
{
  "buyer_title": "Managing Partner",
  "buyer_name": "Ahmad Al-Rashidi",
  "email": "info@firm.com",
  "email_type": "role_based",
  "risk_level": "medium",
  "persona_id": "managing_partner_legal_ar"
}
```
