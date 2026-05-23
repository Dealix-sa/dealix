# Engineering Health Review — مراجعة صحة الهندسة

## Purpose
Monthly review of engineering health: code quality, technical debt, DORA metrics, incident review, and contractor performance. Catches drift before it becomes a fire.

## Owner
Founder pre-engineering hire. Lead engineer once hired. Reviewed with founder always.

## Inputs
- DORA scorecard from `docs/product/DORA_METRICS_POLICY.md`.
- Incident log from `docs/14_trust_os/`.
- Code review queue and merge times.
- Test coverage and CI green-rate.
- Contractor delivery log.
- Architecture decisions made this month (link `docs/product/ARCHITECTURE.md`).

## Outputs
- Monthly review file under `evidence/engineering/health/<YYYY-MM>.md`.
- Top 3 actions for next month.
- Updated risk entry in `docs/investor/RISK_REGISTER.md` if needed.

## Review Sections
1. **DORA snapshot** — four metrics, trend vs last month.
2. **Incident review** — count, severity, root cause, prevention.
3. **Technical debt register** — top 5 items, age, planned action.
4. **Test and CI health** — coverage delta, flaky tests, green-rate.
5. **Contractor performance** — delivery vs SOW, quality, escalations.
6. **Architecture decisions** — what changed, why, link to ADR.
7. **Security review** — secrets rotation, access list audit, anomalies.
8. **Founder asks** — what the founder needs visibility on next month.

## Rules
1. No review skipped, even when busy; if skipped, A3 written in next review.
2. Every incident produces a 5-Why; no anonymous blame.
3. PII or client data never copied into review; reference incident IDs only.
4. Contractor performance discussed without naming clients.
5. Estimated impact figures labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Metrics
- DORA four.
- Incident count + median severity.
- Test coverage % and trend.
- Tech debt item age (median).
- Review on-time rate.

## Cadence
- Monthly, first business week.
- Quarterly deep review with founder + lead engineer.

## Evidence
- `evidence/engineering/health/<YYYY-MM>.md`.
- Signed by reviewer.

## Verifier
Founder counter-signs.

## Runtime Command
`make eng-health MONTH=<YYYY-MM>` — generates the template, pre-fills metrics from logs, refuses to close without all sections complete.

## Arabic Summary — ملخص عربي
مراجعة شهرية لصحة الهندسة: مقاييس DORA، الحوادث، الديون التقنية، أداء المتعاقدين. لا تُلغى ولا تُختصر. القيم التقديرية ليست مُتحقَّقة.
