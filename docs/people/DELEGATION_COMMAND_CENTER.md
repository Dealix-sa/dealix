# Delegation Command Center — مركز قيادة التفويض

## Purpose
A single live view of what is delegated, to whom, with what review cadence, and what cannot be delegated. Prevents two failure modes: founder bottleneck and silent over-delegation of strategic decisions.

## Owner
Founder. Reviewed weekly.

## Inputs
- `docs/people/DELEGATION_RULES.md` (what cannot be delegated).
- `docs/people/ROLE_MAP.md` (current org).
- Scorecards for each delegate role.
- Active SOWs with contractors and partners.

## Outputs
- Live table: task / process, delegate, review cadence, last review date, status.
- Weekly attention list.
- Quarterly delegation audit.

## Dashboard Panels
1. **Delegated tasks** — task, owner (delegate), founder role (review).
2. **Review cadence** — daily / weekly / monthly per task.
3. **Last review date** — overdue flagged red.
4. **Quality signals** — pulled from delegate's scorecard.
5. **Non-delegable list** — visible always (see `docs/people/DELEGATION_RULES.md`).
6. **Re-claim queue** — tasks where founder needs to take back temporarily.

## Rules
1. No task is delegated without a documented SOP and an evidence-attached scorecard.
2. Items in `docs/people/DELEGATION_RULES.md` are never delegated; visible at top of dashboard.
3. Review cadence is set at delegation time and held; missed reviews flagged.
4. A delegate's quality drop ≥ 2 on their scorecard for 2 consecutive periods triggers re-claim.
5. No silent re-delegation; every delegation chain is documented.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to estimated time savings.

## Metrics
- Delegated task count.
- Review on-time rate (target ≥ 90%).
- Re-claim count per quarter (signals weak delegate or weak SOP).
- Founder hours reclaimed (estimated, weekly).

## Cadence
- Daily: glance.
- Weekly: 20-minute review.
- Quarterly: delegation audit (what to delegate next, what to take back).

## Evidence
- `evidence/delegation/<YYYY-Www>.md` snapshot.

## Verifier
Founder.

## Runtime Command
`make delegation-status` — prints the table, lists overdue reviews and at-risk delegations.

## Arabic Summary — ملخص عربي
هذه اللوحة تعرض كل ما هو مُفوَّض، لمن، وبأي إيقاع مراجعة. القائمة غير القابلة للتفويض ظاهرة دائمًا في الأعلى. لا تفويض دون إجراء مُوثَّق ومؤشر أداء. القيم التقديرية ليست مُتحقَّقة.
