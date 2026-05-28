# Dealix · Investor One-Pager (founder-funded snapshot)

> **Status (2026-Q2):** founder-funded, not currently raising. Document
> kept for future optionality + alignment record.

---

## What we do · ما نعمله

**Dealix is a revenue OS for Saudi B2B.** Founders use Dealix to run
outreach, manage sprints, capture proof events, and operate compliance
— all while every customer-facing message passes through founder
approval (no autonomous send).

**One-line:** revenue OS with doctrine-grade governance — every
outbound passes founder approval, every metric ties to a proof
event.

---

## Why this market, why now

- **Saudi Vision 2030** mandates AI-driven B2B transformation across
  sectors → 14,000+ companies need governance-native AI partners.
- **PDPL enforcement** (Sep 2024) makes governance non-optional.
  Vendors without lawful-basis tracking face 5M SAR penalties per
  violation.
- **ZATCA Phase 2** requires e-invoicing on every transaction —
  most B2B SaaS in MENA hasn't wired it.
- **Founders trust transparency.** Existing AI tools promise
  "set and forget"; Saudi B2B founders learned (post-2023) that
  autonomous outreach destroys brand reputation.

Dealix sits at the intersection of these three forces with
zero direct competitor that combines all three.

---

## Traction (honest, no inflation)

> **Doctrine #8 NO_FAKE_PROOF:** every number below either traces to
> a verified event or carries `is_estimate=True`. Empty cells stay
> empty.

| Metric | 2026-Q1 | 2026-Q2 target | Source |
|--------|---------|----------------|--------|
| Customers paying | (TBD) | 2-3 managed-ops | payment_ops ledger |
| MRR (SAR) | (TBD) | 8,000-10,000 | renewal_scheduler |
| Sprint customers completed | 0 | 3-5 | sprint_runner tracker |
| Case studies published | 0 | 1-2 | proof_ledger L4+ |
| LinkedIn following | (TBD) | grow ≥ 25% | LinkedIn analytics |
| Founder hours/week | 50+ | ≤ 35 | manual log |

The empty cells are deliberate — founder has been building
infrastructure (current codebase) before commercial launch. Real
traction begins post-Moyasar KYC (Q2 2026).

---

## Business model

Five offers (transparent pricing, see
`docs/playbooks/FAQ.md`):

| Offer | Price | Margin (gross) |
|-------|-------|----------------|
| Free Diagnostic | 0 SAR | N/A — lead-gen |
| 1 SAR Pilot | 1 SAR | N/A — smoke test |
| 7-day Sprint | 499 SAR | ~95% |
| Starter monthly | 999 SAR/mo | ~92% |
| Growth monthly | 2,999 SAR/mo | ~93% |
| Scale monthly | 7,999 SAR/mo | ~94% |
| Custom AI | 5-25K SAR | ~85% |

**Gross margins** are high because Dealix is a software-product +
founder time hybrid, not a service-heavy business. The founder time
is the constraint — we cap engagements at 25 active customers per
solo founder (per our 90-day plan).

---

## Doctrine (the moat)

We refuse 11 things by code, regardless of customer demand:

1. No autonomous external sends
2. No cold WhatsApp
3. No scraping
4. No fake proof
5. No unconsented data
6. No unverified outcome guarantees
7. No hidden pricing
8. No silent failures
9. No unbounded agents
10. No unaudited changes
11. No LinkedIn automation

These are **not marketing** — they are CI gates that break merge on
violation (`tests/test_doctrine_guardrails.py`). Customers and
partners can audit the code at github.com/VoXc2/dealix.

**The moat thesis:** in Saudi B2B, brand trust is everything. Every
competitor that automates aggressively will eventually face a brand
collapse. Dealix's discipline becomes commercial advantage at the
3-year mark.

---

## Team

**Founder:** Sami Assiri — software engineer + B2B operator with
local Saudi network. Founder-funded, working solo at 50+ hrs/week
through 2026-Q3.

**Advisors:** rotating informal — no formal cap-table claims.

**Hires planned:**
- 2026-Q4: first revenue ops hire (after 50K SAR MRR)
- 2027-Q1: first engineer (after 100K SAR MRR)

---

## Capital posture

Current: **founder-funded, no debt**. Bootstrapped operating costs
are minimal (~3K SAR/month: Railway hosting + LLM tokens +
domains).

Not raising now because:
1. Founder optimization is for **customer value per hour**, not
   investor return per quarter.
2. Doctrine compliance is best maintained when no growth pressure
   from external capital.
3. The unit economics (>92% gross margin on subscriptions) mean
   organic profitability is reachable at 15-25 customers.

**Optionality:** if a strategic round becomes useful (e.g. for
enterprise sales motion or Saudi market expansion), we'd consider
SAFE notes at favorable terms only. Not seeking pitch meetings.

---

## What we'd discuss with an investor (if/when)

- **Saudi market depth + Vision 2030 alignment**
- **Doctrine as moat thesis**
- **Path from 25 customers (solo founder) → 100+ (team of 3-5)**
- **Saudi tech ecosystem strategic positioning**
- **Comparison to global revenue-OS plays (Clay, Apollo, etc.)
  and why Saudi-first wins locally**

---

## Anti-thesis (what would prove us wrong)

We try to be honest about failure modes:

- If governance discipline doesn't actually generate revenue (i.e.
  customers prefer aggressive automation despite churn), we'd need
  to revisit.
- If Saudi B2B AI adoption stalls (no Vision 2030 follow-through),
  TAM compression.
- If a well-capitalized international entrant builds Arabic-first
  governance better than us, defensibility shrinks.
- If founder burns out before reaching 25 customers, single-point-
  of-failure realized.

We watch each of these. Mitigations in
`docs/operations/DEALIX_READINESS.md`.

---

## Contact

For real conversations (not investor-pitch theater):
- Email: `sami.assiri11@gmail.com`
- WhatsApp: link on `dealix.sa`
- Calendly: 30 min "honest discussion" slot

No NDA required for the public materials. NDA before sharing
customer-specific data.

---

**Effective:** 2026-Q2. Updated quarterly. Last revision in
`docs/playbooks/CHANGELOG.md`.
