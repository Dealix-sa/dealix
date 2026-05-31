# Prospect File Schema · مخطط ملف الـ Prospects

> The exact CSV/Excel format Dealix accepts from the founder for bulk
> ingestion. Validated by `scripts/ingest_prospect_file.py`.
>
> **Effective:** 2026-06-01

---

## File format

- **Accepted:** CSV (UTF-8) or XLSX
- **Encoding:** UTF-8 (NOT UTF-16, NOT ISO-8859-1)
- **Header row:** required, must match column names below exactly
- **Empty cells:** OK for optional columns; required columns must be filled

## Required columns

| Column | Description | Example |
|--------|-------------|---------|
| `name_ar` | Prospect full name in Arabic | أحمد العتيبي |
| `name_en` | Prospect full name in English (Latin transliteration) | Ahmad Alotaibi |
| `company` | Company name (AR or EN, founder picks one consistently) | شركة الاتجاه |
| `sector_hint` | Sector code OR free text alias | saas / fintech / TECHNOLOGY |

## Optional columns

| Column | Description | Example |
|--------|-------------|---------|
| `title` | Current title at company | VP Sales / مدير المبيعات |
| `linkedin_url` | Full LinkedIn profile URL | https://linkedin.com/in/ahmad-alotaibi |
| `email` | Business email | ahmad@aletijah.sa |
| `phone` | Phone (E.164 format preferred) | +966501234567 |
| `referrer_name` | Who introduced you | عبدالله الفهد |
| `warm_consent_yes_no` | Has prospect agreed to WhatsApp contact? | yes / no / unknown |
| `notes` | Free text context (max 500 chars) | "Met at Riyadh Season tech event" |
| `priority_hint` | Founder's intuition (P0/P1/P2/BACKLOG) | P0 |

## Validation rules

The ingestion script enforces:

1. **Required columns:** `name_ar`, `name_en`, `company`, `sector_hint`
   must be non-empty per row
2. **Sector hint:** must normalize to a known sector code
   (TECHNOLOGY/FINANCE/HEALTHCARE/etc.) — otherwise OTHER
3. **LinkedIn URL format:** if provided, must start with
   `https://linkedin.com/in/` or `https://www.linkedin.com/in/`
4. **Phone format:** if provided, must be E.164 (`+966...`)
5. **Email format:** if provided, must contain `@` and a dot
6. **warm_consent_yes_no:** if blank or "unknown", defaults to "no"
   (Doctrine #2 — never assume warm consent)
7. **Max rows per file:** 500 (founder reviews per batch)

## Sample CSV

See `prospect_file_sample.csv` in this directory.

## What the script does per row

```
For each row:
  1. Validate required columns
  2. Normalize sector hint via sector_registry.normalize_hint()
  3. Generate Source Passport (PDPL Doctrine #5):
       lawful_basis: "legitimate_interest"
       source: "founder_provided_list"
       suppression_check: ledger lookup
       expires_at: now + 90 days
  4. Call scripts/research_prospect.py with the row data
       → writes data/prospect_briefs/{brief_id}.{md,json}
  5. Call scripts/generate_sequence.py with default channel
       (linkedin_dm if URL present, else email)
       → writes data/prospect_briefs/{brief_id}_sequence.json
  6. Queue all 3 touches in approval_center with batch_id
  7. Append row to data/prospect_ingestion_log.jsonl
```

## Founder's review after ingestion

Open `/ar/ops/approvals?batch_id={batch_id}`:
- See list of prospects with brief summaries
- For each: review the 3-touch sequence
- Approve / edit / reject per touch
- Send manually after approval (Doctrine #1)

## Doctrine guardrails

- **#1 no_live_send:** ingestion ONLY generates drafts; nothing
  sent automatically
- **#2 no_cold_whatsapp:** rows without `warm_consent_yes_no=yes`
  are restricted to LinkedIn DM / email
- **#3 no_scraping:** founder-provided lists only (legitimate
  interest under PDPL); we never enrich from scraped sources
- **#5 no_unconsented_data:** Source Passport recorded per row
- **#10 no_unaudited_changes:** every ingestion logged to
  `data/prospect_ingestion_log.jsonl` (append-only)

## Privacy considerations

If your file contains:
- **Personal email/phone (not business):** review with PDPL counsel
  before ingest
- **Sensitive personal data (health/financial details):** DO NOT ingest
- **EU data subjects:** GDPR rules apply; not currently supported
- **Minors:** explicitly excluded; remove before sending

## Maintenance

After ingestion:
- Briefs auto-expire 90 days (PDPL retention)
- Suppression list checked before every send
- Customer opt-out flows back to suppression_list immediately
- Quarterly review of ingestion log

## Example workflow

```bash
# 1. Founder prepares prospects.csv
# 2. Validate dry-run first
python3 scripts/ingest_prospect_file.py --file prospects.csv --dry-run

# 3. Live ingestion
python3 scripts/ingest_prospect_file.py --file prospects.csv

# 4. Review report
cat data/prospect_ingestion_log.jsonl | tail -1 | jq .

# 5. Founder opens approval queue
open https://api.dealix.me/ar/ops/approvals?batch_id=BATCH_xxx
```
