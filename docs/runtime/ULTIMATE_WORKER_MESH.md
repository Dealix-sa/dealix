# Ultimate Worker Mesh

The Worker Mesh is the horizontally scaled set of worker processes that execute agent jobs dispatched by the Orchestrator. Each worker is isolated, observed, and replaceable.

**Source of truth:** worker services config + `docs/runtime/WORKER_ORCHESTRATOR_V1.md`
**Owner:** Engineering Lead
**Trust gate:** A2 — mesh topology and capacity changes require founder approval.

## Topology

| Tier | Purpose |
|------|---------|
| Edge | Receives external webhooks; validates signatures; enqueues |
| Dispatch | Orchestrator service; assigns jobs |
| Worker pool A | Read-only agents (Brand Guardian, Performance Analyst, CEO Copilot, Trust Guardian) |
| Worker pool B | Drafting agents (Content Strategist, Distribution Operator, Offer Architect, Growth Strategist) |
| Worker pool C | Higher-cost or higher-risk jobs (red-team runs, large eval suites) |

Pools are independently scalable. Pool C runs with stricter cost limits and dedicated audit.

## Isolation

- Each worker process runs one job at a time.
- No shared mutable state between jobs.
- Per-tenant secrets are loaded just-in-time and zeroed on job exit.
- Tool calls go through the LLM Gateway, not directly to providers.

## Observability

Every worker exports:

- Job id, agent id, tenant id.
- Start, end, duration.
- Cost in USD and SAR.
- Schema-validation result.
- Trust decision.
- Policy version.
- Eval certification version.

These feed `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`.

## Backpressure

When a pool's queue depth exceeds its threshold:

1. Dispatch slows new accepts.
2. Founder Copilot is notified.
3. If the pool affects external surfaces, founder is paged.
4. Manual fallback path is announced to the Customer Success team.

The mesh never silently drops jobs.

## OWASP / NIST posture

- **LLM04 Denial of service.** Backpressure protects shared infrastructure.
- **LLM06 Sensitive information disclosure.** Per-job isolation prevents tenant data crossover.
- **Manage.** Pool topology is documented, monitored, and reversible.

## Failure modes

- **Worker crash loop:** a job crashes its worker. Detection: crash monitor. Recovery: worker recycled; job retried within idempotency rules.
- **Pool exhaustion:** queue depth sustained above threshold. Detection: monitor. Recovery: scale; investigate root cause.
- **Cross-tenant leak:** secrets from one tenant visible to another. Detection: red team + audit. Recovery: incident response; founder notified.

## Recovery path

If mesh integrity is in doubt, the orchestrator fails closed. Workers are drained. Manual operation continues until mesh is recertified.

## Metrics

- Pool utilisation (p50, p99).
- Job crash rate.
- Backpressure events per quarter.
- Cross-tenant incidents (target: 0).

## Disclaimer

The mesh is engineered, not infallible. Dealix does not guarantee zero job failures. Estimated value is not Verified value.
