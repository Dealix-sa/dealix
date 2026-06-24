# Pain Hypothesis Prompt

Select the single best pain angle for this company's outreach draft.

## Company
Sector: {{sector}}
Country: {{country}}
Language: {{language}}
Draft type: {{draft_type}} (cold_email / followup_1 / followup_2)
Visible pain from research: {{visible_pain}}
Available angles: {{angles_list}}

## Rules
- ONE angle only per draft
- For cold email → use angle_a (primary angle)
- For followup_1 → use angle_b (secondary angle, different from A)
- For followup_2 → use angle_c (tertiary, most specific)
- If learning data exists → use highest-performing angle for this sector/country/language

## Output
```json
{
  "selected_angle": "document_retrieval",
  "pain_ar": "صعوبة البحث السريع في المستندات والعقود السابقة",
  "pain_en": "difficulty retrieving specific contracts and matter context quickly",
  "draft_version": "A",
  "learning_applied": false
}
```
