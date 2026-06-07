# Dealix Pricing OS — `os/config/` (v2.0)

Source of truth for the **high-touch services** commercial model (Setup +
Monthly + Usage). This is a parallel track to the low-ticket productized ladder
(499/1,500/2,999/7,500) in `auto_client_acquisition/service_catalog/registry.py`
that powers Moyasar checkout — **do not conflate the two**.

| File | Purpose |
| --- | --- |
| [`pricing.yml`](pricing.yml) | Entry/Pilot/Production offers, discounts, payment terms, margin floors, governance gates |
| [`packages.yml`](packages.yml) | Monthly subscription packages + included usage allowance |
| [`usage_meters.yml`](usage_meters.yml) | Usage meters + overage pricing |

## Tooling

```bash
# Render a bilingual quote draft (never sends — founder approval required)
python scripts/generate_quote.py --client "Acme FM" \
    --offer maintenance_intelligence_os --package managed_os

# Check margin before sending a quote
python scripts/calculate_margin.py --price 150000 --cost 60000 --type project
```

## Rules

- All prices are **ex-VAT**; 15% VAT is added per ZATCA.
- Sharing a price with a customer requires **founder approval** (`os/01_CLAUDE.md`).
- Prices are **estimates**; language is a **commitment**, not a **guarantee**.
- High-touch invoices are issued manually (contract + ZATCA), not auto-charged.
- Doctrine `hard_gates` apply: `no_live_send`, `no_live_charge`, `no_cold_whatsapp`,
  `no_linkedin_auto`, `no_scraping`, `no_fake_proof`, `no_fake_revenue`, `no_blast`.

Sales-facing price books: [`sales/PRICE_BOOK_AR.md`](../../sales/PRICE_BOOK_AR.md) ·
[`sales/PRICE_BOOK_EN.md`](../../sales/PRICE_BOOK_EN.md) ·
[`sales/QUOTE_TEMPLATE.md`](../../sales/QUOTE_TEMPLATE.md). MRR model:
[`finance/mrr_model.csv`](../../finance/mrr_model.csv).
