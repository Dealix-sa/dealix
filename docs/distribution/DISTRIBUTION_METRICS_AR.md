# Dealix Distribution Metrics — لوحة مؤشرات القمع

`dealix/distribution/metrics.py` · CLI: `scripts/distribution_metrics.py` ·
Make: `make distribution-metrics`

> تجميع خالص فوق السجلات — لا اتصالات خارجية، ولا حقول تواصل (PII) في المخرجات
> (أسماء شركات + أعداد فقط).

## KPIs
```
pending_drafts · approved_drafts · due_followups · proposal_drafts
proof_packs · payment_handoffs · upcoming_renewals · won_deals · lost_deals
```

## القمع (funnel)
```
drafts → approved → proposals → accepted → payments → paid
```
مع نسب التحويل:
- `draft_approval_rate_pct`
- `proposal_accept_rate_pct`
- `payment_close_rate_pct`

## تفصيلات
- `by_status` لكل نوع سجل.
- `sector_performance` و`channel_performance` (من المسودات).
- `win_loss` (من محرك التعلّم).

## المخرجات
- طباعة + `reports/distribution/DISTRIBUTION_METRICS.md`.
- المراجعة الأسبوعية: `make distribution-weekly` →
  `reports/distribution/WEEKLY_DISTRIBUTION_REVIEW.md` (تتضمن قرارات المؤسس).

## التحقق
```python
from dealix.distribution.metrics import compute_metrics
compute_metrics()["funnel"]
```
