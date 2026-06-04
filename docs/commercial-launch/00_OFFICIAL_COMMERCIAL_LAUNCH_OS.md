# Dealix — Official Commercial Launch Operating System

**Status:** Live · **Market:** Saudi Arabia + GCC · **Mode:** Review-only (no external sending)

Dealix is a Saudi/GCC B2B **AI Revenue & Operations OS**. The Commercial Launch
OS turns that product into a daily *commercial operating system*: it generates
daily opportunities, classifies them, writes high-quality bilingual drafts,
passes them through quality + compliance gates, and places them in a **Founder
Review Queue**.

> **The founder reviews, approves, and sends manually. The system does not send
> email, LinkedIn, WhatsApp, or run any real outreach.**

---

## What this OS does (and does not) do

| Does | Does NOT |
|------|----------|
| Generate ≥ 400 founder-review drafts/day | Send any email / message |
| Score every draft for quality + compliance | Auto-connect or auto-message on LinkedIn |
| Produce a CSV + Markdown + JSONL review queue | Cold-outreach on WhatsApp |
| Run a safety audit that fails on any send code | Scrape personal emails |
| Produce a daily Go/No-Go report | Store secrets or API keys |

## The 5 launch verticals

1. **Facilities Management & Maintenance** — إدارة المرافق والصيانة
2. **Contracting & Project Controls** — المقاولات وضبط المشاريع
3. **Real Estate & Property Operations** — العقار وإدارة الأملاك
4. **Legal & Professional Services** — المكاتب القانونية والخدمات المهنية
5. **Consulting, Training & B2B Services** — الاستشارات والتدريب وخدمات B2B

See [`01_FIRST_5_VERTICALS.md`](01_FIRST_5_VERTICALS.md) for full playbooks.

## The daily loop

```
seed leads (optional)  ─┐
config/*.json           ├─▶ commercial_generate_400_drafts.py ─▶ outputs/commercial_launch/<date>/
verticals + offers     ─┘            │
                                     ├─ quality gate  (>= 70)
                                     ├─ compliance gate (>= 70)
                                     ├─ safety audit (no send code, all blocked)
                                     └─ Founder Review Queue (CSV + MD + JSONL)
```

## Daily commands

```bash
# 1. Generate the queue (>= 400 review-only drafts)
python scripts/commercial_generate_400_drafts.py --target 400

# 2. Run the safety audit
python scripts/commercial_safety_audit.py

# 3. Check launch readiness (Go/No-Go)
python scripts/commercial_launch_readiness.py

# 4. (optional) Validate your real lead file
python scripts/commercial_seed_leads_validate.py --leads data/commercial_seed_leads.jsonl
```

## Daily outputs

Under `outputs/commercial_launch/YYYY-MM-DD/`:

- `draft_queue.jsonl` — every accepted draft
- `founder_review.csv` — sortable queue for the founder
- `founder_review.md` — full daily review with summary, top 50, top opportunities/risks
- `top_50_priority.md` — fast-scan priority list
- `rejected_drafts.jsonl` — drafts the gates rejected, with reasons
- `compliance_report.json` — compliance gate summary
- `safety_audit.json` — safety audit result
- `daily_metrics.json` — counts, distributions, target status
- `next_actions.md` — founder to-do list

## Index of this docset

| Doc | Purpose |
|-----|---------|
| [01_FIRST_5_VERTICALS](01_FIRST_5_VERTICALS.md) | Full playbooks per vertical |
| [02_OFFER_LADDER_SAR](02_OFFER_LADDER_SAR.md) | Offer ladder in SAR |
| [03_400_DAILY_DRAFT_FACTORY](03_400_DAILY_DRAFT_FACTORY.md) | How the factory works |
| [04_CHANNEL_POLICY](04_CHANNEL_POLICY.md) | Email/LinkedIn/WhatsApp/forms policy |
| [05_FOUNDER_DAILY_REVIEW_PLAYBOOK](05_FOUNDER_DAILY_REVIEW_PLAYBOOK.md) | How the founder reviews |
| [06_COMPLIANCE_AND_SAFETY_GATES](06_COMPLIANCE_AND_SAFETY_GATES.md) | Gates + safety audit |
| [07_SALES_MESSAGING_AR_EN](07_SALES_MESSAGING_AR_EN.md) | Bilingual messaging |
| [08_OBJECTION_HANDLING](08_OBJECTION_HANDLING.md) | Objections + responses |
| [09_GO_TO_MARKET_30_DAY_PLAN](09_GO_TO_MARKET_30_DAY_PLAN.md) | 30-day GTM plan |
| [10_COMMERCIAL_LAUNCH_READINESS_REPORT](10_COMMERCIAL_LAUNCH_READINESS_REPORT.md) | Readiness + Go/No-Go |
| [11_SOCIAL_AND_MEDIA_OS](11_SOCIAL_AND_MEDIA_OS.md) | Review-only social + media + ad-copy factory |
