# Lead Table Standard

## Purpose
A common shape for every lead table Dealix ships to a customer.

## Columns
1. `company_name` — full registered name.
2. `sector` — Primary ICP sector value.
3. `region` — city or KSA region.
4. `contact_name` — primary contact full name.
5. `contact_role` — title.
6. `contact_email` — work email if available.
7. `contact_phone` — KSA-format phone if available and willingly shared.
8. `buying_signal` — short text on the public reason this lead matters.
9. `priority` — A/B/C.
10. `notes` — any context.

## Quality bar
- 0 rows with missing `company_name` or `sector`.
- ≤ 5% rows with missing `contact_email` AND `contact_phone`.
- 100% rows have a `buying_signal`.

## Privacy
- No data sourced from leaked databases.
- No personal data of individuals outside the buyer's permitted use.
- Customer agrees on file what they will and won't use the data for.

## Format
- CSV file delivered in UTF-8 with a header row.
- File name: `<client_slug>__lead_table__<YYYY-MM-DD>.csv`.
- Stored at `clients/<slug>/lead_table.csv`.

## QA score impact
- Missing columns: -20 from QA score.
- > 5% missing contact info: -10.
- Duplicates: -10.
