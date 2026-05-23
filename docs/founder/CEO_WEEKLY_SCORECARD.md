# CEO Weekly Scorecard — بطاقة أداء أسبوعية للمؤسس

## Purpose
A weekly self-scorecard for the founder. Honest, structured, signed. Captures the operating week across revenue, sales, delivery, trust, learning, founder discipline, and product. Filed every Friday before close-of-week.

## Owner
Founder. No delegation.

## Inputs
- All command centers.
- Calendar audit.
- Decision log.
- A3 entries.
- Health and incident logs.

## Outputs
- Scorecard file under `evidence/founder/weekly/<YYYY-Www>.md`.
- Read at Monday review.

## The Seven Sections

### 1. Revenue
- Cash collected this week.
- New SOW signed (count, value).
- MRR change.
- Notes: anything material.

### 2. Sales
- Qualified opportunities created.
- Meetings held.
- Win, loss, defer.
- Cycle time on closed deals.

### 3. Delivery
- Active sprints (count).
- On-time milestone rate.
- Rework rate.
- Client health scores: count by band.
- At-risk count and actions taken.

### 4. Trust
- Incidents opened, closed.
- Banned-practice incidents (target 0).
- PDPL findings (target 0).
- Provenance log spot-check (done? yes/no).

### 5. Learning
- A3 opened, closed.
- Top 3 lessons this week (1 sentence each).
- Decisions taken back from delegates.
- Books / papers / interviews of substance (with source).

### 6. Founder
- Hours by category (strategy / sales / delivery / ops / personal).
- Variance vs plan.
- Calendar discipline score (self, 0-5).
- Sleep / health note (one line).

### 7. Product
- Productization candidate movements (promotions / kills).
- Build / Defer / Kill decisions this week.
- Engineering health flag (green / yellow / red).

## Rules
1. Filed every Friday before founder closes the week; no skipping.
2. Numbers labelled estimated or verified.
3. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" at the bottom.
4. No marketing language. No "great week". State facts.
5. Honesty over comfort; if a section is bad, it is bad in writing.
6. PII never in this file; clients referenced by code.
7. Signed by the founder (typed name + date).

## Metrics
- Weekly scorecard on-time rate (target 100%).
- Section completion (no skipped sections).
- Variance vs plan visibility.
- Year-over-year scorecard quality (qualitative founder review at annual close).

## Cadence
- Weekly Friday.

## Evidence
- Filed weekly file.

## Verifier
Founder (self). Quarterly cross-check by accountant on revenue section.

## Runtime Command
`make ceo-scorecard WEEK=<YYYY-Www>` — opens template, pulls dashboard data, refuses to mark filed without all sections.

## Arabic Summary — ملخص عربي
بطاقة أداء أسبوعية ذاتية للمؤسس في سبعة أقسام: إيرادات، مبيعات، تسليم، ثقة، تعلم، مؤسس، منتج. صدق قبل الراحة. تُملأ كل جمعة قبل إغلاق الأسبوع. القيم التقديرية ليست مُتحقَّقة.
