# AI Agent Risk Model — Dealix

## الدور — Role

مخاطر متعلقة بتشغيل الـ agents/automations. مبني على NIST AI RMF: Govern → Map → Measure → Manage.

## فهرس المخاطر — Indexed risks

| ID | Description | Severity | Likelihood | Mitigation |
| --- | --- | --- | --- | --- |
| AIR-001 | Hallucination في proposal/Diagnostic | critical | medium | Eval gate قبل التسليم + founder approval |
| AIR-002 | إرسال آلي لرسالة غير معتمدة | critical | low | distribution = drafts فقط، no auto-send |
| AIR-003 | تسريب بيانات عميل في prompts | high | medium | redact + PII scanner + audit_log |
| AIR-004 | Prompt injection من إيميل وارد | high | medium | reply_router مع content sanitization + trust class |
| AIR-005 | Agent يتجاوز scope (مثال: ينشر proof دون إذن) | critical | low | policy_as_code + trust_gate=hard_block |
| AIR-006 | Drift في جودة output | medium | high | scheduled eval + weekly review |
| AIR-007 | Bias في scoring الحسابات | medium | medium | audit_log + human review قبل قرارات paid |
| AIR-008 | تكلفة LLM غير مراقبة | medium | high | cost_tracking + budget caps في finance_os |
| AIR-009 | Worker يفشل بصمت | high | medium | machine_health.csv + alerts |
| AIR-010 | تعارض قرارات بين agents | medium | low | command_bus + single source of truth |

## ضوابط — Controls

- **Govern**: `docs/00_constitution/NON_NEGOTIABLES.md` + Trust gate.
- **Map**: `registries/machine_registry.yaml`.
- **Measure**: `scripts/verify_prompt_output_quality.py` + Eval gate.
- **Manage**: `MACHINE_FAILURE_PLAYBOOK.md` + disable_switch.

## الملكية — Ownership

- Owner: Founder.
- Auditor: Trust gate.
