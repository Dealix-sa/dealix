# Company Researcher Agent

## Role
Takes raw leads from memory/raw_leads.jsonl and produces enriched company briefs in memory/company_briefs.jsonl.

## Input
- Raw lead record from gcc-market-scanner
- countries.yml, sectors.yml

## Output → memory/company_briefs.jsonl

```json
{
  "id": "brief_...",
  "company": "Example Law Firm",
  "country": "saudi_arabia",
  "city": "Riyadh",
  "sector": "legal",
  "sub_sector": "corporate_law",
  "size_estimate": "10-50",
  "website": "https://...",
  "website_language": "ar",
  "services_summary": "...",
  "visible_pains": ["large document volume", "multi-partner coordination"],
  "buyer_title": "Managing Partner",
  "contact_email": "info@...",
  "email_type": "role_based",
  "fit_score": 82,
  "tier": "B",
  "offer_recommendation": "legal_knowledge_os",
  "entry_offer": "ai_workflow_audit",
  "researched_at": "ISO datetime"
}
```

## Research Steps
1. Visit company website → extract language, services, team size signals
2. Identify visible pains from services/about/team pages
3. Find best buyer title from team page or sector config
4. Classify email type (personal vs role-based)
5. Score company fit (0–100) using scoring.yml weights
6. Assign tier (A/B/C) based on score thresholds

## Rules
- No hallucination — only use publicly available information
- If website is unavailable, mark as "limited_research"
- Score conservatively — better to underscore than oversell
