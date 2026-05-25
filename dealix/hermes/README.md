# Hermes — Dealix's Production + Growth + Governance Max layer

> Dealix is a Sovereign Value Control Plane.
> It turns market signals, customer requests, partner opportunities,
> and operational events into governed execution, measurable outcomes,
> reusable assets, and verified revenue.
>
> Core Loop:
> Signal → Opportunity → Decision → Execution → Trust → Outcome → Asset → Scale/Kill

Hermes is the production layer that makes Dealix more than a repo:

- **Control Plane** — runtime gates (sovereignty, trust, data, tool,
  approval, audit, outcome, kill switch).
- **Identity** — agent, actor, workspace identities, capability scopes,
  revocation, session policies.
- **Data** — classification, tenant isolation, context packets,
  redaction, retention.
- **Growth** — verified revenue loop, channel / message / campaign /
  offer quality scoring, GEO (AI search visibility), attribution.
- **Money** — revenue quality, cost intelligence, margin analysis,
  pricing engine.
- **Products** — productized packages and the delivery playbooks that
  ship them.
- **Customer** — customer value report generator.
- **Partners** — partner tiers, approved claims, revenue share,
  enablement, performance review.
- **Assets** — Revenue Asset Store with quality grading, reuse,
  commercialization, and asset → product flow.
- **Graphs** — opportunity, outcome, revenue, partner, asset, risk,
  sector graphs.
- **Workflows** — declarative YAML workflow configs.
- **API Platform / Marketplace** — readiness gates for any public
  surface.
- **Automation** — Automation Readiness Score that decides draft-only
  / approval-gated / low-risk-autonomous / never.
- **Observability** — metrics + alert rules.

## Rule of the platform

Any request that does not pass through
`hermes.control_plane.runtime.ControlPlaneRuntime.dispatch` is
considered illegitimate and MUST be rejected upstream.
