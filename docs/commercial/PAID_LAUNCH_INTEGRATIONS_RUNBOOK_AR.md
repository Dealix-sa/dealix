# تشغيل تكاملات الإطلاق المدفوع

**متى:** بعد أول `payment_received` + `proof_pack_delivered` حقيقيين.

```bash
python scripts/verify_paid_launch_readiness.py
python scripts/railway_launch_env_check.py
```

## Moyasar

- `MOYASAR_SECRET_KEY`, `MOYASAR_WEBHOOK_SECRET`
- Webhook: `https://api.dealix.me/api/v1/webhooks/moyasar`

## HubSpot · Calendly · PostHog · Gmail

راجع [PAID_LAUNCH_TRACKER_AR.md](PAID_LAUNCH_TRACKER_AR.md) و [LAUNCH_GATES.md](../LAUNCH_GATES.md).

**قاعدة:** لا إرسال بارد أو LinkedIn آلي.
