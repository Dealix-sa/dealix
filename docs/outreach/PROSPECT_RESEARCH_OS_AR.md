# Prospect Research OS — نظام بحث العملاء المحتملين

Research and **score** Saudi B2B companies before any draft is written. We do
not target "everyone": every prospect carries a weighted score and a lifecycle
status. Sources are explicit and lawful — **no scraping, no purchased lists**.
Code: [`../../dealix/market_production_os/prospect_scoring.py`](../../dealix/market_production_os/prospect_scoring.py) ·
Schema: [`../../schemas/prospect.schema.json`](../../schemas/prospect.schema.json) ·
Parent: [`../market_production_os/README.md`](../market_production_os/README.md).

## Allowed sources — المصادر المسموحة

`founder_input` · `referral` · `inbound` · `event` · `partner` ·
`public_directory` · `job_signal`. The schema enum **excludes `scraping`** — a
scraped prospect cannot even be represented (NO_SCRAPING). Job signals come from
[`../signals/JOB_SIGNAL_PLAYBOOK_AR.md`](../signals/JOB_SIGNAL_PLAYBOOK_AR.md).

## Scoring rubric — معيار التقييم (100)

| Criterion | Weight | Earned when |
|---|---:|---|
| sector_fit / القطاع مناسب | 20 | sector is one of the 10 (not `other`) |
| expected_leads / فرص متوقعة | 20 | `has_expected_leads = true` |
| decision_maker_clear / صاحب القرار واضح | 15 | `decision_maker_clear = true` |
| pain_clear / ألم واضح | 15 | `pain_clear = true` |
| payment_capacity / القدرة على الدفع | 15 | high=15 · medium=10 · low=5 · unknown=0 |
| personalization / تخصيص متاح | 10 | P4=10 · P3=8 · P2=6 · P1=4 · P0=0 |
| low_risk / مخاطر قليلة | 5 | low=5 · medium=2 · high=0 |

**Qualify threshold:** total ≥ **60** → `qualify()` returns true. A prospect at
status `do_not_contact` never qualifies. Below threshold → `nurture`.

## Lifecycle — الحالات

`researched → qualified → draft_ready → drafted → approved → sent → replied →
meeting_booked → proposal_needed → proposal_sent → won` — plus the off-ramps
`lost`, `nurture`, `do_not_contact`. The status is the single source of truth
for where a company sits in the pipeline.

## Privacy — الخصوصية

`decision_maker_role` is a **title only**, never a person's name. `notes` must
not contain personal data (NO_PII). No national IDs, no personal phone/email in
the prospect record. Suppression matching is done on a sha256 hash — see
[`UNSUBSCRIBE_POLICY_AR.md`](UNSUBSCRIBE_POLICY_AR.md).

## Daily flow — التدفّق اليومي

1. Add/refresh prospects from allowed sources into the prospect store.
2. `score_prospect()` + `qualify()` rank them.
3. Qualified prospects feed the [Draft Factory](COLD_EMAIL_DRAFT_FACTORY_AR.md).
4. Refresh personalization toward P2+ where possible (raises score + reply rate).

Sector-fit guidance lives in [`../sectors/README.md`](../sectors/README.md);
offer-fit in [`../commercial/DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
