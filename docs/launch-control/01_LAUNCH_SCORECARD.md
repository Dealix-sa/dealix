# Launch Scorecard — Dealix — بطاقة قياس الإطلاق

Score readiness before the Go/No-Go decision. Each line is scored: **Green** (ready), **Amber** (ready with a noted risk), **Red** (blocks launch). Launch proceeds only when every P0 line is Green or an Amber is explicitly risk-accepted.

## A. Public website — الموقع العام

| # | Item — البند | Priority | Score |
|---|---|---|---|
| A1 | All 18 routes load (200), AR and EN where applicable | P0 | ☐ |
| A2 | Copy matches approved deck; no forbidden claims | P0 | ☐ |
| A3 | `robots.txt` and `sitemap.xml` correct | P0 | ☐ |
| A4 | JSON-LD validates with no overclaim | P1 | ☐ |
| A5 | Manual QA checklist complete | P0 | ☐ |

## B. Commercial positioning — التموضع التجاري

| # | Item | Priority | Score |
|---|---|---|---|
| B1 | Offer ladder in SAR matches across site and pricing | P0 | ☐ |
| B2 | Governing rule visible on home, trust, FAQ | P0 | ☐ |
| B3 | Five verticals live in AR and EN | P1 | ☐ |
| B4 | Case-method page states case-safe posture | P1 | ☐ |

## C. Safety & governance — السلامة والحوكمة

| # | Item | Priority | Score |
|---|---|---|---|
| C1 | No external send path is enabled anywhere | P0 | ☐ |
| C2 | API exposes read-only commercial endpoints only | P0 | ☐ |
| C3 | 400 drafts are review-only; none auto-sent | P0 | ☐ |
| C4 | Sensitive data not processed before agreement | P0 | ☐ |
| C5 | PDPL-aware handling reflected in copy and flow | P1 | ☐ |

## D. Analytics & schema — التحليلات والمخطط

| # | Item | Priority | Score |
|---|---|---|---|
| D1 | Analytics schema defined and review-only | P1 | ☐ |
| D2 | Metrics-schema endpoint returns expected shape | P1 | ☐ |
| D3 | No tracking that captures PII without basis | P0 | ☐ |

## E. Delivery prep — تجهيز التسليم

| # | Item | Priority | Score |
|---|---|---|---|
| E1 | Diagnostic delivery SOP ready | P1 | ☐ |
| E2 | Proposal templates ready and reviewed | P1 | ☐ |
| E3 | Pilot scope documented | P1 | ☐ |
| E4 | Founder review queue operational | P0 | ☐ |

## Scoring summary — ملخّص النتيجة

| Section | P0 Green | Open P0 | Decision input |
|---|---|---|---|
| A Website | ☐ / 4 | | |
| B Commercial | ☐ / 2 | | |
| C Safety | ☐ / 4 | | |
| D Analytics | ☐ / 1 | | |
| E Delivery | ☐ / 1 | | |

**Launch readiness = all P0 Green.** Any Red P0 = No-Go. Carry the result into `02_GO_NO_GO_MATRIX.md`.

## Arabic summary — ملخص عربي

تُقيَّم الجاهزية عبر الموقع، التموضع التجاري، السلامة، التحليلات، وتجهيز التسليم. لا ننطلق إلا إذا كانت كل بنود الأولوية القصوى خضراء أو تم قبول مخاطرتها صراحةً. أي بند أحمر بأولوية قصوى يعني «لا انطلاق».

## Related — روابط

- `docs/launch-control/02_GO_NO_GO_MATRIX.md`
- `docs/launch-control/03_EVIDENCE_PACK.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
