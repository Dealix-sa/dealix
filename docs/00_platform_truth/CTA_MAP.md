# Dealix — One-CTA Map

> Every P0 page has **exactly one** main CTA. Secondary links must use a non-primary visual
> variant. The gate `scripts/verify_dealix_cta_map.py` and the frontend guard
> `frontend/scripts/verify_wave3_content.mjs` enforce this.
>
> Machine-readable block below (`route | cta_id | cta_href`) is parsed by the verify script —
> keep the table format stable.

## CTA map

| route | cta_id | cta_label_en | cta_label_ar | cta_href |
|---|---|---|---|---|
| `/` | business_os_score | Get Business OS Score | احصل على Business OS Score | `/tools/business-os-score` |
| `/ar` | business_os_score | Get Business OS Score | احصل على Business OS Score | `/tools/business-os-score` |
| `/platform` | book_diagnostic | Book Diagnostic | احجز تشخيصاً | `/dealix-diagnostic` |
| `/command-sprint` | start_command_sprint | Start Command Sprint | ابدأ Command Sprint | `/start` |
| `/business-os` | book_diagnostic | Book Diagnostic | احجز تشخيصاً | `/dealix-diagnostic` |
| `/pricing` | start_command_sprint | Start Command Sprint | ابدأ Command Sprint | `/command-sprint` |
| `/industries` | get_sector_score | Get Sector Score | احصل على تقييم قطاعك | `/tools/business-os-score` |
| `/security` | book_diagnostic | Book Diagnostic | احجز تشخيصاً | `/dealix-diagnostic` |
| `/start` | submit_diagnostic | Submit Diagnostic | أرسل التشخيص | `submit` |

## Routing rule for growth assets

Every free tool, sector page, and answer page routes its single CTA to exactly one of:
- **Business OS Score** (`/tools/business-os-score`)
- **Diagnostic** (`/dealix-diagnostic`)
- **Command Sprint** (`/command-sprint` or `/start`)

No growth asset may CTA to an external destination or any auto-send action.
