# Go / No-Go Master / قرار المضي من عدمه — الرئيسي

> **Purpose (EN):** The master decision gate for anything customer-facing.
>
> **الغرض (AR):** البوابة الرئيسية للقرار لأي شيء يواجه العميل.

_Layer: V9 — Strategic Moat & Enterprise Readiness OS_

## GO — Allowed / مسموح

- Enterprise readiness preparation and prepared answers (pending review).
- Demo pack generation from sandbox/sample data.
- Trust center content aligned to verifiable claims.
- Data room preparation with sourced evidence only.
- Procurement packet preparation.
- QMS readiness and checklists.
- Deployment static verification.
- Founder delegation planning.

## NO-GO — Forbidden / ممنوع

- External sending (email, WhatsApp, LinkedIn) by the system.
- Platform automation, scraping, or auto-submit.
- Fake certifications or fake traction.
- Unreviewed legal/security claims.
- Live paid-ads launch.
- Committing secrets or API keys.
- Destructive migrations or breaking main/server.

## Decision Rule / قاعدة القرار

- If any NO-GO item is touched, stop and escalate to the founder.
- If all GO conditions hold and verifiers PASS, proceed with founder approval.

```bash
python scripts/strategic_moat_verify.py && \
python scripts/enterprise_readiness_verify.py && \
python scripts/trust_center_verify.py && \
python scripts/demo_os_verify.py && \
python scripts/customer_lifecycle_verify.py && \
python scripts/agent_governance_verify.py && \
python scripts/cost_control_verify.py && \
python scripts/data_room_verify.py && \
python scripts/procurement_verify.py && \
python scripts/qms_verify.py && \
python scripts/docs_governance_verify.py && \
python scripts/deployment_static_verify.py
```

---

## Operating Boundaries / حدود التشغيل

**AI prepares; the founder approves and sends.** Founder approval remains required.
