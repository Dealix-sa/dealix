# Data Room Index — فهرس غرفة البيانات

## Purpose
The structure of Dealix's investor data room — even if no investors are engaged yet. Building the data room from day one means evidence is filed as it occurs, not reconstructed under pressure. A clean data room is also a clean operating company.

## Owner
Founder.

## Inputs
- Operating documents (governance, policies).
- Commercial documents (SOWs, invoices, contracts).
- Trust / compliance artifacts (`docs/14_trust_os/`).
- Financial documents (`docs/finance/`).
- Product and engineering documents.
- HR and partner documents.

## Outputs
- The data room structure (this file).
- Live folder at `data-room/` (gitignored if necessary; access-controlled).
- Quarterly completeness audit.

## Structure
```
data-room/
  00_overview/
    01_company-overview.md         (links to docs/investor/COMPANY_OVERVIEW.md)
    02_one-pager.pdf
    03_team-bios.md
  01_corporate/
    01_articles-of-association.pdf
    02_commercial-registration.pdf
    03_cap-table.xlsx
    04_shareholders-agreement.pdf
  02_commercial/
    01_active-sows/
    02_signed-proposals/
    03_invoices/
    04_pipeline-snapshot.md
  03_product/
    01_architecture.md             (link to docs/product/ARCHITECTURE.md)
    02_roadmap.md                  (link to docs/investor/ROADMAP.md)
    03_productization-ladder.md
  04_financials/
    01_p-and-l.xlsx
    02_cash-flow.xlsx
    03_unit-economics.md
    04_financial-model.md          (link to docs/investor/FINANCIAL_MODEL.md)
  05_trust/
    01_pdpl-compliance.md          (link to docs/14_trust_os/)
    02_ai-policy.md
    03_incidents-log.md
  06_market/
    01_market-thesis.md            (link to docs/investor/MARKET_THESIS.md)
    02_sector-reports/             (link to docs/sector-reports/)
  07_people/
    01_role-map.md                 (link to docs/people/ROLE_MAP.md)
    02_org-chart.png
    03_key-contracts.pdf
  08_risk/
    01_risk-register.md            (link to docs/investor/RISK_REGISTER.md)
  09_metrics/
    01_metrics.md                  (link to docs/investor/METRICS.md)
    02_dashboards-snapshots/
  10_legal/
    01_ip-assignment.pdf
    02_template-contracts/
```

## Rules
1. No PII (client emails, national IDs) in shared sections; redacted before filing.
2. Named case studies require approval per `docs/content/CASE_STUDY_SYSTEM.md` before inclusion.
3. Access is granted per-investor, time-bound, watermarked.
4. No "soft" promises in the data room; the room contains evidence, not pitch.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projections.
6. Data room cannot be opened before proof gates 1-3 are passed (see `docs/investor/PITCH_DECK_OUTLINE.md`).

## Metrics
- Folder completeness rate.
- Document freshness (median age, target ≤ 90 days for active sections).
- Access events logged.

## Cadence
- Continuous filing.
- Quarterly completeness audit.

## Evidence
- Quarterly audit file `evidence/investor/data-room/<YYYY-Qn>_audit.md`.

## Verifier
Founder.

## Runtime Command
`make data-room-audit` — lists missing files, stale files, PII flags.

## Arabic Summary — ملخص عربي
هيكل غرفة البيانات بُني من اليوم الأول حتى تتراكم الأدلة طبيعيًا. لا بيانات شخصية، لا اقتباسات بلا موافقة، لا وعود ناعمة. القيم التقديرية ليست مُتحقَّقة.
