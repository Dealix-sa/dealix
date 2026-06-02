# GTM Metrics — مقاييس السوق

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../market_os/MARKET_PRODUCTION_OS_AR.md)

> ما لا يُقاس لا يتحسّن. نقيس الإنتاج والجودة والإرسال والردود — ونفصل دائمًا التقدير عن المُتحقَّق.

---

## 1. مقاييس يومية

drafts generated · drafts quality-passed · drafts approved · emails sent · bounces · unsubscribes ·
replies · positive replies · meetings booked · proposals requested · job signals found · content posts drafted · partner prospects.

> ملاحظة حوكمة: "emails sent" مقيّد بسقف التدرّج، لا بعدد الـ drafts. الفجوة بين 250 draft و(0–250) send مقصودة.

---

## 2. مقاييس أسبوعية

best sector · best offer · best subject line · best CTA · worst bounce source · highest reply source ·
pipeline value (تقديري، مع وسم estimated) · lessons learned · next week experiments.

---

## 3. مصادر القياس

- الإنتاج/الجودة/الموافقة: `outreach_draft` + `approval_action`.
- الإرسال/الصحة: `email_account` + `sending_batch` + [DOMAIN_HEALTH_REVIEW](../../reports/outreach/DOMAIN_HEALTH_REVIEW.md).
- الردود: `reply`.
- الإشارات: `job_signal`.
- القيمة/الإثبات: `value_os` (estimated/observed/verified/client_confirmed) + `proof_os`.

لا نخترع أرقام CRM في الأتمتة؛ القيم الحقيقية تُستورد بموافقة (انظر سياسة KPI في AGENTS.md).

---

## 4. التقارير

[DAILY_GTM_REPORT](../../reports/gtm/DAILY_GTM_REPORT.md) · [WEEKLY_GTM_REVIEW](../../reports/gtm/WEEKLY_GTM_REVIEW.md).

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
