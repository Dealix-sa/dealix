# استراتيجية العميل المثالي — ICP Strategy

> Current ICP, expansion rules, when to add a new ICP.

## Purpose
Stay disciplined about who Dealix sells to. Resist the founder pull to chase shiny logos outside fit.

## Owner
Founder/CEO.

## Inputs
- Thesis (`STRATEGIC_THESIS.md`).
- Won and lost deal patterns (`docs/customer/` notes).
- Sector reports (`docs/sector-reports/`).
- Pipeline state (`docs/revenue/PIPELINE_STAGES.md`).

## Outputs
- Active ICP definition (this file).
- ICP-fit score in proposals (`templates/PROPOSAL_*.md.j2`).

## Rules
1. One primary ICP at a time. A secondary ICP is allowed only after the primary has 5 PSDE.
2. Every proposal records an ICP-fit score (0–10). Proposals < 6 require a written waiver from the founder.
3. Adding a new ICP requires: 3 paid sprints in the candidate sector + 2 successful deliveries + 1 retainer attempt.
4. ICP changes are made in the Monthly Strategy Review, not mid-week.
5. "Logo lust" — pursuing a famous customer outside ICP — requires an A3 Go/No-Go gate.

## Metrics
- % proposals at ICP-fit ≥ 7: target ≥ 80%.
- Win rate by ICP-fit bucket: tracked.
- Retainer attach rate by ICP-fit: tracked (expected: higher fit → higher attach).

## Cadence
Reviewed monthly. Adjusted quarterly.

## Evidence
This file, plus ICP-fit scores in each proposal.

## Verifier
`make icp-verify` — checks every proposal in pipeline has an ICP-fit score.

## Runtime Command
`make icp-score proposal=<id>`

---

## Current primary ICP

**Saudi B2B operator, mid-market.**

| Dimension | Definition |
|---|---|
| Geography | Headquartered in Saudi Arabia, operates in KSA |
| Revenue | SAR 10M – 500M annual |
| Headcount | 30 – 500 employees |
| Sector (focus) | services, distribution, light manufacturing, contracting, retail with operational complexity |
| Buyer | founder / COO / commercial director / head of operations |
| Buyer authority | can sign SAR 50k–250k within 30 days |
| Pain | unclear commercial pipeline, undocumented delivery, no operational evidence to act on |
| Existing stack | mix of Excel + ERP + ad hoc CRM; some pilots of "AI" tools without measurable outcomes |
| Language | AR primary, EN secondary in commercial docs |
| Acceptance posture | will accept case-safe anonymized evidence; will refuse "AI guarantee" framing |

## ICP-fit scoring (10 points)

| Signal | Points |
|---|---|
| Geography KSA | 1 |
| Revenue band match | 2 |
| Buyer is the decision-maker | 2 |
| Decision cycle ≤ 30 days | 2 |
| Accepts case-safe evidence | 1 |
| AR primary docs welcome | 1 |
| No "guarantee revenue" demand | 1 |

Total ≥ 7 → strong fit. 5–6 → marginal, requires waiver. ≤ 4 → reject.

## Anti-ICP signals (auto-reject without waiver)
- Decision cycles > 60 days with no first payment.
- Demands a guarantee of revenue, conversion, or ROI.
- Refuses any anonymized evidence at all (zero artifact possible).
- Asks Dealix to run cold outreach or scraping.
- Requires Dealix to brand outputs as a different company (white-label primary).

## Secondary ICPs (allowed once primary has 5 PSDE)
Candidates to be activated by Monthly Strategy Review:
- KSA mid-market in regulated sectors (healthcare ops, finance back-office) — requires legal review.
- GCC operators with KSA exposure — requires `MARKET_ENTRY_DECISION.md` checklist met.

## When to add a new ICP
Per Rule 3 above: 3 paid sprints + 2 deliveries + 1 retainer attempt in the candidate sector. Document the move in the Monthly Strategy Review.

## When to drop an ICP
- 12 months without a PSDE in that ICP.
- Two consecutive quarters with negative gross margin in that ICP.
- Compliance or legal risk increases past acceptable threshold.

## القواعد العربية
1. عميل مثالي واحد رئيسي في كل وقت.
2. كل عرض يحمل درجة ملاءمة من 10. الأقل من 6 يحتاج تنازلًا مكتوبًا.
3. إضافة عميل مثالي ثانوي تتطلب 3 سبرنتات مدفوعة + تسليمَين + محاولة احتفاظ.

## Cross-links
- `STRATEGIC_THESIS.md`
- `GTM_STRATEGY.md`
- `docs/revenue/PIPELINE_STAGES.md`
- `MARKET_ENTRY_DECISION.md`
