# 01 — Launch Scorecard

Score من 100 لكل محور، مع الدليل والعائق والمالك والإجراء التالي.
Each axis scored /100 with evidence, blockers, owner, next action. Scores reflect the
**verifiable, doctrine-compliant** state of this repo (artifact-only, no external send).

| Axis | Score | Evidence | Blockers | Owner | Next action |
|---|---|---|---|---|---|
| Website | 80 | `apps/web/app/*` pages + `site_static_check.json` | Manual browser QA pending | Founder | Run `100_SITE_MANUAL_QA_CHECKLIST.md` |
| SEO | 70 | metadata in `apps/web` layout; sitemap/robots advisory | sitemap/robots to confirm | Founder | Add `robots.ts`/`sitemap.ts` if missing |
| Commercial Offer | 90 | `99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md` | — | Founder | Confirm pricing in proposal pack |
| First 5 Verticals | 85 | `draft_queue.jsonl` (5 verticals) | Real account list | Founder | Replace synthetic with real leads |
| Draft Factory | 100 | 400+ drafts, `final_verification.json` | — | Engine | Daily run |
| Founder Review | 80 | `founder_review.md`, `top_50_priority.md` | Manual throughput | Founder | Review top 50 daily |
| Media OS | 85 | `00_MEDIA_SOCIAL_OS.md`, `calendar_30_day.json` | — | Founder | Post manually from plan |
| Social OS | 80 | `media_social_verify.py` PASS | Manual posting | Founder | Daily manual post |
| Ads OS | 60 | `15_ADS_READINESS_GATE.md` | Tracking/compliance gate | Founder | Clear ads gate before spend |
| CRM OS | 85 | `crm_schema_verification.json` PASS | Real pipeline data | Founder | Load approved leads |
| Delivery OS | 80 | existing `docs/27_delivery_playbooks` + sprint SOPs | — | Delivery | Run first sprint |
| Compliance | 90 | PDPL docs + no sensitive-data-before-agreement policy | — | Founder | Keep register current |
| Safety | 100 | `safety_audit.json` PASS, send_allowed=0 | — | Engine | Keep gate green |
| GitHub Actions | 95 | 4 artifact-only workflows, `contents: read` | — | Engine | Schedule runs |
| Server/API | 80 | `api_commercial_static_check.json` PASS | Live `/health` manual | Ops | Confirm health on deploy |
| Documentation | 95 | this folder + generated reports | — | Content | Keep synced |
| Tests | 95 | 14 launch-control test files PASS | — | Engine | Keep green in CI |
| External Requirements | 50 | see Evidence Pack | SPF/DKIM/DMARC, ads tracking | Founder | Complete before any send/spend |

> Scoring rule: a 100 means fully automated + verified; anything requiring a human decision or an
> external-provider setup is intentionally capped below 100 until that gate is cleared.
