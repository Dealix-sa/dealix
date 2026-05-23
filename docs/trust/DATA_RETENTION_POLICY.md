# Data Retention Policy

How long Dealix keeps which data, and why.

## Categories

| Category | Retention | Storage | Notes |
|---|---|---|---|
| Public source data | Indefinite | Public repo / ops folder | Sources logged |
| Client intake data | Length of engagement + 24 months | Private ops folder | Restricted access |
| Client business data shared with consent | Length of engagement + 12 months | Private ops folder | Encrypted at rest |
| Outreach logs | 24 months | Private ops folder | For suppression and audit |
| Payment records | 7 years | Finance system | Saudi accounting requirements |
| Personal communications | 24 months | Private ops folder | Then archived or deleted |
| Suppression list | Indefinite | Private ops folder | Append-only |

## Process
- Each client folder carries a `retention.yaml` with the start date, category, and scheduled review date.
- A monthly review checks for items past retention and either archives or deletes them.
- Deletion is logged in `dealix-ops-private/trust/deletion_log.csv`.

## Rule
Data we do not need is data we do not keep. Storage is cheap; trust is expensive.
