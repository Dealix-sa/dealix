# Revenue Engine v2 — Operating Manual

**Version**: 2.0  
**Wave**: 2  
**Last updated**: 2026-06-10

---

## Purpose

The Revenue Engine generates a complete daily commercial pack from existing data sources.
It does NOT send anything. All output is a draft for founder review.

---

## Daily Output (company/runtime/revenue/YYYY-MM-DD/)

| File | Content |
|------|---------|
| `DAILY_OFFER.md` | Recommended offer to push today + supporting message |
| `TOP20_TARGETS.csv` | Top 20 scored outbound targets |
| `WHATSAPP_DRAFTS.md` | Personalized WhatsApp messages per target |
| `EMAIL_DRAFTS.md` | Email drafts per target |
| `LINKEDIN_POST.md` | One LinkedIn post draft (Arabic) |
| `PROPOSAL_STUBS.md` | Proposal summaries for top 5 targets |
| `WEBSITE_BRIEF.md` | Website update brief for today's offer focus |
| `CEO_REVENUE_REPORT.md` | Full daily revenue pack summary |

---

## Data Sources

| Source | Path |
|--------|------|
| Lead research CSVs | `company/lead_research/*/web_lead_research.csv` |
| Founder OS targets | `founder_os/output/*/daily_targets.csv` |
| CRM pipeline | `company/crm/pipeline.csv` |
| Approval queue | `company/outbox/` |

If no lead data exists, falls back to sector-based research targets.

---

## Running the Engine

```bash
# Full revenue day
./scripts/dealix_revenue_day.sh

# Python engine only
python company/revenue_engine/revenue_engine_v2.py
```

---

## Rules

- Never send WhatsApp, email, or LinkedIn automatically
- All output is draft — founder reviews and sends manually
- Never commit runtime output (`company/runtime/` is gitignored)
- No Docker, no npm, no external API calls
- Fallback data used when no live leads exist
