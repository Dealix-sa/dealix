# Hermes Governance Policy

Hermes is a governed operating layer for Dealix. It is designed for continuous monitoring, planning, review, and approval-ready recommendations.

## Operating modes

| Mode | Purpose |
| --- | --- |
| `dry_run` | Default mode. Agents inspect, draft, summarize, and log. |
| `review` | Founder reviews recommendations and decides next steps. |
| `approved_task` | A previously reviewed task is documented for manual execution. |
| `manual_only` | Agents may only explain and escalate. |

## Core rules

1. Keep real provider keys and production secrets outside the repository.
2. Keep live customer, finance, publishing, and infrastructure changes behind founder review.
3. Every agent run should create a reviewable artifact.
4. Every recommendation should include owner, reason, expected benefit, risk, and next step.
5. Agents should escalate when confidence is low or data is stale.

## Risk levels

| Level | Examples | Required handling |
| --- | --- | --- |
| Low | summaries, drafts, read-only checks | log artifact |
| Medium | client-facing drafts, proposed pricing notes | founder review |
| High | operational changes, customer-facing actions | explicit approval path |
| Critical | irreversible or regulated actions | manual-only handling |

## Review record

```json
{
  "review_id": "hermes-YYYYMMDD-HHMMSS",
  "agent_id": "agent_name",
  "risk": "low|medium|high|critical",
  "recommendation": "short summary",
  "target": "system or workflow",
  "reason": "why it matters",
  "expected_benefit": "business or reliability benefit",
  "next_step": "manual action or review item",
  "created_at": "ISO-8601 timestamp"
}
```

## Recommended initial cadence

- Hourly: revenue opportunity scan in dry-run mode.
- Every 6 hours: operations and readiness review.
- Daily 08:00 Asia/Riyadh: founder digest input.
- Daily 17:00 Asia/Riyadh: market and finance snapshot.
- On PR: product quality and security review.

## Framework fit

- LiteLLM: provider routing and fallback.
- LangGraph: persisted flows and human review checkpoints.
- OpenAI Agents SDK: guardrails, handoffs, and tracing.
- CrewAI: role-based crew orchestration for simpler agent teams.

Hermes should adopt runtime libraries incrementally. The first safe layer is manifest, governance, schedules, runbooks, and dry-run artifact generation.
