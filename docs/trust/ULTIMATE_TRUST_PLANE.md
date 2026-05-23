# Ultimate Trust Plane

The Trust Plane is the connected set of controls that ensure no Dealix action escapes founder intent. It spans agents, runtime, data, finance, and external surfaces.

**Source of truth:** this doc + `policies/dealix_control_policy.yaml`
**Owner:** Founder + Engineering Lead
**Trust gate:** A2 — Trust Plane structural changes require founder approval.

## Components

| Component | Responsibility |
|-----------|----------------|
| Policy as Code | Encodes founder intent | `docs/trust/POLICY_AS_CODE_V1.md` |
| Agent Registry | Enumerates agents and their bounds | `docs/ai/AGENT_REGISTRY_SYSTEM.md` |
| Trust Guardian | Per-action policy check | `docs/ai/TRUST_GUARDIAN_AGENT.md` |
| Eval and Red Team | Continuous assurance | `docs/ai/EVAL_RED_TEAM_SYSTEM.md` |
| Founder Console | Approval surface | `docs/trust/FOUNDER_CONSOLE_TRUST_GATE.md` |
| Audit log | Append-only event log | `$PRIVATE_OPS/audit_log.csv` |
| Kill switch | Per-agent halt | enforced at runtime |
| Data Trust | Provenance and access | `docs/trust/DATA_TRUST_ARCHITECTURE.md` |
| AI Control Plane | Inference governance | `docs/trust/AI_CONTROL_PLANE.md` |

## Layered defence

Trust is layered:

1. **Pre-dispatch.** Trust Guardian checks the proposed action.
2. **Dispatch.** Runtime checks again at execution.
3. **Post-action.** Audit log records what happened.
4. **Continuous.** Eval and red-team confirm registered behaviour.
5. **Periodic.** Founder reviews policy and exceptions.

A single layer failure does not constitute a Trust Plane failure as long as another layer catches the error.

## OWASP LLM Top 10 mapping

| Risk | Layer that addresses |
|------|---------------------|
| LLM01 Prompt injection | Agent prompt hardening + Trust Guardian + eval |
| LLM02 Insecure output handling | Output schema validation + restricted write targets |
| LLM03 Training data poisoning | Read-only sources + provenance |
| LLM04 Denial of service | Cost guardrails + rate limits (`docs/security/RATE_LIMITS.md`) |
| LLM05 Supply chain | Pinned model + tool allowlist |
| LLM06 Sensitive information disclosure | PII classification + access controls |
| LLM07 Insecure plugin design | No plugins; registered tools only |
| LLM08 Excessive agency | Approval class + kill switch + write allowlist |
| LLM09 Overreliance | Human-in-the-loop on all external action |
| LLM10 Model theft | Internal API auth + model identifiers not published |

## NIST AI RMF mapping

| Function | Implementation |
|----------|----------------|
| Govern | Policy as Code + founder approval gate |
| Map | Agent Registry + Trust Guardian |
| Measure | Eval + red team + audit |
| Manage | Kill switch + recovery paths + exceptions |

## Failure modes

- **Quiet bypass:** an action reaches external systems without going through any layer. Detection: external send vs internal audit reconciliation. Recovery: runtime fix; engagement notified; root cause filed.
- **Layered fatigue:** founder approvals become rubber stamps. Detection: approval-cycle-time review. Recovery: founder Console UX changes; tighter pre-screening.
- **Drift:** policy and reality diverge. Detection: quarterly policy review. Recovery: policy update or behaviour fix.

## Recovery path

If the Trust Plane integrity is in doubt, the founder freezes all external actions and runs a Trust Audit (see `docs/14_trust_os/`). Operations continue manually.

## Metrics

- Layered-defence catches per quarter (multiple layers catching the same action).
- Quiet-bypass incidents (target: 0).
- Founder approval cycle time (median minutes).
- Audit log completeness.

## Disclaimer

The Trust Plane reduces the probability of unintended action; it does not eliminate it. Estimated value is not Verified value.
