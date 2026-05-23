---
title: Model Policy
owner: Trust Lead
status: active
cadence: review-quarterly
last_review: 2026-05-23
---

# Model Policy

Which model class is allowed for which task. The point is not to pick the "best" model; it is to pick the right model class for the governance level.

## Model classes

| Class | Used for | Examples of tasks |
|---|---|---|
| Heavy | Reasoning, evaluation, governance gating | Trust OS claim filter, EVAL suite |
| Standard | Drafting, summarising | Proposal drafts, wrap-up briefs |
| Light | Classification, extraction | Lead scoring, friction tagging |

## Allowed bindings

- Heavy class is allowed for any task.
- Standard class is allowed for A0 and A1 tasks.
- Light class is allowed for A0 tasks only.
- Anything A2 or A3 is not delegated to an agent at all.

## Disallowed in policy

- Naming a specific model in code (we name a class, not a vendor model).
- Embedding model names in user-facing copy.
- Using closed-platform proxies to access models that are not allowed in our region.

## Owner

Trust Lead.
