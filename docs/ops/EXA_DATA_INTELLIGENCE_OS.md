# Exa Data Intelligence OS

Dealix uses Exa as a research connector for Riyadh-focused market intelligence, revenue research, company brain signals, market watch, and proof-pack evidence.

## Purpose

Turn web evidence into a daily operating queue for founder review. Exa is not treated as a chat search box. It is treated as one connector inside Dealix Agentic Command Room OS.

## Operating rules

- `EXA_API_KEY` must live only in environment variables, Railway variables, or GitHub secrets.
- The repository must never contain a real Exa key.
- Highlights and source URLs are preferred before raw full text.
- Every reviewed row must preserve `source_url`.
- Every output is review-first.
- Publishing, CRM mutation, and billing remain outside this connector.
- No guaranteed ROI, fake customer claims, or unsupported proof.

## Products powered

1. Data Intelligence OS
2. Revenue Command Room OS
3. Company Brain OS
4. Market Watch OS
5. Proof Pack OS
6. Client Diagnosis Sprint

## Daily Riyadh loop

```text
Riyadh sectors
→ Exa query plan
→ evidence/highlights
→ normalized review rows
→ ledgers/riyadh_exa_prospects.csv
→ reports/intelligence/latest.md
→ founder decision
→ approved rows move to ledgers/prospects.csv
→ revenue-daily / command-room
```

## Environment

```env
EXA_API_KEY=
EXA_BASE_URL=https://api.exa.ai
EXA_DEFAULT_SEARCH_TYPE=auto
EXA_DEEP_SEARCH_TYPE=deep
EXA_NUM_RESULTS=10
EXA_ALLOW_LIVE_SEARCH=true
EXA_STORE_RAW_TEXT=false
EXA_REQUIRE_SOURCE_URL=true
EXA_REQUIRE_HUMAN_REVIEW=true
```

## Commands

```bash
python scripts/intelligence/run_data_intelligence_day.py
python -m pytest -q tests/test_exa_data_intelligence_os.py tests/test_data_intelligence_no_live_outbound.py
```

## Definition of done

- `reports/intelligence/latest.md` exists.
- `reports/intelligence/latest.json` exists.
- `ledgers/riyadh_exa_prospects.csv` exists.
- Every row is review-first.
- Exa key is not committed.
- No live action flag is enabled by this connector.
