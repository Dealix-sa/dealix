# Warm List — Scored & Prioritized | قائمة العملاء المحتملين — مُقيّمة ومرتّبة

<!-- Owner: Founder | Assembled: 2026-05-18 | Workstream B -->
<!-- Source: docs/ops/pipeline_tracker.csv (50 rows). This file SCORES that list. -->

> Scoring asset for the founder. It does not change the source list — it
> ranks it so the limited founder hours go to the highest-probability leads
> first. Outreach drafts for Tier 1 are in
> [`OUTREACH_DRAFTS_BATCH1.md`](OUTREACH_DRAFTS_BATCH1.md).

---

## 1. Scoring rubric | منهجية التقييم

Each lead is scored 0–100, the sum of three components. Higher = contact sooner.

### A. ICP fit — 0–50 | مطابقة العميل المثالي

Dealix's ICP is **a Saudi B2B company with a real revenue pipeline, a
reachable decision-maker, and structured pipeline/lead data to read.**

| Signal | Points |
|--------|--------|
| Saudi-based B2B with a genuine sales/partner pipeline | +20 |
| Decision-maker is a named founder / CEO / co-founder (not "TBD") | +15 |
| Has structured pipeline or lead data Dealix can read (CRM, exports, marketplace flow) | +10 |
| Sector where opportunity leakage is acute (SaaS, marketplace, fintech sales motion, contech quote flow) | +5 |

### B. Reachability — 0–35 | إمكانية الوصول

Can the founder actually start a doctrine-true conversation? No cold WhatsApp,
no scraping — so a real channel and warm context must exist.

| Signal | Points |
|--------|--------|
| Named individual with a known LinkedIn profile or email on file | +15 |
| Warm context exists (surname affinity, mutual network, public founder, app-store/partner overlap) | +12 |
| Channel is consent-appropriate (LinkedIn connect+note, email, Twitter DM to a public account) | +8 |

A lead with `company = TBD` and no named contact scores **0** on reachability —
it is not a warm lead yet; it is a research task.

### C. Freeze fit — 0–15 | ملاءمة التجميد

The freeze permits selling rung 0–1 only. Score how cleanly the lead maps to
the Free Diagnostic → 499 SAR Sprint motion.

| Signal | Points |
|--------|--------|
| Direct buyer for a Free Diagnostic on their own pipeline | +15 |
| Partner/agency lead — diagnostic is for *their client*; Partner OS (rung 5) is frozen, so pitch only the per-client diagnostic | +8 |
| B2C-leaning or booking-funnel business — weaker B2B-pipeline fit | +3 |

### Tiering

| Tier | Score | Action |
|------|-------|--------|
| **Tier 1** | 70–100 | First outreach. Drafts ready in BATCH1. Contact this week. |
| **Tier 2** | 45–69 | Second wave. Personalize after Tier 1 replies land. |
| **Tier 3** | 20–44 | Hold. Mostly partner/B2C-adjacent; revisit post-pilot. |
| **Research** | 0–19 | `TBD` placeholders. Not leads yet — name the contact first. |

---

## 2. Tier 1 — first outreach (contact this week) | الأولوية القصوى

Drafts for every Tier 1 lead are in [`OUTREACH_DRAFTS_BATCH1.md`](OUTREACH_DRAFTS_BATCH1.md).

| # | Lead | Company | Role | Score | Why Tier 1 |
|---|------|---------|------|-------|------------|
| 1 | عبدالله العسيري | Lucidya | CEO & Co-founder | **96** | Saudi B2B SaaS, named CEO + email on file, surname affinity = strong warm context, CXM team runs a real pipeline. |
| 2 | Ahmad Al-Zaini | Foodics | CEO & Co-founder | **89** | Saudi B2B SaaS, named CEO + email, public founder, restaurant-onboarding pipeline is a clean diagnostic scenario. |
| 3 | Hisham Al-Falih | Lean Technologies | CEO & Co-founder | **86** | Fintech-API B2B, named CEO, public founder, solutions-engineering pipeline with clear bottleneck. |
| 4 | Ibrahim Manna | BRKZ | Founder | **84** | Contech with a large quote/inside-sales pipeline; named founder; quote-flow leakage is an acute, nameable problem. |
| 5 | Nawaf Hariri | Salla | CEO | **82** | Saudi e-commerce platform, named CEO, public account (Twitter+LinkedIn); merchant-enablement pipeline. |
| 6 | Sultan Mofarreh | Zid | Co-founder | **79** | Saudi e-commerce platform, named co-founder, B2B merchant pipeline. |
| 7 | Mohammed Aldossary | Sary | Co-founder | **79** | B2B marketplace, named co-founder, 50K+ SMB retailer pipeline — opportunity leakage is structural. |
| 8 | Talha Ansari | Retailo | Co-founder | **76** | B2B retail marketplace (MENAP), named co-founder, real supplier/retailer pipeline. |
| 9 | Hatem Kameli | Lucidya | Co-founder | **74** | Same strong Lucidya ICP; second doorway into the account behind lead #1. |
| 10 | Mosab Alothmani | Foodics | Co-founder | **73** | Co-founder doorway into Foodics behind lead #2; same strong ICP. |
| 11 | SiFi CEO | SiFi | CEO | **72** | Corporate fintech, B2B sales motion into corporates; named role (CEO), reachable on LinkedIn. |
| 12 | Founder Logexa | Logexa | Founder | **71** | Logistics B2B, named founder role, pre-Series-A with an active sales pipeline and partner flow. |

