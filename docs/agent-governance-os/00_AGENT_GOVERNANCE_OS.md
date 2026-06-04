# Agent Governance OS / نظام حوكمة الوكلاء

> **Purpose (EN):** Roles, boundaries, QA, cost control, and audit for AI agents.
>
> **الغرض (AR):** الأدوار والحدود وضمان الجودة وضبط التكلفة والتدقيق للوكلاء.

_Layer: V9 — Strategic Moat & Enterprise Readiness OS · Generated: 2026-06-04_

## Overview / نظرة عامة

- Every agent has a defined role and explicit boundaries.
- Agents prepare and recommend; they never act autonomously externally.
- Defined in config/agent_registry.json and config/agent_prompt_library.json.

---

## Operating Boundaries / حدود التشغيل

**AI prepares, analyzes, drafts, ranks, and recommends. The founder reviews,
approves, sends manually, sells, signs, and decides. The system never sends
externally.**

الذكاء الاصطناعي يجهّز ويحلّل ويصيغ ويرتّب ويوصي. المؤسس يراجع ويعتمد ويرسل يدويًا
ويبيع ويوقّع ويقرّر. النظام لا يرسل خارجيًا أبدًا.

Non-negotiables enforced across this OS:

- No secrets, API keys, SMTP, or credentials committed.
- No email / WhatsApp / LinkedIn outbound, no platform automation.
- No scraping, no auto-submit, no live paid-ads launch.
- No fake traction, no guaranteed ROI, no unverified claims or certifications.
- No external sending from GitHub Actions; verification is artifact-only.
- Founder approval remains required before anything leaves the building.
