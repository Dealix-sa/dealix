---
title: Prompt Review Policy
owner: Trust Lead
status: active
cadence: review-monthly
last_review: 2026-05-23
---

# Prompt Review Policy

A prompt is a unit of business logic. Changes are reviewed like code.

## What counts as a prompt change

- A change to any prompt template used by an agent in the [AGENT_REGISTRY.md](./AGENT_REGISTRY.md).
- A change to any system prompt.
- A change to a few-shot example.

## Review process

1. Prompt diff is opened in the prompt store with a one-paragraph "why".
2. Trust Lead reviews against the [docs/trust/SAFE_LANGUAGE_LIBRARY.md](../trust/SAFE_LANGUAGE_LIBRARY.md).
3. The new prompt must pass the existing EVAL suite (see [EVAL_POLICY.md](./EVAL_POLICY.md)).
4. Founder approves A1 for production rollout.

## What blocks a prompt change

- Any banned phrase appearing in the prompt or in its examples.
- Any reference to an external system the agent is not allowed to touch.
- A failing EVAL.

## Audit trail

- The full prompt history is stored in the Prompt Registry.
- The AI Run Ledger captures the prompt hash for every run.

## Owner

Trust Lead.
