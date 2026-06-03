# Prospect Research Report — تقرير بحث العملاء المحتملين

Researched + scored prospects and their pipeline status. **Source:**
[`../../docs/outreach/PROSPECT_RESEARCH_OS_AR.md`](../../docs/outreach/PROSPECT_RESEARCH_OS_AR.md) ·
code `dealix/market_production_os/prospect_scoring.py`.

## Pipeline — خطّ الأنابيب

| prospect_id | company | sector | source | score | qualified | status |
|---|---|---|---|---:|---|---|
| … | … | … | founder_input | … | yes/no | qualified |

## Health — المؤشرات

| Metric | Value |
|---|---:|
| Total prospects | … |
| Qualified (≥ 60) | … |
| Avg score | … |
| Do-not-contact | … |

Sources are lawful only (`founder_input`, `referral`, `inbound`, `event`,
`partner`, `public_directory`, `job_signal`) — **no scraping, no purchased
lists**. Titles only in `decision_maker_role`; no PII in `notes`.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
