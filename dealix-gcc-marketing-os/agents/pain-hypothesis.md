# Pain Hypothesis Agent

## Role
Selects the single most compelling pain angle for each company + sector combination, based on A/B testing config from persuasion.yml.

## Logic
1. Load sector's pain list from sectors.yml
2. Load A/B angles from persuasion.yml ab_testing_angles
3. Check learning_log.jsonl for which angle performs best for this sector/country/language
4. If no learning data → use angle_a (default first angle)
5. For Tier A companies → use deeper research to find visible pain on website

## Output per draft type
```json
{
  "angle_id": "document_retrieval",
  "pain_statement_ar": "كمية المستندات وصعوبة الوصول إليها بسرعة",
  "pain_statement_en": "difficulty retrieving specific contracts and matter context quickly",
  "draft_version": "A",
  "learning_applied": false
}
```
