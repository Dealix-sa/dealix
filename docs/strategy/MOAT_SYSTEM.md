# نظام الخنادق — Moat System

> The five moats: proof, governance, sector data, founder voice, sprint factory.

## Purpose
Make moats explicit and measurable. A moat that is not measured does not exist.

## Owner
Founder/CEO.

## Inputs
- Evidence library (`docs/case-studies/`, `docs/14_trust_os/`).
- Sector reports (`docs/sector-reports/`).
- Founder content (`docs/content/`).
- Sprint factory state (`docs/03_commercial_mvp/`).
- Trust dashboard (`docs/14_trust_os/TRUST_DASHBOARD.md`).

## Outputs
- Monthly moat score per moat (0–100).
- Direction (↑ ↓ →) vs previous month.
- Captured in `MONTHLY_MOAT_REVIEW.md`.

## Rules
1. A moat must have an owner, a metric, and an evidence path. No "soft" moats.
2. A moat scoring below 40 for two months triggers a bet.
3. A new moat is added only by Monthly Strategy Review approval after one quarter of evidence.
4. Founder cannot personally be the moat — the moat is what survives without the founder.
5. Marketing claims about moats require the matching metric to be ≥ 60.

## Metrics
- Average moat score across 5 moats: target ≥ 65 (steady state).
- Number of moats ≥ 60: target ≥ 4 of 5.
- Months with no moat declining: tracked.

## Cadence
Monthly score. Quarterly review.

## Evidence
`MONTHLY_MOAT_REVIEW.md`, evidence library, trust dashboard.

## Verifier
`make moat-verify` — confirms each moat has owner, metric, and current month's score.

## Runtime Command
`make moat-score`

---

## The Five Moats

### Moat 1 — Proof
**What**: Case-safe artifacts from completed paid sprints. Replicable, anonymized, dated.

**Owner**: Founder/CEO (delegated to evidence lead after Motion 2).

**Metric**: Number of case-safe artifacts ≥ 6 months old AND publicly shareable.

**Score scale**:
| Artifacts shareable | Score |
|---|---|
| ≥ 20 | 100 |
| 10–19 | 80 |
| 5–9 | 60 |
| 1–4 | 40 |
| 0 | 0 |

### Moat 2 — Governance
**What**: Trust pack, disclosure standards, refund policy, decision logs.

**Owner**: Founder/CEO.

**Metric**: Trust dashboard composite score (`docs/14_trust_os/TRUST_DASHBOARD.md`).

**Score scale**: Map dashboard score 0–100 directly.

### Moat 3 — Sector Data
**What**: Anonymized aggregated benchmarks in sector reports.

**Owner**: Founder/CEO.

**Metric**: Number of sectors with ≥ 5 PSDE feeding aggregated benchmarks.

**Score scale**:
| Sectors with ≥ 5 PSDE | Score |
|---|---|
| ≥ 3 | 100 |
| 2 | 70 |
| 1 | 40 |
| 0 | 0 |

### Moat 4 — Founder Voice
**What**: Published bilingual writing tied to evidence (not generic thought-leadership).

**Owner**: Founder/CEO.

**Metric**: Pieces published per quarter that cite a Dealix artifact AND get meaningful engagement.

**Score scale**:
| Pieces/quarter citing artifact | Score |
|---|---|
| ≥ 8 | 100 |
| 5–7 | 70 |
| 2–4 | 40 |
| 0–1 | 0 |

### Moat 5 — Sprint Factory
**What**: Sprint delivery templates running with low founder execution.

**Owner**: Founder/CEO → Delivery Lead.

**Metric**: % sprints completed in last 90 days with zero founder Delivery hours.

**Score scale**:
| % founder-free sprints | Score |
|---|---|
| ≥ 60% | 100 |
| 40–59% | 70 |
| 20–39% | 40 |
| < 20% | 10 |

## Anti-moats (things that look like moats but aren't)
- A custom tool only the founder can run.
- A relationship with one large customer (concentration, not moat).
- An NDA-locked case study with no shareable artifact.
- Award badges or vanity press.

## When a moat is at risk
- An artifact shareability drops (legal or customer pulled consent).
- The trust dashboard flags an open issue past SLA.
- Founder voice drops to zero for a quarter.

## القواعد العربية
1. لكل خندق مالك، مقياس، ومسار دليل.
2. الخندق الذي يسجّل أقل من 40 لشهرين يفعّل رهانًا.
3. المؤسس نفسه ليس خندقًا — الخندق ما يبقى بدونه.

## Cross-links
- `MONTHLY_MOAT_REVIEW.md`
- `STRATEGIC_THESIS.md`
- `docs/14_trust_os/TRUST_DASHBOARD.md`
- `docs/sector-reports/`
- `docs/case-studies/`
