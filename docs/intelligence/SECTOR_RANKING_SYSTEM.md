# Sector Ranking System

**Owner:** Strategy Office
**Source of truth:** This doc + `docs/intelligence/SAUDI_B2B_MARKET_MAP.md`

## Purpose

Sector ranking decides where Dealix invests next sprint cycles. It is a forced-choice exercise. Without it, the team chases whichever sector is loudest in the last week's inbound.

The system scores each candidate sector on 11 dimensions and produces a priority order.

## The 11 dimensions

| # | Dimension | Question | Scale |
|---|---|---|---|
| 1 | Saudi relevance | Is the sector materially present and growing in KSA? | 0-10 |
| 2 | B2B fit | Are sales B2B, not B2C? | 0-10 |
| 3 | High-ticket potential | Are deal sizes above SAR 50,000? | 0-10 |
| 4 | Buyer clarity | Can we name the buyer role precisely? | 0-10 |
| 5 | Pain urgency | Is the pain a current quarter problem? | 0-10 |
| 6 | Outreach fit | Is sanctioned, gated outreach feasible? | 0-10 |
| 7 | Proof fit | Can we produce dated, anonymizable proof in one sprint? | 0-10 |
| 8 | Partner potential | Are there integrators or consultancies to partner with? | 0-10 |
| 9 | Delivery complexity | How operationally complex is sprint delivery? (lower is better — score 10 = simple) | 0-10 |
| 10 | Trust risk | Does the sector carry regulatory or reputational risk? (lower is better — score 10 = low risk) | 0-10 |
| 11 | Priority weight | Founder strategic priority override | 0-10 |

## Scoring rules

- Each dimension is scored 0-10 in whole numbers.
- A sector's total score is the sum (max 110).
- A score must cite the evidence source — public market report, founder observation log, partner interview note.
- Scores are reviewed quarterly. Stale scores are flagged with `STALE` in the ranking table.

## Example ranking table (illustrative — replace with current quarter's data)

| Sector | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | Total | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cybersecurity B2B | 9 | 10 | 9 | 9 | 9 | 8 | 8 | 7 | 6 | 7 | 9 | 91 | A |
| ERP/CRM consulting | 9 | 10 | 9 | 8 | 8 | 8 | 8 | 8 | 6 | 8 | 8 | 90 | A |
| B2B SaaS (regional) | 8 | 10 | 8 | 9 | 8 | 8 | 8 | 7 | 7 | 8 | 7 | 88 | A |
| B2B agencies | 8 | 10 | 7 | 8 | 8 | 9 | 8 | 7 | 8 | 9 | 7 | 89 | A |
| Enterprise logistics | 9 | 9 | 9 | 7 | 7 | 7 | 7 | 7 | 5 | 7 | 7 | 81 | B |
| Consulting (boutique) | 8 | 10 | 7 | 8 | 7 | 8 | 7 | 7 | 7 | 8 | 6 | 83 | B |
| Enterprise services | 8 | 9 | 9 | 7 | 7 | 7 | 7 | 7 | 5 | 7 | 6 | 79 | B |
| High-ticket B2B (other) | 8 | 9 | 9 | 6 | 7 | 7 | 7 | 6 | 5 | 6 | 5 | 75 | C |

## Tiers

| Tier | Total | Action |
|---|---|---|
| A | 85-110 | Active focus; weekly account scoring runs |
| B | 70-84 | Pipeline build; monthly account scoring runs |
| C | 55-69 | Watch; quarterly check |
| Out | <55 | Out of scope; no sprint targeting |

## Decision rules

1. No more than four Tier-A sectors at any time. More than four splits operator attention beyond sustainable depth.
2. A sector cannot enter Tier A without at least one named, dated Proof Pack from that sector or an adjacent sector.
3. A sector exits Tier A if two consecutive quarters produce no closed sprint from that sector.
4. Trust risk score below 5 disqualifies a sector regardless of total.
5. Founder strategic priority (dimension 11) can override at most one tier movement per quarter.

## Sector entry checklist

Before a sector enters Tier A:

- [ ] ICP definition drafted (see `ICP_SEGMENTATION_SYSTEM.md`).
- [ ] Buyer persona drafted (see `BUYER_PERSONA_SYSTEM.md`).
- [ ] At least 3 trigger event patterns identified (see `TRIGGER_EVENT_SYSTEM.md`).
- [ ] At least 20 candidate accounts in the account scoring run (see `ACCOUNT_SCORING_MODEL.md`).
- [ ] At least 1 partner conversation logged.
- [ ] Sprint catalog mapped to sector pains.

## Sector exit checklist

- [ ] Two consecutive quarters with no closed sprint.
- [ ] No Proof Pack from the sector in the last 180 days.
- [ ] Strategy Office and Founder sign-off.

## Trust gate

| Action | Approval class |
|---|---|
| Score update (internal) | A1 — Strategy Office |
| Tier movement | A2 — Founder + Strategy Office |
| Sector exit | A2 — Founder + Strategy Office |
| Public sector scorecard | A3 — Founder |

## Failure mode

- Scores become stale; rankings drive decisions on year-old evidence.
- A sector enters Tier A on enthusiasm, not on the checklist.
- Six sectors all carry Tier A status simultaneously; operator focus collapses.

## Recovery path

1. Re-run quarterly review.
2. Force the count of Tier A sectors back to four.
3. Re-evidence each Tier A entry with a current Proof Pack reference.

## Disclaimer

Sector scores are directional and analyst-judged, not predictive. Dealix does not guarantee revenue or conversion outcomes from any sector. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
