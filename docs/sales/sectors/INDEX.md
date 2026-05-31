# Saudi Sector Briefs · Index

> 13 sectors mapped to `auto_client_acquisition/sector_registry/saudi_taxonomy.yaml`.
> 10 deep briefs in this directory + 3 in `SECTOR_POSITIONING_TEMPLATE.md` (SaaS,
> fintech, logistics).
>
> Use these for prospect outreach personalization + closing pitch
> calibration.

## Files

| # | Sector | File | Entry offer | Status |
|---|--------|------|-------------|--------|
| 01 | SaaS / Technology | `../SECTOR_POSITIONING_TEMPLATE.md#Sector 1` | Sprint 499 | ✓ |
| 02 | Fintech / Finance | `../SECTOR_POSITIONING_TEMPLATE.md#Sector 2` | Custom AI / Growth | ✓ |
| 03 | Logistics | `../SECTOR_POSITIONING_TEMPLATE.md#Sector 3` | Starter Managed | ✓ |
| 04 | Healthcare | `04_saudi_healthcare.md` | Growth Managed | ✓ |
| 05 | Real Estate | `05_saudi_real_estate.md` | Sprint 499 | ✓ |
| 06 | Education | `06_saudi_education.md` | Growth Managed | ✓ |
| 07 | Retail / E-commerce | `07_saudi_retail_ecommerce.md` | Starter Managed | ✓ |
| 08 | Manufacturing | `08_saudi_manufacturing.md` | Growth / Custom AI | ✓ |
| 09 | Construction | `09_saudi_construction.md` | Custom AI | ✓ |
| 10 | Consulting (partner) | `10_saudi_consulting.md` | Partnership | ✓ |
| 11 | Tourism | `11_saudi_tourism.md` | Starter Managed | ✓ |
| 12 | Agencies (partner) | `12_saudi_agencies.md` | Partnership | ✓ |
| 13 | B2B Marketplaces | `13_saudi_b2b_marketplaces.md` | Growth / Custom AI | ✓ |

## Section structure (every brief)

1. Vital stats (Saudi-specific, is_estimate=true)
2. Common pain (top 5)
3. Why Dealix wins here
4. Recommended entry offer
5. Outreach hooks (3 bilingual)
6. Likely objections + responses
7. Decision-maker profile
8. Sample story (case-safe, hypothetical until real customer)
9. Doctrine angle
10. Success metrics (90 days)

## Doctrine reminders

- All numbers tagged `is_estimate=true` (Doctrine #6)
- No fabricated customer names in sample stories (Doctrine #4)
- Outreach hooks personalize per prospect; never bulk (Doctrine #1)
- Cold WhatsApp blocked across all sectors (Doctrine #2)
- LinkedIn DM is the cold-first-contact default (Doctrine #11 — manual only)

## How agents use these

The personalization agent
(`auto_client_acquisition/agents/personalized_outreach.py`) loads the
matching sector brief during draft generation:
- Extracts the relevant doctrine angle for that prospect's sector
- Pulls the strongest objection-handler if prior touch hit one
- Injects the recommended entry offer into proposals
- Uses outreach hooks as starting templates

## Maintenance

Quarterly review of each sector (founder owns):
- Vital stats refreshed from latest public reports
- Hooks updated based on which actually converted
- Decision-maker profiles validated with real customer data
- Sample stories upgraded from hypothetical to real (with permission)
