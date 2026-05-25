# المراجعة الأسبوعية للأعمال — CEO Business Audit

> Weekly score across six dimensions. One number, six inputs.

## Purpose
Convert a noisy week into a single audit score the founder cannot deceive themselves with. Force the founder to grade Dealix every Sunday.

## Owner
Founder/CEO.

## Inputs
- Cash position (`docs/finance/CASH_CONTROL.md`)
- Proof artifacts shipped this week (`docs/case-studies/`, `docs/14_trust_os/`)
- Retention signals (renewals, churns, escalations)
- Trust events (compliance, refunds, complaints)
- Learning events (docs updated, kills logged)
- Founder leverage (`FOUNDER_LEVERAGE_INDEX.md`)

## Outputs
- Audit score (0–100) in `dealix-ops-private/audit/YYYY-WW.md`
- One-line verdict + the worst dimension
- Action item tied to the worst dimension

## Rules
1. Score every Sunday, no exception.
2. Use the formula exactly — no "feel" adjustments.
3. If score < 60, the next week's focus is the worst dimension.
4. Three consecutive weeks below 60 triggers a Monthly Strategy Review out-of-cycle.
5. Audit is private. Never published externally.

## Metrics
- Weeks audited: 52 / year target.
- Average rolling 4-week score: target ≥ 70.
- Time to compute audit: ≤ 30 minutes.

## Cadence
Weekly, Sunday afternoon.

## Evidence
`dealix-ops-private/audit/YYYY-WW.md`.

## Verifier
`make audit-verify` — fails if this week's audit is missing past Sunday 23:59.

## Runtime Command
`make ceo-audit`

---

## The Formula

Score = (Cash × 0.25) + (Proof × 0.20) + (Retention × 0.15) + (Trust × 0.15) + (Learning × 0.10) + (Founder Leverage × 0.15)

Each dimension is scored 0–100.

### Cash (25%)
| Runway | Score |
|---|---|
| ≥ 12 months | 100 |
| 9–12 months | 85 |
| 6–9 months | 70 |
| 3–6 months | 50 |
| < 3 months | 20 |

### Proof (20%)
| Proof artifacts shipped this week | Score |
|---|---|
| 2+ (case study + trust artifact) | 100 |
| 1 | 70 |
| 0 but 2+ rolling 4-week | 50 |
| 0 | 0 |

### Retention (15%)
| Signal | Score |
|---|---|
| Retainer renewed or extended | 100 |
| No churn, no extension | 70 |
| Churn risk flagged + handled | 50 |
| Churn occurred | 20 |

### Trust (15%)
| Signal | Score |
|---|---|
| Zero open flags, 1+ trust artifact updated | 100 |
| Zero flags | 80 |
| 1 flag, owner assigned | 50 |
| Refund or complaint unresolved | 0 |

### Learning (10%)
| Signal | Score |
|---|---|
| 2+ docs updated from delivery | 100 |
| 1 doc updated | 70 |
| Kill logged | +20 bonus (cap 100) |
| Nothing | 0 |

### Founder Leverage (15%)
Pulled directly from `FOUNDER_LEVERAGE_INDEX.md` weekly score, scaled to 100.

## Verdict template
```
Week YYYY-WW Audit
Score: NN / 100
Worst dimension: <name>, score <NN>
Action next week: <one sentence>
Cash: <SAR> | Runway: <days>
```

## القواعد العربية
1. درجة كل أحد، بلا استثناء.
2. لا تعديلات "بالحس". الصيغة كما هي.
3. إذا كانت الدرجة أقل من 60، التركيز التالي على أسوأ بُعد.

## Cross-links
- `CEO_COMMAND_CENTER.md`
- `FOUNDER_LEVERAGE_INDEX.md`
- `docs/finance/CASH_CONTROL.md`
- `WEEKLY_CEO_REVIEW.md`
