# Dealix AI System Inventory

The list of every AI / autonomous system Dealix runs. This file is the
human-readable mirror of `registries/agent_registry.yaml`. They must
agree.

## Purpose

Make every AI system Dealix runs visible to a human at a glance, with
the controls that govern it.

## Owner

Founder. Re-audited monthly.

## Cadence

- Whenever an agent is added or retired.
- Monthly audit during the AI governance review.

## Source of Truth

This file mirrors `registries/agent_registry.yaml`. If they disagree,
the registry is authoritative for execution and this file is wrong.

## Required Per Entry

- `owner`
- `purpose`
- `risk_class` (A1 / A2 / A3)
- `kill_switch`
- `eval` suite (or "n/a" with reason)
- `audit` destination
- `allowed_write_targets`

## Inventory

### 1. ceo_daily_brief
- **Owner**: founder
- **Risk class**: A1
- **Purpose**: Build the founder's morning brief from internal KPIs.
- **Kill switch**: `DEALIX_CEO_BRIEF_DISABLED=1`
- **Eval suite**: n/a (read-only summarizer; no external send)
- **Audit destination**: `audit_events` table
- **Allowed write targets**: `data/founder_briefs/`

### 2. outreach_drafter
- **Owner**: founder
- **Risk class**: A2
- **Purpose**: Draft prospect outreach messages for human review.
- **Kill switch**: `DEALIX_OUTREACH_DRAFTER_DISABLED=1`
- **Eval suite**: `evals/outreach_quality_eval.yaml`
- **Audit destination**: `audit_events` table
- **Allowed write targets**: `data/outreach_drafts/`, approval queue

### 3. external_sender
- **Owner**: founder
- **Risk class**: A3
- **Purpose**: Send approved outreach via WhatsApp / Email **after** human approval.
- **Kill switch**: `WHATSAPP_ALLOW_LIVE_SEND=false`
- **Eval suite**: `evals/outreach_quality_eval.yaml`
- **Audit destination**: `audit_events` + `send_log`
- **Allowed write targets**: `audit_events`, `send_log`
- **Requires approval**: yes
- **Suppression check**: required before every send
- **Daily cap**: 50

### 4. lead_scorer
- **Owner**: founder
- **Risk class**: A1
- **Purpose**: Score inbound leads for the daily list.
- **Kill switch**: `DEALIX_LEAD_SCORER_DISABLED=1`
- **Eval suite**: `evals/lead_intelligence_eval.yaml`
- **Audit destination**: `audit_events` table
- **Allowed write targets**: `data/lead_scores/`

### 5. governance_auditor
- **Owner**: founder
- **Risk class**: A1
- **Purpose**: Run `make everything` on a schedule and write audit reports.
- **Kill switch**: `DEALIX_GOVERNANCE_AUDITOR_DISABLED=1`
- **Eval suite**: n/a (deterministic verifier)
- **Audit destination**: `audit_events` table + audit reports under `docs/ops/`
- **Allowed write targets**: the four reports under `docs/ops/`

## Trust Boundary

Anything not in this inventory is not allowed to run in production. CI
fails if `verify_agent_registry.py` finds an agent in the registry that
is not also documented here (manually) or vice versa.

## Failure Mode

- Agent added to registry but missing here → drift; surfaced by next
  monthly audit.
- Agent in this list but missing from registry → execution unsafe; CI
  blocks.

## Recovery Path

1. Pick the source of truth (registry).
2. Update this doc to match.
3. Commit; CI must pass.

## Verification

```bash
make ai-governance
```

## Next Action

If you added an agent today, also add a section above.
