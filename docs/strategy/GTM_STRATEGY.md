# استراتيجية الذهاب إلى السوق — GTM Strategy

> Founder-led sales → SDR-assisted → partner channel. In that order. No skipping.

## Purpose
Define the sales motion as a sequence of stages, each with entry and exit criteria. Resist scaling the next stage before unit economics support it.

## Owner
Founder/CEO.

## Inputs
- ICP definition (`ICP_STRATEGY.md`).
- Offer ladder (`docs/revenue/OFFER_LADDER.md`).
- Pipeline metrics (`docs/revenue/REVENUE_METRICS.md`).
- Capacity (founder time logs).

## Outputs
- Active GTM motion declared in this file.
- Monthly motion-fit review in `MONTHLY_STRATEGY_REVIEW.md`.

## Rules
1. Move to the next motion only when all exit criteria of the current motion are met for 2 consecutive months.
2. No automated outbound (email, LinkedIn, WhatsApp). All outbound is founder-personal, written by hand, with disclosure of who is sending.
3. No mass content campaigns until founder voice has 10 published pieces with measurable engagement.
4. Partner channel requires legal agreement reviewed under `docs/legal/` and a written carve-out of customer ownership.
5. Every motion stage produces evidence per quarter (case-safe templates, sector pieces).

## Metrics
- Stage-fit score: % months meeting all exit criteria.
- CAC by motion (founder hours × loaded cost + spend).
- LTV (per `REVENUE_METRICS.md`) / CAC ratio.
- Motion progression deadline misses: target 0.

## Cadence
Stage review monthly. Motion-change decision quarterly.

## Evidence
This file (motion declaration), pipeline reports.

## Verifier
`make gtm-verify` — checks current motion stated, exit criteria measured, no banned outbound listed.

## Runtime Command
`make gtm-review`

---

## The three motions

### Motion 1 — Founder-led
**Current state.**

- Source: founder network + warm intros + inbound from founder-published content.
- First contact: founder personally, AR or EN.
- Disqualification: ICP-fit < 5 → polite decline with referral if possible.
- Conversion: founder runs the Signal Sample call, writes the proposal, signs the work.

Exit criteria to move to Motion 2:
1. ≥ 6 PSDE in last 2 quarters.
2. Proposal-to-payment rate ≥ 30% (rolling 30 days).
3. Retainer attach rate ≥ 25%.
4. Founder Leverage Index ≥ 50.
5. Documented sales playbook (`docs/03_commercial_mvp/`).

### Motion 2 — SDR-assisted
**Future state, only after Motion 1 exit.**

- SDR handles first-touch qualification using a written script (no auto-send).
- Founder runs every Signal Sample call until 30 PSDE.
- All outbound is opt-in: warm intros, inbound from content, event follow-ups with consent.
- SDR compensation: weighted to qualified meeting → paid sprint, not to volume.

Exit criteria to move to Motion 3:
1. ≥ 24 PSDE per year.
2. Two delivery leads carrying sprints without founder execution.
3. Sprint-to-evidence rate ≥ 90%.
4. CAC payback ≤ 4 months.

### Motion 3 — Partner channel
**Distant state.**

- Partners (integrators, accountants, sector associations) refer qualified leads.
- Dealix delivers; partners earn a defined referral fee or co-delivery share.
- All partner agreements list explicit customer ownership terms.
- Partners must accept Dealix evidence and disclosure standards.

Exit criteria: none — this motion is steady-state.

## Banned tactics (any motion)
- Cold email at scale, even compliant — does not match the brand.
- LinkedIn automation tools.
- WhatsApp broadcast for cold contacts.
- Scraped contact lists.
- Pretending content is organic when it is paid (paid distribution is fine if labeled).

## Content as GTM input
Founder-published bilingual posts (`docs/content/LINKEDIN_POST_NNN.md`) feed Motion 1. Content is governed by `docs/brand/` voice rules. Content does not promise outcomes.

## القواعد العربية
1. الحركة الحالية: مبيعات يقودها المؤسس.
2. الانتقال للحركة التالية يتطلب استيفاء معايير الخروج لشهرين متتاليين.
3. لا تواصل بارد آلي بأي قناة. كل تواصل خارج العلاقات الدافئة يكون شخصيًا ومكشوف الهوية.

## Cross-links
- `ICP_STRATEGY.md`
- `DEALIX_GROWTH_SYSTEM.md`
- `docs/revenue/OFFER_LADDER.md`
- `docs/revenue/REVENUE_METRICS.md`
