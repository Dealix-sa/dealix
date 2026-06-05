# Prospect Data Retention

> بيانات الأهداف = بيانات عمل عامة، بأقل قدر، ولمدة محدودة.

How the targeting OS stores and ages prospect data, aligned with Saudi PDPL
principles (data minimisation, purpose limitation, retention limits).

---

## What we store

Only **business** information from public sources:

- Company name, website, city, sector, services.
- Official contact channel (never a personal phone / personal email as the
  primary channel).
- Public signals (hiring, growth, case-study presence, etc.).
- Source URLs + evidence count.

Stored in `data/targeting/company_master.jsonl` and `outcomes.jsonl`.

## What we never store

- Personal phone numbers.
- Personal data beyond a publicly-listed business role title.
- Leaked / purchased datasets.
- Login-gated content.

---

## Retention

| Data | Default retention |
|------|-------------------|
| Rejected candidates | purge after the daily run (kept only as a reason row) |
| Nurture (C/B) not contacted in 90 days | review + purge or refresh |
| Outcomes ledger | retained for learning; anonymise on request |
| Customer folders | governed by the delivery engagement + contract |

## Rights

On a documented request, a company's prospect record is removed from the master
and outcomes ledger. Customer (paid) data follows the engagement's data
processing terms.

See `docs/03_governance/RESEARCH_SOURCE_POLICY.md` and the repo's broader PDPL
and compliance docs under `docs/25_compliance_trust/`.
