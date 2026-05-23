# Founder Console — Trust Gate

The Founder Console is the surface through which the founder approves or rejects every protected decision. It is the human-side of the Trust Plane.

**Source of truth:** `api/routers/internal/founder_console.py` + UI at `apps/web/lib/dealix-runtime.ts`
**Owner:** Founder + Engineering Lead
**Trust gate:** A2 — the Console is itself a protected surface; auth required.

## Protected decisions

The Console surfaces these decision classes:

| Class | Examples |
|-------|---------|
| Proof publishing | Case study, sector report, testimonial |
| Pricing change | Reference price, custom price, exception |
| Contract execution | Proposal send, contract sign |
| Refund | Full or partial refund |
| Payment terms | Extension, deferral |
| Data export | Export of any client data |
| Agent activation / retirement | Agent lifecycle changes |
| Policy change | Policy as Code edits |
| External send | Any email or DM to a non-customer |

## Decision card

Each pending decision is shown as a card with:

- Title and decision class.
- Requester (agent id or human).
- Linked artifact (proposal, draft, policy diff).
- Rationale provided by the requester.
- Risk summary computed by Trust Guardian.
- Approval options: `approve`, `revise`, `deny`, `escalate`.
- Comment field (required on `deny` and `revise`).

Approval and denial are logged in `$PRIVATE_OPS/founder_decisions.csv` with `decided_at`, `decision`, `rationale`.

## Authentication

The Console is gated by `DEALIX_INTERNAL_TOKEN` (see `docs/security/INTERNAL_API_AUTH_GATE.md`) and by founder identity. A non-founder cannot approve.

## OWASP LLM Top 10 posture

- **LLM08 Excessive agency.** The Console is the human check on agent agency. No agent can self-approve.
- **LLM09 Overreliance.** The Console always shows the agent's rationale plus the source artifact, so the founder can decide on first-principles rather than trusting the agent's summary.
- **LLM01 Prompt injection.** Decision cards render content as content, not as instructions to the founder.

## Cadence

- **Real-time.** A2 decisions are notified immediately.
- **End-of-day.** Pending decision summary in CEO Copilot daily briefing (`docs/ai/CEO_COPILOT_SYSTEM.md`).
- **Weekly.** Decision distribution review (approvals, denials, revisions, escalations).

## Failure modes

- **Approval queue starvation:** decisions wait > 48 hours. Detection: queue audit. Recovery: founder is paged; if unavailable, decisions deny by default; never auto-approve.
- **Stale token:** Console auth token expires; decisions cannot be approved. Detection: auth log. Recovery: token rotation per `docs/security/KEY_ROTATION.md`.
- **Phantom decision:** a decision card is shown for an action already completed. Detection: state reconciliation. Recovery: dismiss with audit.

## Recovery path

If the Console is unavailable, all A2 actions deny by default. The founder receives a backup notification channel and may approve through a written, signed message stored in audit.

## Metrics

- Pending decisions count (current).
- Median approval cycle time.
- Approval / deny / revise / escalate distribution.
- Stale-decision incidents per quarter (target: 0).

## Disclaimer

The Console enforces approval; it does not guarantee correct judgement. Founder judgement remains the last layer. Estimated value is not Verified value.
