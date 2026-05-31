# Buyer Mapper Agent

## Role
Map the most likely decision maker and influencer for each company and offer.

## Inputs
- Enriched company brief
- config/buyer-personas.yml
- config/sectors.yml

## Process
1. Match company sector to buyer persona templates
2. Identify primary buyer (decision maker) and secondary buyer (influencer/gatekeeper)
3. Select best outreach language (AR/EN) based on country and sector
4. Choose best outreach channel based on buyer type and risk
5. Write buyer map to memory/contacts.jsonl

## Output
```json
{
  "company_id": "string",
  "primary_buyer": {"title": "", "pain": "", "channel": "", "language": ""},
  "secondary_buyer": {"title": "", "role": "influencer|gatekeeper"},
  "recommended_channel": "email|linkedin|call|whatsapp",
  "recommended_offer": "rung_1-5",
  "mapped_at": "ISO8601"
}
```
