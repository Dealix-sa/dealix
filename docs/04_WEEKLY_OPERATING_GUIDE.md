# Weekly Operating Guide / دليل التشغيل الأسبوعي

> **Purpose (EN):** The weekly cadence that keeps the company healthy.
>
> **الغرض (AR):** الإيقاع الأسبوعي الذي يحافظ على صحة الشركة.

_Layer: V9 — Strategic Moat & Enterprise Readiness OS_

## Weekly Review / المراجعة الأسبوعية

- Customer health review across all accounts (`docs/customer-lifecycle-os/05_CUSTOMER_HEALTH_REVIEW.md`).
- Delegation review of delegated work quality (`docs/delegation-os/06_WEEKLY_DELEGATION_REVIEW.md`).
- Cost review of model usage assumptions (`docs/cost-control-os/04_COST_ALERTS_MANUAL_PROCESS.md`).
- QMS continuous-improvement review (`docs/qms-os/07_CONTINUOUS_IMPROVEMENT.md`).

## Weekly Verification / التحقق الأسبوعي

```bash
python scripts/strategic_moat_verify.py
python scripts/enterprise_readiness_verify.py
python scripts/qms_verify.py
python scripts/docs_governance_verify.py
python scripts/deployment_static_verify.py
```

## Weekly Outputs / المخرجات الأسبوعية

- Updated pipeline and forecast.
- One captured moat asset minimum.
- Risk and blocker list for founder decision.

---

## Operating Boundaries / حدود التشغيل

**AI prepares; the founder approves and sends.** Founder approval remains required.
