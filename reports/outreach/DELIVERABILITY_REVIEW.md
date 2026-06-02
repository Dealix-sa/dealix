# Deliverability Review — مراجعة قابلية التسليم (قالب)

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../../docs/market_os/MARKET_PRODUCTION_OS_AR.md)

> قالب مراجعة يومية. القيم placeholder حتى ربط البيانات الفعلية (`data/`, مكبوتة في git).
> المرجع: [EMAIL_DELIVERABILITY_POLICY_AR](../../docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md).

**التاريخ:** YYYY-MM-DD

## بوابة ما قبل الإرسال (لكل حساب)

| account_id | SPF | DKIM | DMARC | tracking domain | unsubscribe | suppression | health |
|---|---|---|---|---|---|---|---|
| acct_example | ✓ | ✓ | ✓ | ✓ | ✓ | active | healthy |

## مؤشرات الصحة اليوم

| المؤشر | القيمة | العتبة | الحالة |
|---|---|---|---|
| bounce rate | 0.0% | < 3% | ok |
| spam complaint rate | 0.0% | < 0.1–0.3% | ok |
| unsubscribe rate | 0.0% | مُراقَب | ok |
| provider warnings | 0 | 0 | ok |
| positive reply rate | — | يتحسّن | — |

## قرارات اليوم

- المرحلة الحالية للتدرّج: Week 0 (0–20 send/day).
- أي حساب `paused`؟ لا.
- إجراءات تصحيحية: —

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
