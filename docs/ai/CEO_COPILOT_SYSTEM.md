# CEO Copilot System

> Recommends the single highest-leverage CEO action each day. Never
> executes it.

## Purpose

Give the founder one screen, one paragraph, one decision per morning.
No dashboards. No "ten metrics to check". One action, with evidence
and risk attached, that the founder either approves or overrides.

## Position in the Operating Layer

CEO Copilot lives **above** the Revenue Runtime and Worker layers, and
**below** the Founder Control Layer. It reads from runtime state and
writes only to `/ceo` and the audit log.

```
Workers + Sales OS + Trust Plane + Finance
    │
    ▼
CEO Copilot  ─── reads state, produces recommendation
    │
    ▼
/ceo surface ─── founder sees + decides
    │
    ▼
Audit log    ─── what was shown, what was decided, why
```

## Inputs

| Input | Source | Why it matters |
|-------|--------|----------------|
| Sales funnel | `lead_intelligence`, `outreach_queue`, `conversation_log`, `proposal_queue` | Where is the bottleneck this week? |
| Approval queue | `approval_queue`, `approval_decisions` | What is waiting on the founder? |
| Worker health | `worker_state` | Is the machine actually running? |
| Trust flags | `trust_flags` | Is anything blocking external action? |
| Finance summary | `payment_capture_queue`, retainer ledger | Where is cash, today and this month? |
| Payment capture | `payment_capture_queue` | Which proposals are stuck on payment? |
| Delivery queue | delivery ledger | Which paid customers are unserved? |

## Output Contract

The CEO Copilot must return a single JSON object with this shape:

```json
{
  "summary": "string (≤ 280 chars, bilingual ok)",
  "top_action": "string (imperative, ≤ 120 chars)",
  "why_now": "string (≤ 280 chars)",
  "evidence": [
    {"label": "string", "value": "string", "source": "table/column"}
  ],
  "risk": "Low | Medium | High | Critical",
  "approval_class": "A1 | A2 | A3",
  "next_action": "string (what the founder should click)",
  "generated_at": "ISO-8601 timestamp",
  "model": "string (model id used)",
  "policy_version": "string"
}
```

Any missing field → output is rejected and the founder sees the previous
day's recommendation with a "stale" marker. We never invent fields.

## What the CEO Copilot Never Does

- Send external messages (email, WhatsApp, LinkedIn, SMS).
- Change pricing, contracts, or scope.
- Approve proposals or invoices.
- Publish proof, case studies, or social posts.
- Modify suppression or DNC lists.
- Trigger A3 actions, ever.

## Approval Class Mapping

- **A1 (auto-eligible):** read-only summary, internal queue
  reordering, generating internal drafts. CEO Copilot may surface
  these as "already done".
- **A2 (founder-approved):** sending outreach, sending samples,
  sending proposals, capturing payment. CEO Copilot recommends; the
  founder clicks approve.
- **A3 (never automatic):** discounts beyond policy, contract
  signature, public proof publication, refunds, scope changes.
  CEO Copilot may *only* describe the situation; it must not
  recommend execution.

## Rule

> CEO Copilot recommends. Sami decides.

If the recommendation engine cannot run, the surface degrades to the
last successful recommendation with an explicit "stale" badge, plus a
manual-mode link. Never blank, never silent.

## Failure Modes

| Mode | Detection | Response |
|------|-----------|----------|
| Stale data | `generated_at` older than 24h | Show stale badge, dim recommendation |
| Missing input | Any required source returns null | Show "input missing" + which source |
| Policy version drift | `policy_version` ≠ current | Block render, alert founder |
| Output contract violation | JSON schema fails | Fall back to last good output |

## Implementation Notes

- The recommender is a deterministic ranker over current state plus an
  LLM-generated rationale. The ranker is the decision; the LLM only
  writes the human-readable `summary` and `why_now`.
- The LLM never sees raw PII. It receives a redacted snapshot.
- Every recommendation, including the inputs hash, is written to
  `audit_events` with `event_type = ceo_copilot.recommendation`.

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`TRUST_GUARDIAN_AGENT`](TRUST_GUARDIAN_AGENT.md)
- [`AI_NATIVE_COMPANY_ARCHITECTURE`](../architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md)
