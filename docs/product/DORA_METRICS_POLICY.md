# DORA Metrics Policy — سياسة مقاييس DORA

## Purpose
Define when and how Dealix tracks the four DORA metrics (deployment frequency, lead time for changes, change failure rate, mean time to recovery). Pre-product, these are aspirational; post-SaaS-gate, they are mandatory.

## Owner
Founder pre-engineering hire. CTO or lead engineer once hired.

## Inputs
- Git commit and deploy logs (when CI is set up).
- Incident log from `docs/14_trust_os/`.
- Workflow run logs from `docs/product/WORKFLOW_REGISTRY.md`.

## Outputs
- Monthly DORA scorecard once tracking is active.
- Engineering health review entry in `docs/product/ENGINEERING_HEALTH_REVIEW.md`.

## The Four Metrics
| Metric | Definition | Target Band (post-SaaS) |
|---|---|---|
| Deployment frequency | Production releases per week | ≥ 1 per week, ≤ 5 per day |
| Lead time for changes | Hours from commit to production | ≤ 48h |
| Change failure rate | % of deploys causing incident / rollback | ≤ 15% |
| MTTR | Median minutes to recover from incident | ≤ 60 min |

## Tracking Stage Rules
1. **Pre-Template stage**: no DORA tracking; effort goes to delivery, not metrics theatre.
2. **Template stage**: track deployment frequency only (lightweight).
3. **Automation stage**: track all four, manual collection allowed.
4. **SaaS Candidate / SaaS**: full automated DORA pipeline mandatory.

## Rules
1. No DORA dashboard built before automation stage; it is anti-discipline.
2. No targets set without 4 weeks of baseline data.
3. Incidents that touch client data are tagged separately and reviewed in `docs/14_trust_os/`.
4. Estimated improvement claims are labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
5. No marketing claim about "fast iteration" without DORA evidence.

## Metrics
- Deployment frequency (weekly).
- Lead time median + p90.
- Change failure rate (monthly).
- MTTR median + p90.

## Cadence
- Pre-SaaS: ad-hoc.
- Post-SaaS: weekly metric refresh, monthly review.

## Evidence
- `evidence/engineering/dora/<month>.md` with raw counts.
- Incident references in `docs/14_trust_os/`.

## Verifier
Lead engineer (when hired). Founder pre-hire.

## Runtime Command
`make dora-report MONTH=<YYYY-MM>` — collects logs, prints scorecard, flags out-of-band metrics.

## Arabic Summary — ملخص عربي
لا تُتبَّع مقاييس DORA قبل مرحلة الأتمتة. عند الوصول لمرحلة منتج SaaS تصبح إلزامية. لا ندَّعي سرعة التكرار دون أدلة. القيم التقديرية ليست مُتحقَّقة.
