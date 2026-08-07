# 00 — Final Launch Control Tower

نظام التحكم النهائي بتدشين Dealix التجاري — **يثبت** الجاهزية بأوامر واختبارات وأدلة، لا بالكلام.
The Final Launch Control Tower **proves** Dealix's commercial launch readiness with commands, tests, and evidence — not claims.

## ما الفكرة / What this is
A single control surface that turns "many files" into a verifiable launch room. It generates review-only
outreach drafts, audits them for safety, checks the website / media / CRM / API / secrets surfaces, and
emits one Go/No-Go verdict. **Everything is artifact-only, approval-first, and performs no external send.**

## ما الذي صار جاهزًا / What is ready (automated)
| Capability | Script | Output |
|---|---|---|
| 400+ review-only drafts | `scripts/commercial_generate_400_drafts.py` | `outputs/commercial_launch/latest/draft_queue.jsonl` |
| Safety audit | `scripts/commercial_safety_audit.py` | `.../safety_audit.json` |
| Commercial readiness | `scripts/commercial_launch_readiness.py` | `docs/commercial-launch/99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md` |
| Media/social 30-day plan | `scripts/media_social_calendar_generate.py` | `outputs/media_social/calendar_30_day.json` |
| Media/social verify | `scripts/media_social_verify.py` | `outputs/media_social/final_media_social_verification.json` |
| Website static QA | `scripts/site_launch_static_check.py` | `outputs/final_launch_control/site_static_check.json` |
| CRM schema verify | `scripts/commercial_crm_schema_verify.py` | `outputs/final_launch_control/crm_schema_verification.json` |
| API static check | `scripts/api_commercial_static_check.py` | `outputs/final_launch_control/api_commercial_static_check.json` |
| Secret/risk scan | `scripts/final_secret_and_risk_scan.py` | `outputs/final_launch_control/secret_risk_scan.json` |
| Master verification | `scripts/final_launch_control_verify.py` | `outputs/final_launch_control/final_verification.{json,md}` |

## ما الذي لا يزال يدويًا / What remains manual (by design)
- Founder review and approval of every draft.
- Actual outreach — sent **manually** by the founder after approval.
- Social posting — **manual** from the generated plan.
- Paid ads — **planning + copy only** until the ads readiness gate is cleared.
- Email program — only after SPF/DKIM/DMARC + Postmaster + reputation monitoring are in place.

## ما الذي ممنوع تنفيذه آليًا / What is forbidden to automate
Automated email sending · cold messaging automation · professional-network automation ·
website form auto-submit · bulk sending · scraping · paid-ads live launch without
tracking/compliance · external sending from GitHub Actions · processing sensitive data
before a signed agreement · any unproven claim · any blind deletion of the existing system.

## الروابط / Index
- Scorecard → [`01_LAUNCH_SCORECARD.md`](01_LAUNCH_SCORECARD.md)
- Go/No-Go → [`02_GO_NO_GO_MATRIX.md`](02_GO_NO_GO_MATRIX.md)
- Evidence pack → [`03_EVIDENCE_PACK.md`](03_EVIDENCE_PACK.md)
- 30-day war room → [`04_30_DAY_WAR_ROOM.md`](04_30_DAY_WAR_ROOM.md)
- Daily command center → [`05_DAILY_COMMAND_CENTER.md`](05_DAILY_COMMAND_CENTER.md)
- Failure response → [`06_FAILURE_RESPONSE_PLAYBOOK.md`](06_FAILURE_RESPONSE_PLAYBOOK.md)
- Founder checklist → [`07_FOUNDER_EXECUTION_CHECKLIST.md`](07_FOUNDER_EXECUTION_CHECKLIST.md)
- **Final verdict** → [`99_FINAL_CONTROL_TOWER_REPORT.md`](99_FINAL_CONTROL_TOWER_REPORT.md)

## كيف أثبت أن كل شيء سليم / How to prove it
```bash
python scripts/commercial_generate_400_drafts.py --target 400
python scripts/commercial_safety_audit.py
python scripts/commercial_launch_readiness.py
python scripts/media_social_calendar_generate.py
python scripts/final_launch_control_verify.py   # exit 0 == GO
```
