---
title: Agent EVAL Policy
owner: Trust Lead
status: active
cadence: review-monthly
last_review: 2026-05-23
---

# Agent EVAL Policy

How an agent earns the right to ship and the right to keep shipping.

## EVAL types

| EVAL | Cadence | What it measures |
|---|---|---|
| Pre-prod | Before any deployment | Does the agent stay in scope? Does it trigger any banned phrase? |
| Daily smoke | Every morning | Did anything regress overnight? |
| Weekly diff | Every Monday | Has output drifted vs last week? |
| Incident | After an incident | Did the agent's output contribute? |

## Pass criteria

- Zero banned-phrase hits.
- Zero out-of-scope actions.
- Output passes JSON schema validation where applicable.
- Manual spot-check by Trust Lead on three sampled runs.

## Failure handling

- One failure: warning logged.
- Two failures: A1 manual approval required for every run until clean.
- Three consecutive failures: agent auto-paused (`blocked`).

## Owner

Trust Lead.
