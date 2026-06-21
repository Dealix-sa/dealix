# Agent Governance v3 / حوكمة الوكلاء v3

## Purpose / الغرض

Govern all Dealix agents by risk, approval, evidence, and reversibility.

حوكمة جميع وكلاء Dealix حسب المخاطر والموافقة والدليل وقابلية العكس.

## Agent Classes / فئات الوكلاء

- **L0** Prompt Assistant / مساعد موجِّه
- **L1** Draft Assistant / مساعد مسودات
- **L2** Internal Analyst / محلل داخلي
- **L3** Workflow Router / موجه سير عمل
- **L4** Controlled Tool User / مستخدم أدوات مُحكَم
- **L5** Governed Automation / أتمتة محكومة

## Risk Dimensions / أبعاد المخاطر

- approval class A0–A3 / فئة الموافقة A0–A3
- reversibility R0–R3 / قابلية العكس R0–R3
- sensitivity S0–S3 / الحساسية S0–S3
- external impact / تأثير خارجي
- financial impact / تأثير مالي
- trust impact / تأثير ثقة

## Required For Every Agent / مطلوب لكل وكيل

- purpose / الغرض
- owner / المسؤول
- inputs / المدخلات
- outputs / المخرجات
- tools / الأدوات
- approval class / فئة الموافقة
- eval suite / حزمة التقييم
- logs / السجلات
- disable path / مسار التعطيل
- incident path / مسار الحوادث

## Rule / القاعدة

No L4/L5 agent without eval, logs, and approval gates.

لا وكيل L4/L5 بدون تقييم وسجلات وبوابات موافقة.

## Supersedes / يحل محل

- [`../agentic_operations/AGENT_GOVERNANCE_RUNTIME.md`](../agentic_operations/AGENT_GOVERNANCE_RUNTIME.md) — يستبدل وثيقة الـ runtime ويضع فئات الوكلاء L0–L5 وأبعاد المخاطر A/R/S كتصنيف موحد. Replaces the runtime doc with unified L0–L5 agent classes and A/R/S risk dimensions.
- [`../enterprise/AI_AGENT_GOVERNANCE_COUNCIL.md`](../enterprise/AI_AGENT_GOVERNANCE_COUNCIL.md) — يستبدل وثيقة مجلس الحوكمة ويوحدها مع مصفوفة المخاطر التشغيلية. Replaces the governance council doc and unifies it with the operational risk matrix.

## See Also / مراجع

- [`../evals/EVAL_CI_GATE.md`](../evals/EVAL_CI_GATE.md)
- [`../runtime/WORKER_MESH_OS.md`](../runtime/WORKER_MESH_OS.md)
- [`../../dealix/contracts/schemas/decision_output.schema.json`](../../dealix/contracts/schemas/decision_output.schema.json)

## Owner / المسؤول

Sami / سامي (CEO)

## Version / الإصدار

v3.0 — 2026-05-23
