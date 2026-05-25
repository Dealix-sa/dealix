# Client Success Command Center — مركز قيادة نجاح العملاء

## Purpose
Single dashboard for the health of every active client engagement. Surfaces at-risk accounts before churn, flags upsell readiness only after value is proven, and orders the founder's attention across the book.

## Owner
Founder. Maintained jointly by analyst and AE (when hired).

## Inputs
- Active engagements list from `docs/03_commercial_mvp/`.
- Health scores from `docs/client_success/CLIENT_HEALTH_SCORE.md`.
- Tiering from `docs/client_success/CLIENT_TIERING.md`.
- Feedback log from `docs/client_success/FEEDBACK_LOOP.md`.
- Weekly reports from `docs/client_success/WEEKLY_REPORT_TEMPLATE.md`.

## Outputs
- Live table: client, tier, health score, next milestone, last contact, at-risk flag.
- Weekly attention list (top 3 accounts requiring founder action).
- Monthly retention forecast.

## Dashboard Panels
1. **Active engagements** — name (or code), tier, days into engagement.
2. **Health score** — 0-100, color-coded.
3. **Last touchpoint** — date, type, outcome.
4. **Next milestone** — date, owner.
5. **At-risk flag** — explicit Yes/No with reason.
6. **Upsell readiness** — Yes only if value proven (see `docs/client_success/UPSELL_PLAYBOOK.md`).
7. **Renewal status** — days to renewal, conversation stage.
8. **Open feedback items** — count, age.

## Rules
1. No upsell flagged Yes without verified outcome evidence.
2. No client name in external content without written approval.
3. At-risk flag triggers retention playbook within 48 hours.
4. The founder reviews this dashboard weekly; no skipping.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to any estimated impact figures.

## Metrics
- Active engagement count.
- Median health score.
- At-risk count.
- Renewal rate (rolling 90 days).
- Net revenue retention (when 12+ months of data exist).

## Cadence
- Daily glance.
- Weekly review (30 min).
- Monthly retention deep-dive.

## Evidence
- Weekly snapshot under `evidence/client-success/<YYYY-Www>.md`.

## Verifier
Founder.

## Runtime Command
`make client-status` — prints the table, sorts by at-risk first, lists top 3 attention items.

## Arabic Summary — ملخص عربي
لوحة قيادة نجاح العملاء تعرض كل العلاقات النشطة: الصحة، الفئة، المعلَم القادم، إشارة الخطر. لا توصية بزيادة الخدمة دون قيمة مُثبتة. القيم التقديرية ليست مُتحقَّقة.
