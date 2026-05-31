# Hermes Artifact Schemas

Hermes artifacts are review-first records. They should be simple, durable, and easy to inspect with standard tools.

## Review record JSONL

Path suggestion:

```text
data/hermes/review_records.jsonl
```

Each line is one JSON object.

```json
{
  "review_id": "hermes-20260527T080000Z-revenue_scout",
  "agent_id": "revenue_scout",
  "run_id": "dry-run-20260527T080000Z",
  "created_at": "2026-05-27T08:00:00Z",
  "mode": "dry_run",
  "risk_level": "low",
  "input_scope": "manifest_bootstrap",
  "finding": "Revenue Scout is registered for review-only operation.",
  "confidence": "high",
  "recommended_next_step": "Connect a read-only lead source in a future PR.",
  "evidence": ["hermes/agents/manifest.json"],
  "owner": "founder",
  "status": "new"
}
```

### Required fields

| Field | Type | Notes |
| --- | --- | --- |
| `review_id` | string | Unique review record id. |
| `agent_id` | string | Must match an agent in `hermes/agents/manifest.json`. |
| `run_id` | string | Groups records from one run. |
| `created_at` | string | ISO-8601 timestamp. |
| `mode` | string | Usually `dry_run` at this stage. |
| `risk_level` | string | `low`, `medium`, `high`, or `critical`. |
| `finding` | string | Short human-readable finding. |
| `confidence` | string | `low`, `medium`, or `high`. |
| `recommended_next_step` | string | Founder-readable next step. |
| `evidence` | array | File paths, URLs, or source names. |
| `owner` | string | Usually `founder`. |
| `status` | string | `new`, `reviewed`, `accepted`, `rejected`, or `deferred`. |

## Founder digest Markdown

Path suggestion:

```text
data/hermes/founder_digest.md
```

Required sections:

```markdown
# Hermes Founder Digest

Generated: ...
Mode: dry_run
Agents: ...

## Registered agents

## Recommended next steps
```

Future digest versions should add:

- Revenue opportunities.
- Operational risks.
- Market notes.
- Finance and margin notes.
- Product QA notes.
- Items requiring founder decision.

## Weekly strategy Markdown

Path suggestion:

```text
data/hermes/weekly_strategy.md
```

Recommended sections:

- Top three opportunities.
- Top three blockers.
- Suggested PR queue.
- Founder decisions needed.
- Deferred items.

## Cockpit export JSON

Future path suggestion:

```text
landing/assets/data/hermes-status.json
```

Suggested shape:

```json
{
  "generated_at": "2026-05-27T08:00:00Z",
  "mode": "dry_run",
  "agents_total": 8,
  "open_reviews": 4,
  "high_risk_reviews": 0,
  "next_recommended_pr": "Add read-only GitHub PR review connector",
  "last_digest_path": "data/hermes/founder_digest.md"
}
```

Do not include private customer data in static cockpit exports.
