# CRM Research Agent Prompt Contract

## Input
- company_name
- vertical
- known_pain
- source
- optional_notes

## Output JSON
```json
{
  "company": "",
  "vertical": "",
  "likely_pains": [],
  "fit_summary": "",
  "missing_information": [],
  "recommended_next_action": "",
  "risk_level": "low|medium|high",
  "needs_human_review": true
}
```

## Forbidden
- لا تخترع أرقام أو أسماء أشخاص.
- لا تستخدم معلومات غير مذكورة كحقيقة مؤكدة.
