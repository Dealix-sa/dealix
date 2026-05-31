# Offer Router Prompt

Select the best Dealix offer for this company based on sector, size, and buyer stage.

## Company
Sector: {{sector}}
Size estimate: {{size}}
Country: {{country}}
First contact: true

## Available Entry Offers
- ai_workflow_audit (499 SAR / 7 days) — always the safest first step

## Available Primary Offers
See offers.yml

## Rules
- First contact always leads with entry offer as the CTA
- Primary offer mentioned as the destination/context, not the immediate ask
- For companies < 20 people → entry offer only
- For sensitive sectors → entry offer only in first message

## Output
```json
{
  "entry_offer_id": "ai_workflow_audit",
  "entry_offer_cta_ar": "هل يناسبكم أرسل صفحة مختصرة للفكرة؟",
  "entry_offer_cta_en": "Would it be useful if I sent a one-page summary?",
  "primary_offer_id": "legal_knowledge_os",
  "rationale": "Law firm with 10+ partners — document intelligence is primary value prop"
}
```
