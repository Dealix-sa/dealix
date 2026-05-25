# Dealix Founder / CEO Operating Layer

> Start here every morning.

```
make audit       # nightly trust audit on the public docs surface
make stage       # one-time: scaffold dealix-ops-private/
make daily       # open today's brief
make kit         # show the Revenue Sprint Kit
make dashboard   # refresh the Master CEO Dashboard
make weekly-close   # run the weekly review (Fridays)
make close-day   # end-of-day evidence
```

## The Twelve Systems

| # | System | Folder |
|---|--------|--------|
| 01 | CEO Command | `docs/founder/` (this dir) |
| 02 | Strategy | `docs/strategy/` |
| 03 | Revenue | `docs/revenue/` |
| 04 | Sales | `docs/sales/` |
| 05 | Delivery | `docs/delivery/revenue_sprint/` |
| 06 | Trust & AI Governance | `docs/trust/` + `docs/ai_management/` |
| 07 | Finance | `docs/finance/` |
| 08 | Client Success | `docs/client_success/` |
| 09 | Productization | `docs/product/` |
| 10 | Engineering | `docs/product/` + DORA tracking |
| 11 | Brand & Content | `docs/content/` |
| 12 | People / Partners / Scale | `docs/people/` + `docs/partners/` |

## The Two Halves

- **Public (this repo):** docs, templates, policies, playbooks, indexes.
- **Private (`dealix-ops-private/`, gitignored):** customer-named data,
  ledgers, drafts, decisions, time logs, financial records.

See `PUBLIC_PRIVATE_BOUNDARY.md` for the rule.

## Core Files In This Directory

| File | Purpose |
|------|---------|
| `CEO_OPERATING_SYSTEM.md` | Master operating model |
| `CEO_COMMAND_CENTER.md` | Daily live reference |
| `DAILY_COMMAND_BRIEF.md` | Daily template |
| `WEEKLY_CEO_REVIEW.md` | Weekly template |
| `MONTHLY_STRATEGY_REVIEW.md` | Monthly template |
| `GO_NO_GO_DECISION_SYSTEM.md` | Major decision gate |
| `DECISION_QUALITY_SYSTEM.md` | Decision rubric |
| `FOUNDER_TIME_ACCOUNTING.md` | Where the hours go |
| `KILL_LIST.md` | What we are not doing |
| `BOARD_PACK_TEMPLATE.md` | Monthly board pack |
| `90_DAY_CEO_PLAN.md` | The 90-day plan |
| `MASTER_DASHBOARD.md` | Dashboard spec |
| `PRIVATE_OPS_LAYOUT.md` | Private layout |
| `INDEX.md` | Founder docs index |

## Start

If you have never run this before:

```
make stage    # creates dealix-ops-private/ scaffolding
make daily    # opens today's brief
make kit      # shows the Sprint Kit
```

Then enter 25 real ICP-qualified leads in
`dealix-ops-private/sales/pipeline.csv`.
The system becomes alive only after that.
