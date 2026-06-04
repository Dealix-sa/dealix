# 03 — Evidence Pack

قائمة الأدلة المطلوبة لإثبات الجاهزية. كل بند له ملف أو أمر يولّده.
Required evidence to prove readiness. Each item has a file or command that produces it.

| Evidence | Source / command | Artifact |
|---|---|---|
| Command outputs | run the scripts in `00_FINAL_LAUNCH_CONTROL_TOWER.md` | console + JSON files |
| Test results | `pytest -q tests/test_final_launch_control_verify.py …` | CI log / local run |
| Workflow results | Actions → Final Launch Control | uploaded artifacts |
| Website build result | `cd apps/web && npm run verify || npm run build` | `site_static_check.json` + build log |
| API health result | `api_commercial_static_check.py` (+ live `/health` manual) | `api_commercial_static_check.json` |
| Safety audit result | `commercial_safety_audit.py` | `outputs/commercial_launch/latest/safety_audit.json` |
| Draft count result | `final_launch_control_verify.py` | `final_verification.json` (`draft_count`) |
| Secret scan result | `final_secret_and_risk_scan.py` | `outputs/final_launch_control/secret_risk_scan.json` |
| CRM schema result | `commercial_crm_schema_verify.py` | `crm_schema_verification.json` |
| Media/social result | `media_social_verify.py` | `final_media_social_verification.json` |
| README status | `final_launch_control_verify.py` | checks "Commercial Launch OS" + clone URL |
| Final reports status | this folder + generated `99_*` reports | markdown |

## كيف تجمع الحزمة كاملة / Assemble the full pack
```bash
python scripts/commercial_generate_400_drafts.py --target 400
python scripts/commercial_safety_audit.py
python scripts/commercial_launch_readiness.py
python scripts/media_social_calendar_generate.py
python scripts/site_launch_static_check.py
python scripts/media_social_verify.py
python scripts/commercial_crm_schema_verify.py
python scripts/api_commercial_static_check.py
python scripts/final_secret_and_risk_scan.py
python scripts/final_launch_control_verify.py
```
All artifacts land under `outputs/commercial_launch/`, `outputs/media_social/`,
and `outputs/final_launch_control/`.
