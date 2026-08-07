# Agentic Commercial OS Integration Decision

## Executive verdict

Dealix already has multiple strong commercial layers in flight: launch stabilization, Brand Company OS, commercial launch rescue, SaaS foundation, HubSpot operating queue, and Commercial Command Room work. The correct action is **not** to merge every large PR blindly. The correct action is to create a control plane that integrates them into a safe commercial sequence.

This branch creates that control plane.

## Current GitHub reality

The latest open commercial rescue PR is `#792 — Rescue commercial launch control pack`. It contains a major founder-led commercial launch system, but it is currently not directly mergeable and is behind `main`. It has 74 commits and 123 changed files, so it should be treated as a source branch to harvest and stabilize, not as something to force-merge.

## Decision

Use this order:

1. Keep `main` stable.
2. Merge only small, green, reviewable PRs.
3. Use `#792` as the commercial source pack, but do not force merge it while it is non-mergeable.
4. Build a control-plane layer on top of current `main`:
   - loop engineering doctrine
   - commercial loop registry
   - agentic command day runner
   - safety contract tests
   - integration report
5. Rebase or recreate the large commercial rescue pack after this control plane is merged.

## Why this matters commercially

Dealix must become a company that can run daily, not a folder of disconnected AI experiments. The commercial system should produce these outputs every day:

- target priorities
- founder actions
- outreach drafts
- follow-up queue
- proposal briefs
- client delivery tasks
- trust/safety blocks
- proof pack notes
- command room state

## Safety posture

Defaults must remain:

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

Allowed in this phase:

- generate drafts
- score targets
- create founder tasks
- generate proof packs
- update reports
- update command room snapshots

Not allowed in this phase:

- automatic cold email
- automatic WhatsApp send
- SMS automation
- live billing
- fake clients
- fake testimonials
- guaranteed ROI claims
- admin merge of conflicting PRs

## Product decision

The first commercial product to sell should be:

### Dealix Agentic Command Room Sprint

A 14-day implementation that connects:

1. Revenue Command Room
2. Company Brain Daily Decision
3. Market / Competitor Watch
4. Customer Pain Radar
5. Follow-up Draft Engine
6. Proposal Brief Engine
7. Trust & Safety Gates
8. Weekly Board Memo
9. Proof Pack
10. Founder / CEO Dashboard

Suggested beta pricing: `5,000–9,000 SAR`.
Suggested standard pricing: `15,000–35,000 SAR`.
Suggested premium range: `45,000–90,000 SAR`.
Suggested retainer: `8,000–25,000 SAR/month`.

These are planning ranges, not guaranteed market prices.

## Technical decision

Create the following operating sequence:

```text
Loop registry
→ Data connector abstraction
→ Revenue loop
→ Brain loop
→ Trust loop
→ Proof pack loop
→ Command room snapshot
→ Founder review
```

The system should run without external API keys using CSV/sample data, then upgrade to HubSpot, Exa, Gmail, Railway Postgres, and other connectors under explicit configuration.

## Immediate branch scope

This PR adds:

- `docs/ops/DEALIX_LOOP_ENGINEERING_OS.md`
- `data/commercial/agentic_commercial_os_registry.json`
- `scripts/commercial/run_agentic_commercial_control_plane.py`
- `tests/saas/test_agentic_commercial_os_control_plane.py`
- `reports/go_live/AGENTIC_COMMERCIAL_OS_INTEGRATION_DECISION.md`

## Merge recommendation

Merge this branch before attempting to recover the large commercial rescue pack. It gives the repo a stable commercial execution contract that future PRs can target.

## Next PR after this

Create:

```text
phase/data-connectors-os
```

It should add:

- `app/connectors/base.py`
- `app/connectors/csv_source.py`
- `app/connectors/public_web.py`
- `app/connectors/exa_stub.py`
- `app/connectors/hubspot_stub.py`
- connector tests

## Founder operating rule

Every day Dealix should answer:

1. What changed?
2. What should be reviewed?
3. Who should be contacted manually?
4. What is unsafe to send?
5. What should be delivered?
6. What proof can we show?
