# MODULE STATUS MAP — مصدر الحقيقة لحالة الوحدات

> **Rule:** Never present a `FUTURE`, `BETA`, `INTERNAL`, or `DOCS_ONLY` module as `LIVE`.
> Every feature/page/claim that names a capability must carry exactly one status label.

## Status labels (constitution)

`LIVE` · `BETA` · `INTERNAL` · `DOCS_ONLY` · `BLOCKED` · `FUTURE` · `DEPRECATED`

## Machine source of truth

The authoritative, evidence-linked claim ledger is **`dealix/registers/no_overclaim.yaml`**
(CI-gated). Its internal status legend maps to the constitution labels as:

| `no_overclaim.yaml` status | Constitution label | Meaning |
|---|---|---|
| `Production` | `LIVE` | built, tested, default-on, evidence-linked |
| `Partial` | `BETA` | available under flag / missing hardening |
| `Pilot` | `INTERNAL` | built, internal-only, not enabled by default |
| `Planned` | `FUTURE` | not built yet |
| — | `DOCS_ONLY` | described in docs, no running surface |
| — | `BLOCKED` | intentionally never enabled (e.g. live auto-send) |
| — | `DEPRECATED` | retired |

When this map and `no_overclaim.yaml` disagree, **`no_overclaim.yaml` wins** and this map is corrected.

## The 14 Operating Systems — status (conservative)

> Statuses below are the **public-claim ceiling**. If you are unsure, default to the lower label.
> Confirm against `no_overclaim.yaml` and the service registry (`api/routers/service_catalog.py`)
> before publishing any "LIVE" claim.

| # | Operating System | Public status | Notes |
|---|---|---|---|
| 1 | Command OS | `BETA` | executive command brief / next-action board surfaces exist |
| 2 | Market Intelligence OS | `BETA` | "Lite" scope ships inside the Command Sprint |
| 3 | Revenue OS | `BETA` | governed lead pipeline + decision passport (`/api/v1/leads`) |
| 4 | Proof OS | `BETA` | Proof Pack assembly; evidence levels L0–L5 |
| 5 | Delivery OS | `BETA` | Delivery Lite within the Sprint |
| 6 | Client OS | `BETA` | client memory / account scoring |
| 7 | Support OS | `INTERNAL` | support-desk scope; verify before public claim |
| 8 | Finance OS | `INTERNAL` | Moyasar links sandbox-by-default; live charge `BLOCKED` |
| 9 | Data OS | `BETA` | data quality / DQ score |
| 10 | Governance OS | `LIVE` | approval-first gate + no-overclaim register are enforced |
| 11 | Knowledge OS | `INTERNAL` | |
| 12 | Agent OS | `INTERNAL` | internal agent runtime |
| 13 | Partner OS | `FUTURE` | partner distribution is a growth plan, not a shipped product |
| 14 | Academy OS | `FUTURE` | academy-as-marketing is planned |

## Hard blocks (`BLOCKED` — never enabled in any environment)

- Live external auto-send (WhatsApp / Gmail / email)
- Cold WhatsApp / LinkedIn automation
- Scraping behind login or of personal data
- Moyasar live charge without explicit founder enablement
- Publishing a customer name/logo/quote without written approval

## How to use this map

- Writing page copy or a deck slide? Find the capability here; use its label; never round up.
- Adding a new claim? Add a row to `dealix/registers/no_overclaim.yaml` **and** the
  Claims Register (`docs/03_governance/CLAIMS_REGISTER.md`) before it ships.
