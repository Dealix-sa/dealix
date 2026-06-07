# AI Agent Risk Register

| Risk | Impact | Control |
|---|---|---|
| Hallucinated prospect facts | فقدان ثقة | source_required + human review |
| Overpromising ROI | مخاطرة قانونية | compliance QA + forbidden claims list |
| Sending without approval | ضرر سمعة | no-send architecture |
| Sensitive data leakage | عالي | secret/public exposure checks |
| Bad CRM stage changes | pipeline غير دقيق | approval for stage changes |
| Workflow drift | مخرجات غير متسقة | prompt contracts + evals |
