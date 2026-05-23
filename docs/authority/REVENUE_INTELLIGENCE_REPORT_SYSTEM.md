# Revenue Intelligence Report System

> The quarterly long-form report Dealix publishes on a beachhead
> sector. Goal: become the most-cited primary source for that sector
> in Saudi B2B.

## Inputs

- Internal: `sector_insights.csv`, `campaign_results.csv`,
  `objection_library.csv`, `strategic_accounts.csv`.
- External: public regulator data, financial filings, MCI / SDAIA /
  Chamber publications.

## Structure (mandatory)

```
1. Executive summary (1 page)
2. Sector definition and 2024-2026 trajectory
3. Buyer behavior — what changed in the last 12 months
4. Frictions we observe (objection library, anonymized)
5. Investment signals — funding, hiring, regulation
6. Practical playbook for buyers
7. Methodology and limitations (always present)
```

## Governance

- Report ideas live in `<PRIVATE_OPS>/authority/report_ideas.csv`.
- Each report passes governance review before publishing.
- The methodology section is the truth gate — if a claim cannot be
  defended in methodology, it is removed.
- We never publish a "winners and losers" list with named private
  companies.

## Output

When published, the report and its proof index live under
`assets/sales/proof_safe/reports/`.
