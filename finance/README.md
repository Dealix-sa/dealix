# Dealix Finance — MRR Model (v2.0)

`mrr_model.csv` encodes the four growth phases of the high-touch services track
toward **500,000 SAR MRR** with 20–25 strong B2B clients. All amounts are SAR,
**ex-VAT**.

## Price anchors (must match `os/config/packages.yml`)

| Package | Monthly (ex-VAT) |
| --- | --: |
| Managed OS | 15,000 |
| Growth + Ops OS | 25,000 |
| Command Center | 45,000 (range 25,000–60,000; per-client column varies by phase) |

## Phases

| Phase | Target MRR | Managed | Growth/Ops | Command Center | Usage | B2B clients |
| --: | --: | --: | --: | --: | --: | --: |
| 1 | 30,000 | 2 | 0 | 0 | 0 | 2 |
| 2 | 100,000 | 4 | 0 | 1 (40k) | 0 | 5 |
| 3 | 250,000 | 8 | 3 | 1 (55k) | 0 | 12 |
| 4 | 500,000 | 15 | 6 | 2 (50k) | 25,000 | 23 |

`computed_mrr_sar = managed×15,000 + growth_ops×25,000 +
command_center×command_center_mrr_each + usage_addons` — and it equals
`target_mrr_sar` for every row (verified by `tests/test_dealix_pricing_os.py`).

`expected_setup_cash_sar` is one-off Setup cash that lands alongside the MRR
(Audits/Pilots/Production setup) — it funds growth and is **not** part of MRR.

## Source of truth

Prices live in [`os/config/`](../os/config/). This CSV is a planning model, not a
billing record. Actual MRR comes from signed contracts and ZATCA invoices; never
inject invented CRM numbers here.
