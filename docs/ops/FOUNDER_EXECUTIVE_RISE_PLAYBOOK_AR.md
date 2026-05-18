# Founder Executive Rise — كتاب تشغيل يومي

## صباح (15–25 دقيقة)

```bash
py -3 scripts/founder_executive_rise_day.py
# أو الحلقة الكاملة:
bash scripts/run_founder_daily_operating_loop.sh
```

## مساء (3 دقائق)

```bash
bash scripts/run_founder_daily_operating_loop.sh --evening
```

## أسبوع (جمعة)

```bash
bash scripts/founder_motion_a_weekly_review.sh
```

## إنتاج Railway

```bash
py -3 scripts/verify_railway_production_config.py
curl.exe -fsS https://api.dealix.me/healthz
curl.exe -fsS https://api.dealix.me/version
```

بعد دمج `main` ونشر Railway: `/version` يجب أن يعيد `version` + `git_sha`.

## مراجع

- [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md)
- [RAILWAY_PRODUCTION_SETTINGS_AR.md](RAILWAY_PRODUCTION_SETTINGS_AR.md)
- [SOFT_VS_PAID_LAUNCH_MATRIX_AR.md](../commercial/SOFT_VS_PAID_LAUNCH_MATRIX_AR.md)
