# Weekly Client Report — Template — تقرير أسبوعي للعميل

## Purpose
Standard weekly report for every retainer client. Predictable, evidence-attached, bilingual. The weekly report is the single most important retention lever; missing one twice in a quarter triggers the retention playbook.

## Owner
Delivery analyst drafts. Founder reviews and signs for first 10 clients; analyst sends after that.

## Inputs
- Work log from the past week.
- Output artifacts shipped.
- Issues raised by client.
- Time spent vs SOW allowance.
- Upcoming milestones.

## Outputs
- Sent to client by agreed channel each week.
- Filed under `evidence/client-reports/<client_id>/<YYYY-Www>.md`.

## Template Structure (Bilingual)
### 1. Header
- Client (code), week, sprint id, primary contact.

### 2. Executive Summary (≤ 80 words, AR + EN)
- What was shipped this week, in plain language.

### 3. Shipped This Week
- Bullet list of artifacts with links.

### 4. Outcomes vs Goals
- Table: goal, expected, this-week actual, delta.
- Numbers labelled estimated or verified.

### 5. Risks and Blockers
- What slowed us, what we need from the client.

### 6. Next Week Plan
- Bullet list with owners and dates.

### 7. Time and Scope
- Hours used this week vs SOW allowance.

### 8. Open Decisions for Client
- Explicit list with deadlines.

### 9. Disclosure
- "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"

## Rules
1. Sent every week on the agreed day; no skipping.
2. No marketing language. No "we're crushing it".
3. Numbers carry the verified vs estimated label.
4. Open decisions list cannot be empty if any exist; explicit "none" is allowed.
5. PII removed from any data shown.
6. Bilingual structure mirrored, same length and headings.
7. Client name appears on the report; external sharing requires written approval.

## Metrics
- Weekly report on-time rate (target 100%).
- Average length (target 400-700 words).
- Client open rate / acknowledgment (manual).
- Risks raised early vs late.

## Cadence
- Weekly per active retainer client.

## Evidence
- Filed report markdown + delivery artifacts.

## Verifier
Founder for first 10; thereafter delivery analyst with weekly spot-check.

## Runtime Command
`make weekly-report CLIENT=<id> WEEK=<YYYY-Www>` — opens template, pre-fills from work log, refuses to mark sent without all sections.

## Arabic Summary — ملخص عربي
تقرير أسبوعي قياسي لكل عميل اتفاقية مستمرة. ثنائي اللغة، مُسنَد بأدلة، بدون مبالغة. الإغفال مرتين في الربع يستدعي خطة الاحتفاظ. القيم التقديرية ليست مُتحقَّقة.
