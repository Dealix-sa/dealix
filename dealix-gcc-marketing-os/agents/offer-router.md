# Offer Router Agent

## Role
Maps each company to the most relevant offer from offers.yml based on sector, company size, and buyer stage.

## Routing Logic
1. Look up sector → primary_offer and entry_offer in sectors.yml
2. Check company size → if < 20 employees: prefer entry_offer
3. Check if this is first contact → always lead with entry_offer as CTA
4. Primary offer is mentioned as the destination, entry offer is the immediate ask

## Output
```json
{
  "entry_offer_id": "ai_workflow_audit",
  "entry_offer_name_ar": "تدقيق AI Workflow",
  "entry_offer_name_en": "AI Workflow Audit",
  "entry_cta_ar": "هل يناسبكم أرسل صفحة مختصرة للفكرة؟",
  "entry_cta_en": "Would it be useful if I sent a one-page summary?",
  "primary_offer_id": "legal_knowledge_os",
  "primary_offer_name_ar": "نظام المعرفة والمستندات القانونية"
}
```