**Founder note:** leads 9 and 10 are second contacts inside Lucidya and
Foodics. Do not message them in the same 48 hours as leads 1 and 2 — wait for
the primary contact to reply or go quiet first, so the account does not
receive parallel pitches.

---

## 3. Tier 2 — second wave | الموجة الثانية

Named or near-named contacts with solid ICP but thinner warm context or a
partner-only angle. Personalize after Tier 1 replies.

| # | Lead | Company | Score | Note |
|---|------|---------|-------|------|
| 9(CTO) | Abdullah Asiri (CTO) | Lucidya | 68 | Technical-angle contact; use only if the CEO/co-founder route stalls. |
| 12 | CEO Tamara | Tamara | 64 | BNPL fintech; large, but B2B-pipeline fit is indirect — diagnostic on partner/merchant onboarding. |
| 13 | CEO Mozn | Mozn | 63 | Peer AI company; reachable, but a peer-vendor conversation, not a clean buyer. |
| 16 | Founder Nana | Nana | 62 | Grocery delivery with a B2B supplier pipeline — the supplier side is the diagnostic scenario. |
| 17 | Founder Jahez | Jahez | 61 | Food delivery; restaurant-onboarding pipeline is the angle, similar to Foodics. |
| 14 | Founder Mnzil | Mnzil | 60 | Proptech Series A; B2B pipeline exists but contact not yet named. |
| 18 | Merit Incentives CEO | Merit Incentives | 57 | HR-tech B2B sales motion; contact role-named, not person-named. |
| 19 | Bayzat CEO | Bayzat Saudi | 56 | HR SaaS, KSA expansion; regional-lead contact, reachable on LinkedIn. |
| 21 | Hakbah CEO | Hakbah | 52 | Fintech with a B2B-partnerships pipeline; partnership angle. |
| 22–29 | Peak Content, Digital8, Brand Lounge, Qatar Digital, Wavy, Serviceplan, Intermarkets, MSL Saudi | Agencies | 46–50 | Partner-angle leads. Agency Partner OS (rung 5) is **frozen** — pitch only a Free Diagnostic for **one of their clients**. See `launch_content_queue.md` agency template. |

---

## 4. Tier 3 — hold | مؤجَّل

Lead #50 (Gym chain) and similar booking-funnel / B2C-leaning rows score
20–44 on weak B2B-pipeline fit. Not part of the first motion. Revisit after
the first paid pilot.

## 5. Research bucket — not leads yet | بحث مطلوب

Rows 30–49 in `pipeline_tracker.csv` are `company = TBD` placeholders
(Saudi tech founders, recruitment, EdTech, real-estate, healthcare,
automotive, insurance, distribution, construction, events, training, etc.).
Reachability score = 0 until a real named contact is identified. These are a
research task, not outreach targets. Do **not** draft messages to a `TBD`
contact — that risks drifting toward cold/bulk outreach.

> Healthcare/clinic rows in the source carry a "WhatsApp leads" note. That is
> a description of *their* inbound channel — it is **not** permission for
> Dealix to do cold WhatsApp. If these are ever activated, contact must be a
> named person on a consent-appropriate channel.

---

## 6. First-wave summary | ملخص الموجة الأولى

- **Tier 1: 12 leads.** Drafts ready in `OUTREACH_DRAFTS_BATCH1.md`.
- **Today's 5 (highest score):** Lucidya (96), Foodics (89), Lean (86),
  BRKZ (84), Salla (82).
- All outreach is manual, personalized, founder-approved, one at a time,
  max 5/hour. No automation, no bulk, no cold WhatsApp.

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
