# خارطة تنفيذ 30 / 60 / 90 — Dealix (مواءمة CEO #6)

مرجع تشغيلي مرتبط بـ [STRATEGIC_MASTER_PLAN_2026.md](../STRATEGIC_MASTER_PLAN_2026.md) Part VI و [COMMERCIAL_OFFER_MESSAGING_AR.md](../commercial/COMMERCIAL_OFFER_MESSAGING_AR.md).

## أيام 1–30 — أول إيراد + إثبات

| # | مخرج | معيار نجاح |
|---|------|------------|
| 1 | نشر حي | `/health` + `git_sha` |
| 2 | Pipeline | 20 warm في `data/warm_list.csv`، 5 رسائل من `data/warm_list_personalized_drafts.yaml` |
| 3 | Discovery | ≥3 اجتماعات |
| 4 | إيراد | ≥1 دفعة (499 أو 9,500) |
| 5 | تسليم | kickoff + `POST /api/v1/commercial/engagements/lead-intelligence-sprint` أو sprint 499 |
| 6 | حوكمة | 0 `REVIEW_PENDING` في landing |

## أيام 31–60 — Proof + توسع

| # | مخرج | معيار نجاح |
|---|------|------------|
| 7 | Proof Pack موقّع | `docs/proof-events/` + عميل |
| 8 | Upsell | pitch Retainer 15k أو Pilot 22k |
| 9 | وكالات | 5 أسماء + 2 مكالمات — [AGENCY_MOU_OUTLINE_AR.md](../commercial/templates/AGENCY_MOU_OUTLINE_AR.md) |
| 10 | دفع | Moyasar حي + `reconcile_moyasar.py` يومياً |

## أيام 61–90 — تكرار + قناة

| # | مخرج | معيار نجاح |
|---|------|------------|
| 11 | عملاء | ≥2 مدفوعين (1 recurring) |
| 12 | وكالة | ≥1 MoU |
| 13 | إثبات | ≥3 ProofEvents موقّعة |
| 14 | علني | خدمة واحدة Live على `/status.html` (مرشح: `lead_intake_whatsapp` بعد 8 gates) |
| 15 | محتوى | case study بموافقة — [CASE_STUDY_TEMPLATE_AR.md](../commercial/templates/CASE_STUDY_TEMPLATE_AR.md) |

## تشغيل يومي (15 دقيقة)

```bash
python3 scripts/dealix_pm_daily.py --json
python3 scripts/founder_daily_scorecard.py --json
bash scripts/dealix_market_launch_ready_verify.sh
python3 scripts/ceo_top50_execute.py --run-next-7
```
