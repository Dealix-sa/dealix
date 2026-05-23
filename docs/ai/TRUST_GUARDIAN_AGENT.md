# Trust Guardian Agent

> The agent that reviews every AI output, queue write, and external-impact
> request before it reaches the founder's approval queue or the world.

## Purpose

Prevent Dealix from doing avoidable damage to itself: leaking data,
overclaiming, sending to suppressed contacts, accepting prompt injection
from a prospect's reply, or attempting an A3 action automatically.

This is the **most important AI system after CEO Copilot**. Where CEO
Copilot tells the founder what to do, Trust Guardian tells every
other system what *not* to do.

## Position in the Operating Layer

Trust Guardian sits between every AI agent (and every frontend action)
and the approval queue / external-action worker. Policy-as-Code runs
the deterministic rules; Trust Guardian runs the judgment rules that a
YAML file cannot easily express.

```
Agent / Frontend / Approval Request
       │
       ▼
Policy-as-Code Evaluator      ← deterministic, fast, deny by default
       │
       ▼  (allow / require_review)
Trust Guardian Agent          ← judgment + content safety
       │
       ▼  (allow / deny / edit / escalate)
Approval Queue / Audit Log / Worker
```

## What It Checks

| Check | What it looks for |
|-------|-------------------|
| Prompt injection risk | Untrusted text (prospect replies, scraped pages) attempting to override system instructions, exfiltrate data, or invoke tools |
| Sensitive data leakage | PII, secrets, internal-only metrics, or unredacted account data in agent output |
| Overclaim | Revenue guarantees, "ensure X% ROI", fabricated metrics, fake client logos |
| Unsupported claim | Any statement that cannot be linked to evidence in the knowledge base |
| Suppression violation | Recipient is on DNC, PDPL opt-out, bounce, or manual block list |
| Missing evidence | Outreach / proposal / proof without at least one verifiable source |
| A3 action attempt | Any path trying to auto-execute an A3 action |
| Pricing / contract / payment commitment | Any draft that commits Dealix outside the approved matrix |
| Public proof without approval | Case study, social post, or testimonial without explicit signoff |
| Tool misuse | Agent requesting tools outside its declared permission level |

## Input Contract

```json
{
  "subject_type": "agent_output | queue_write | approval_request | external_action",
  "subject_id": "string",
  "actor": "agent_id | user_id | worker_id",
  "approval_class": "A1 | A2 | A3",
  "payload": { "...": "the thing being reviewed" },
  "context": {
    "recipient": "optional contact id",
    "suppression_state": "ok | blocked | unknown",
    "evidence_refs": ["..."],
    "policy_results": [ { "rule": "...", "result": "..." } ]
  }
}
```

## Output Contract

```json
{
  "decision": "allow | needs_edit | deny | escalate",
  "reasons": [
    {"code": "string", "severity": "low|medium|high|critical", "detail": "string"}
  ],
  "required_edits": ["string"],
  "audit_event_id": "string",
  "guardian_version": "string"
}
```

- `allow` → proceed to approval queue (A2) or audit log (A1).
- `needs_edit` → return to author agent with specific edits required.
- `deny` → block, log, never auto-retry.
- `escalate` → route to founder with the reason codes attached.

## Rule

> No A2 or A3 action proceeds without Policy-as-Code **and** Trust
> Guardian review.

A1 actions skip Trust Guardian only if they are pure read-only and
internally scoped. The default for any new action class is **review
required**.

## Threat Model

We treat the following as untrusted:

- Any prospect-supplied content (replies, forms, uploads).
- Any scraped or fetched web content.
- Any LLM-generated content (including from our own agents) before
  guardian review.
- Any contractor- or partner-supplied content.

This aligns with the OWASP LLM Top 10 view that prompt injection is the
primary risk surface for LLM applications, and that every external
input is untrusted until evaluated.

## Failure Modes

| Mode | Detection | Response |
|------|-----------|----------|
| Guardian unavailable | Health check | Trust Layer fails closed — no A2/A3 proceeds |
| Guardian uncertain | Confidence < threshold | Decision = `escalate`, never `allow` |
| Guardian disagrees with Policy-as-Code | Comparison check | Stricter wins; both logged |
| Repeated denies on same author | Audit aggregation | Auto-throttle that agent |
| Adversarial injection detected | Pattern + classifier | Deny + log + alert |

## Implementation Notes

- Trust Guardian is itself an AI agent. It is bound by the same
  governance rules: scope, output contract, evals, red-team suite,
  kill switch.
- It runs on a separate model and a separate prompt path from the
  authoring agents, to reduce shared-failure risk.
- It must pass its own red-team suite (see
  [`EVAL_RED_TEAM_SYSTEM`](EVAL_RED_TEAM_SYSTEM.md)) before promotion.
- Decisions are append-only in `audit_events` with
  `event_type = trust_guardian.decision`.

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`POLICY_AS_CODE_SYSTEM`](../trust/POLICY_AS_CODE_SYSTEM.md)
- [`AI_NATIVE_COMPANY_ARCHITECTURE`](../architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md)
- [`EVAL_RED_TEAM_SYSTEM`](EVAL_RED_TEAM_SYSTEM.md)
