# Dealix GCC Draft Factory

**Goal:** 300+ high-quality, bilingual, sector-specific outreach drafts per day across 6 GCC countries.

## What This System Does

```
Find 1,000–3,000 signals/day
→ Filter to 500 relevant companies
→ Enrich 300–500 company briefs
→ Generate 300+ personalized drafts (Arabic + English)
→ Generate follow-up sequences
→ Score every draft
→ Run quality gate + compliance gate
→ Put only the best 150–300 into Founder Review Queue
```

## Directory Structure

```
config/          — YAML configuration for countries, sectors, offers, compliance
memory/          — JSONL working memory (leads, drafts, replies, suppression)
agents/          — Agent instruction files
prompts/         — LLM prompt templates
scripts/         — Python pipeline scripts
outputs/         — Daily pipeline outputs and reports
.github/workflows/ — GitHub Actions for daily automation
```

## Daily Pipeline

1. **GCC Market Scanner** → raw_leads.jsonl
2. **Company Researcher** → company_briefs.jsonl
3. **Language Detector + Sector Classifier** → classification layer
4. **Buyer Mapper + Pain Hypothesis + Offer Router** → company enrichment
5. **Arabic + English Draft Writers** → draft_queue.jsonl
6. **Quality Gate + Compliance Gate** → pass/fail scoring
7. **Founder Review Ranker** → review_queue/
8. **Founder Review Report** → reports/

## Countries Covered

Saudi Arabia · UAE · Qatar · Kuwait · Bahrain · Oman

## Priority Sectors

Legal · Consulting · Facilities Management · Real Estate · International Companies ·
Healthcare Admin · Education & Training · Contracting · Logistics · B2B Services · Financial Services

## Key Rules

- `send_allowed: false` on every draft until founder approves
- All sends require founder review
- Suppression list checked before every send
- Opt-out included in every message
- No guaranteed ROI claims
- No generic AI language

## Compliance

Each country's data protection law is configured in `config/compliance.yml` and `config/countries.yml`.
This system is an operational guide, not legal advice.

## Run Locally

```bash
cd dealix-gcc-marketing-os/scripts
python gcc_daily_pipeline.py
```
