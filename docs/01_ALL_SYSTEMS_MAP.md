# All Systems Map / خريطة كل الأنظمة

> **Purpose (EN):** A complete map of the repository's operating systems and where they live.
>
> **الغرض (AR):** خريطة كاملة لأنظمة تشغيل الريبو وأين تقع.

_Layer: V9 — Strategic Moat & Enterprise Readiness OS_

## V9 Systems / أنظمة V9

- `docs/strategic-moat-os/` — durable competitive advantage.
- `docs/enterprise-readiness-os/` — selling to large organizations.
- `docs/trust-center-os/` — public + internal trust posture.
- `docs/demo-os/` — safe, sandbox-only demos.
- `docs/customer-lifecycle-os/` — first touch to expansion.
- `docs/delegation-os/` — founder vs operator split.
- `docs/agent-governance-os/` — AI agent roles and boundaries.
- `docs/cost-control-os/` — model routing and token budgets.
- `docs/data-room-os/` — investor/enterprise/partner packets.
- `docs/procurement-os/` — vendor, PO, SOW, change requests.
- `docs/qms-os/` — quality management system.
- `docs/docs-governance-os/` — documentation governance.
- `docs/deployment-verification-os/` — static deploy verification.

## Configs / الإعدادات

- `config/demo_scenarios.json`
- `config/customer_lifecycle_stages.json`
- `config/agent_registry.json`
- `config/agent_prompt_library.json`
- `config/model_routing_policy.json`
- `config/token_budgets.json`
- `config/qms_checklists.json`

## Verification / التحقق

- All V9 verifiers live in `scripts/*_verify.py` and write JSON to `outputs/v9_verification/`.
- The aggregate report is `outputs/v9_verification/V9_MASTER_VERIFICATION.md`.

## Prior Layers / الطبقات السابقة

- V1–V8 systems remain under their existing `docs/` folders and modules.
- V9 layers on top without breaking prior systems.

---

## Operating Boundaries / حدود التشغيل

**AI prepares; the founder approves and sends.** No external sending, no
automation, no scraping, no unverified claims. Founder approval remains required.
