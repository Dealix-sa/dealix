# Worker Orchestrator v1

The Worker Orchestrator is the runtime that dispatches agent jobs, enforces the Trust Plane, and reports execution results. It is the single chokepoint through which every agent action flows.

**Source of truth:** code at `apps/web/lib/dealix-runtime.ts` + worker services + `policies/dealix_control_policy.yaml`
**Owner:** Engineering Lead
**Trust gate:** A2 — orchestrator behavior changes require founder approval.

## Dispatch pipeline

1. **Intake.** A job request arrives with: agent id, action, inputs, approval class, requested write targets.
2. **Trust check.** Trust Guardian (`docs/ai/TRUST_GUARDIAN_AGENT.md`) validates against the registry and policy.
3. **Cost check.** Cost Guard (`docs/06_llm_gateway/COST_GUARD.md`) validates against guardrails.
4. **Eval check.** The orchestrator confirms the agent's required suites are passing.
5. **Run.** The agent executes. Inputs and outputs are streamed to the audit log.
6. **Validate.** Output is validated against the schema (`docs/06_llm_gateway/SCHEMA_VALIDATION.md`).
7. **Persist.** Approved writes are committed to the allowed targets.
8. **Notify.** If an external surface or A2 decision is involved, the Founder Console is notified.

A failure at any step is a hard stop with an audit row.

## Concurrency

The orchestrator runs work in tenant-scoped queues. A noisy tenant cannot starve another tenant. Per-agent concurrency limits prevent runaway loops.

## Retries

| Failure | Retry strategy |
|---------|----------------|
| Inference outage | Exponential backoff, 3 attempts, then fail closed |
| Schema validation failure | No retry; the agent must produce a new output |
| Policy denial | No retry; never |
| Cost-guard denial | No retry until the next guardrail window |
| Network blip on persist | Retry with idempotency key |

Retries are bounded; the orchestrator does not loop on policy denials.

## Idempotency

Every job carries an idempotency key. Re-dispatch with the same key returns the prior result rather than re-running. This protects against double-charge, double-send, double-log.

## OWASP LLM Top 10 posture

- **LLM01 Prompt injection.** Inputs are typed; instructions are not user-supplied content.
- **LLM02 Insecure output handling.** Outputs are schema-validated before persist.
- **LLM04 Denial of service.** Concurrency caps and cost guard prevent runaway.
- **LLM08 Excessive agency.** Tool list and write allowlist enforced.
- **LLM05 Supply chain.** Pinned model and tool implementations; tool registry is signed.

## Failure modes

- **Skipped trust check:** a code path bypasses Trust Guardian. Detection: code review + red team. Recovery: code fix; runtime audit replay.
- **Schema-validation skip:** an output is persisted without validation. Detection: monthly audit. Recovery: code fix; affected rows quarantined.
- **Queue starvation:** a tenant's queue stalls. Detection: queue monitor. Recovery: scale workers; investigate.

## Recovery path

If orchestrator integrity is in doubt, the runtime fails closed: no new dispatches accepted. Manual operation continues until the orchestrator is recertified.

## Metrics

- Jobs dispatched per minute.
- Trust-deny rate.
- Cost-deny rate.
- Schema-validation pass rate.
- p99 dispatch latency.

## Disclaimer

The orchestrator is engineered, not infallible. Dealix does not guarantee zero job failures. Estimated value is not Verified value.
