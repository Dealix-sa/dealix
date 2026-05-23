# Distribution Operator Agent

The Distribution Operator agent prepares distribution artifacts (newsletter slot, founder post draft, sector excerpt) and queues them for human approval. It never publishes.

**Source of truth:** `registries/agent_registry.yaml` entry `distribution_operator`
**Owner:** Marketing Lead
**Trust gate:** A1 — queue management; A2 for any send-time decision.

## Spec

| Field | Value |
|-------|-------|
| `id` | `distribution_operator` |
| `name` | Distribution Operator |
| `purpose` | Prepare distribution drafts and queue for human approval |
| `approval_class_max` | A1 |
| `tools` | `read_calendar`, `read_brief`, `draft_artifact`, `write_queue_row` |
| `outputs` | `artifact_draft`, `queue_entry` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | marketing_lead |
| `allowed_write_targets` | `$PRIVATE_OPS/distribution_queue.csv`, `$PRIVATE_OPS/drafts/` |

## What it does

1. Reads the content calendar (`docs/marketing/CONTENT_CALENDAR_SYSTEM.md`) for the day's slots.
2. For each slot, reads the brief and source artifacts.
3. Drafts the artifact bilingually (EN + AR with parity).
4. Submits to Brand Guardian (`docs/ai/BRAND_GUARDIAN_AGENT.md`) for lint.
5. On lint pass, writes the draft to `$PRIVATE_OPS/drafts/` and queues a row in `distribution_queue.csv`.
6. Notifies the Marketing Lead.

The agent does not press send. The agent does not send DMs. The agent does not post on the founder's behalf.

## OWASP LLM Top 10 posture

- **Excessive agency (LLM08).** Tools list excludes any external-send capability.
- **Insecure output handling (LLM02).** Drafts are markdown only; no auto-publishing surface accepts them without human approval.
- **Sensitive information disclosure (LLM06).** Agent reads briefs and public source artifacts; it does not read client confidential data.

## Eval

The eval suite scores:

- Bilingual parity.
- Voice alignment against `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- Guarantee / hype absence.
- Disclosure presence where applicable.
- Citation density on quantitative claims.

## Failure modes

- **Auto-publish leak:** an integration accidentally enables auto-publish. Detection: policy engine + send-log audit. Recovery: blocked at policy; root cause filed.
- **Stale brief:** agent drafts from an archived brief. Detection: freshness check. Recovery: re-draft from current brief.
- **Voice drift:** drafts read generic. Detection: Brand Guardian + human review. Recovery: prompt re-anchored; eval suite extended.

## Recovery path

If draft quality falls below threshold, the agent is killed. Drafts revert to human authoring. Marketing Lead reports impact daily until the agent is restored.

## Metrics

- Drafts produced per week.
- Drafts approved without revision.
- Brand Guardian pass rate on first submission.
- Time from brief to queued draft (median minutes).

## Disclaimer

Distribution Operator is a drafting aid. Publication is always a human decision. Estimated value is not Verified value.
