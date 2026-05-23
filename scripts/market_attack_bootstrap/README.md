# Market Attack Bootstrap Templates

These CSV files are the *template* schemas for the runtime
`<PRIVATE_OPS>` ops tree. They are **not** the runtime data. The
generator scripts in `scripts/generate_*` and the runtime bootstrapper
copy these into the private ops directory if no file is present there
yet, so that every site starts from a known-good schema.

Directory map:

```
market_attack/
  beachhead_sector_scorecard.csv
  strategic_accounts.csv
  offer_market_fit_tests.csv
  objection_library.csv
campaigns/
  campaign_registry.csv
  campaign_assets.csv
  campaign_queue.csv
  campaign_results.csv
sales_assets/
  sales_asset_registry.csv
authority/
  content_angles.csv
  sector_insights.csv
  founder_posts.csv
  report_ideas.csv
partners/
  partner_pipeline.csv
```

Each file is treated as **read-only seed data**. Do not put live
customer data here. Live data lives in the operator's private ops
tree (e.g. `/opt/dealix-ops-private`).
