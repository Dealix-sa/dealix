# مؤشرات الشمال — منتج / تجاري / امتثال

**YAML:** [`dealix/config/founder_north_star_metrics.yaml`](../../dealix/config/founder_north_star_metrics.yaml)  
**أمر:** `python scripts/founder_north_star_status.py` · `--skip-live` بدون إنترنت

**شمال أسبوعي:** Pilots نشطة + Proof Packs مسلّمة — يكمّل [`operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md`](operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md).

## ربط السكربتات

| التكرار | أمر |
|---------|-----|
| يومي | `bash scripts/run_founder_commercial_day.sh` |
| أسبوعي | `bash scripts/founder_weekly_loop.sh` |
| قبل نشر | `bash scripts/railway_ui_alignment.sh --with-smoke` |

يشمل **agent_queue_pending_p0** من `data/founder_agent/queue_today.json`.
