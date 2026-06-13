# Agent Security Playbook

## Controls
- Least privilege workflows.
- No secrets in prompts or outputs.
- Output logging without sensitive data.
- Human approval gates.
- Prompt contracts.
- Evaluation before production use.

## Emergency stop
إذا أنتج agent مخرجات خطرة:
1. أوقفه من registry.
2. سجل incident.
3. راجع آخر 20 run.
4. أصلح prompt contract.
5. أعد التقييم قبل التشغيل.
