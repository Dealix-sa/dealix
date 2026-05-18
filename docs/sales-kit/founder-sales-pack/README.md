# Founder Sales Pack — حزمة مبيعات المؤسس

> Everything the founder needs to run a full Dealix sales motion starting tomorrow, with zero prep.
> الحزمة الكاملة لتشغيل دورة مبيعات Dealix بدءاً من الغد، دون أي تحضير مسبق.

Dealix sells **Governed Revenue Operations**: a radar that finds and scores revenue
opportunities and drafts approval-ready Arabic + English outreach. The founder approves
everything. **Nothing sends without explicit founder approval.** Every result is Proof-backed.

---

## What is in this pack — محتويات الحزمة

| # | File | Purpose |
|---|------|---------|
| 1 | [01_WARM_OUTREACH_FRAMEWORK.md](./01_WARM_OUTREACH_FRAMEWORK.md) | Personalizable bilingual outreach-draft framework + 4 fully-written example drafts for Saudi SME personas. |
| 2 | [02_QUALIFICATION_KIT.md](./02_QUALIFICATION_KIT.md) | Discovery-call script, qualifying questions, offer-recommendation logic, objection-handling sheet. |
| 3 | [03_PROPOSAL_TEMPLATES.md](./03_PROPOSAL_TEMPLATES.md) | Bilingual proposal templates: Free Diagnostic, 499 Sprint, 1,500 Data Pack, Managed Ops. |
| 4 | [04_FOUNDER_DAILY_CADENCE.md](./04_FOUNDER_DAILY_CADENCE.md) | Concrete daily operating rhythm: pipeline review, draft-approval block, follow-ups, call slots. |

---

## The offer ladder — سلم الخدمات

Source of truth: [`docs/OFFER_LADDER_AND_PRICING.md`](../../OFFER_LADDER_AND_PRICING.md). Do not invent prices.

| Tier | Offer | Price (SAR) | Unlock condition |
|------|-------|-------------|------------------|
| 0 | Free AI Ops Diagnostic | 0 | Any qualified first contact |
| 1 | 7-Day Revenue Proof Sprint | 499 (one-time) | Pain clear + owner + data ready |
| 2 | Data-to-Revenue Pack | 1,500 (one project) | + CSV/CRM export, PII handling needed |
| 3 | Managed Revenue Ops | 2,999–4,999 / month | After a successful pilot |
| 4 | Executive Command Center | 7,500–15,000 / month | After 3 completed pilots |
| 5 | Agency Partner OS | Custom + rev-share | After 3 Proof Packs |

This pack covers the **active** offers the founder sells tomorrow: Tiers 0, 1, 2, and 3.

---

## The 11 non-negotiables — الثوابت الأحد عشر

Every asset in this pack honors these. They are enforced by code, tests, and middleware.

1. No scraping of websites, social platforms, or third-party UIs.
2. No cold WhatsApp messaging or WhatsApp automation without recorded opt-in.
3. No LinkedIn automation (connection requests, messages, scraping, feed actions).
4. No source-less claims; every number or quote requires a Source Passport.
5. No guaranteed-outcome language ("we will close X deals", "guaranteed revenue").
6. No PII in application logs, friction logs, or telemetry.
7. No source-less knowledge answers; "source required" instead of invention.
8. No external action (send, charge, publish, share) without explicit human approval logged with identity + timestamp.
9. No autonomous workflow without a registered agent identity.
10. No project closure without a 14-section Proof Pack with a computed score.
11. No project closure without at least one reusable Capital Ledger asset.

**What this pack refuses:** cold automation, scraping, LinkedIn automation, mass-blast
content, and guaranteed-outcome promises. Every outreach asset here is **draft-only**,
reviewed and sent **manually** by the founder. There is no autonomous external sending.

---

## How to use this pack — كيفية الاستخدام

1. **Today (prep, 30 min):** read this README + the daily cadence. Confirm Moyasar is in
   live mode before sending any real proposal — run `python scripts/moyasar_live_cutover.py`
   if `launch-status` reports `moyasar.mode == "test"`.
2. **Tomorrow morning:** load your 20–50 real warm contacts into the framework in file 01.
   Personalize one draft per contact. Approve each draft yourself, then send manually.
3. **On reply:** run the discovery script (file 02), then run
   `auto_client_acquisition/sales_os/qualification.qualify(...)` to get a decision.
4. **On ACCEPT / DIAGNOSTIC_ONLY:** render the matching proposal from file 03.
5. **Every day:** follow the cadence in file 04.

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
