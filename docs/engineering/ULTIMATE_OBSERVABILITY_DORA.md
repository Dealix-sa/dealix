# Ultimate Observability and DORA

Observability is the discipline of being able to answer, in production, the question "what happened and why?". DORA metrics are the discipline of measuring whether the engineering system itself is healthy.

**Source of truth:** observability stack config + `$PRIVATE_OPS/dora_metrics.csv`
**Owner:** Engineering Lead
**Trust gate:** A1 — dashboard and alarm changes are reviewed before activation.

## Observability pillars

| Pillar | What it shows |
|--------|---------------|
| Logs | Discrete events with structured fields |
| Metrics | Time series of numeric quantities |
| Traces | End-to-end request paths across services |
| Audit | Append-only ledger of trust-gated events |

Every Dealix service emits to all four pillars with consistent labels: `tenant_id`, `agent_id`, `job_id`, `policy_version`, `eval_version`.

## DORA metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Deployment frequency | Production deploys per week | Multiple per week |
| Lead time for changes | Median time from commit to production | < 48 hours |
| Change-failure rate | Deploys requiring rollback or hotfix | < 15% |
| Time to restore service | Median outage duration | < 1 hour |

DORA metrics are tracked in `$PRIVATE_OPS/dora_metrics.csv` and reviewed monthly.

## Alarms

Alarms are categorised:

| Category | Routing |
|----------|---------|
| P0 (Trust Plane integrity) | Founder + Engineering Lead immediate |
| P1 (Customer impact) | Engineering Lead immediate, founder summary |
| P2 (Internal impact) | Engineering Lead next business hour |
| P3 (Trend / drift) | Weekly review |

Every alarm has a runbook in `docs/runtime/`. An alarm without a runbook cannot ship.

## Trace correlation

A single business action (e.g. a proposal send) carries a `trace_id` that links: founder approval, agent dispatch, tool calls, schema validation, persist write, external send. The trace is queryable end-to-end.

## OWASP / NIST posture

- **Measure.** Observability is how the NIST RMF "Measure" function is implemented.
- **Manage.** Alarms drive the "Manage" function.
- **LLM10 Model theft.** Inference-pattern observability detects exfiltration attempts (mass token reads, unusual prompt patterns).

## Failure modes

- **Alarm fatigue:** too many low-value alarms. Detection: alarm-action rate. Recovery: tune or delete.
- **Silent failure:** a service is down but no alarm fired. Detection: synthetic check. Recovery: add alarm; root cause filed.
- **DORA drift:** a metric trends bad for two consecutive months. Detection: monthly review. Recovery: founder review; engineering plan.

## Recovery path

If observability is itself down, the founder treats the situation as P0 because the Trust Plane cannot be verified without observability. New external actions deny by default until restored.

## Metrics

- Alarm count by category per week.
- P0 / P1 alarm count (target: low).
- DORA metrics current vs target.
- Trace coverage (jobs with full trace) (target: 100%).

## Disclaimer

Observability reduces incident time, it does not prevent incidents. Dealix does not guarantee zero downtime. Estimated value is not Verified value.
