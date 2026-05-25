# Outreach Approval Queue — 2026-05-23 ERP / CRM Seed

## Batch
`acquisition/lead_batches/2026-05-23-erp-crm-seed.csv`

## Sector
Saudi ERP / CRM vendors

## Leads Count
25 total — 9 with verified URLs (priority A/B), 16 candidates requiring URL
verification before any send.

## Message Versions
- `erp_crm_v1_en` (first touch, English)
- `erp_crm_v1_ar` (first touch, Arabic)
- `erp_crm_v1_followup_en` (follow-up at day +4)
- `erp_crm_v1_followup_ar` (follow-up at day +4)

Full text in `acquisition/outreach_messages/erp_crm_v1.md`.

## Risk Review
- No guaranteed-revenue claim.
- No guaranteed-meeting / guaranteed-reply claim.
- No client data used.
- Uses public company fit only.
- Send requires Sami's explicit approval per row.
- Rows with `verification_status=URL_NEEDS_VERIFICATION` are blocked from
  the send queue until a verified URL and public contact path are recorded.

## Leads Summary
| # | Company | Priority | Verification |
|---|---|---|---|
| 1 | OdooTec | A | URL_VERIFIED |
| 2 | ALIA ICT | A | URL_VERIFIED |
| 3 | LOGIX ERP | A | URL_VERIFIED |
| 4 | Focus Softnet Saudi | A | URL_VERIFIED |
| 5 | SowaanERP | A | URL_VERIFIED |
| 6 | BetterTech Saudi | B | URL_VERIFIED |
| 7 | TeleNoc | B | URL_VERIFIED |
| 8 | Saudi Irsal | B | URL_VERIFIED |
| 9 | Megamind IT Solutions | B | URL_VERIFIED |
| 10 | Penieltech KSA | B | URL_NEEDS_VERIFICATION |
| 11 | Azdan Business Analytics | B | URL_NEEDS_VERIFICATION |
| 12 | RealSoft | B | URL_NEEDS_VERIFICATION |
| 13 | ebs (Emirates Business Solutions) KSA | C | URL_NEEDS_VERIFICATION |
| 14 | Bevatel | C | URL_NEEDS_VERIFICATION |
| 15 | Beetrix ERP | C | URL_NEEDS_VERIFICATION |
| 16 | Edara ERP | C | URL_NEEDS_VERIFICATION |
| 17 | Daftra | C | URL_NEEDS_VERIFICATION |
| 18 | Qoyod | C | URL_NEEDS_VERIFICATION |
| 19 | ZATCA-ready ERP partners (group) | C | URL_NEEDS_VERIFICATION |
| 20 | Microsoft Dynamics Saudi partner (candidate 1) | B | URL_NEEDS_VERIFICATION |
| 21 | Microsoft Dynamics Saudi partner (candidate 2) | B | URL_NEEDS_VERIFICATION |
| 22 | SAP Saudi partner (candidate 1) | B | URL_NEEDS_VERIFICATION |
| 23 | Salesforce Saudi partner (candidate 1) | B | URL_NEEDS_VERIFICATION |
| 24 | Zoho Saudi partner (candidate 1) | C | URL_NEEDS_VERIFICATION |
| 25 | HubSpot Saudi partner (candidate 1) | C | URL_NEEDS_VERIFICATION |

## Recommended Decision
1. Approve the message direction (`erp_crm_v1_en` / `erp_crm_v1_ar`).
2. Approve send for the 9 URL_VERIFIED rows once their public contact path
   is recorded in `acquisition/contact_discovery_queue.csv`.
3. Verify URLs + select named partners for rows 10–25 before approval.
4. Build Gmail drafts only — no auto-send.

## Sami Decision
Pending

## Approved Date
-

## Audit Log
- 2026-05-23 — batch created from web research (9 verified URLs + 16
  candidates).
