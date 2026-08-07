# Dealix Artifact Approval States

Use these states for design artifacts, generated pages, decks, dashboards, proposals, and proof packs.

```text
draft
needs_review
approved_for_demo
approved_for_client
approved_for_production
rejected
```

## Rules

- `draft`: internal only.
- `needs_review`: ready for human review.
- `approved_for_demo`: can be shown in a demo context.
- `approved_for_client`: can be sent or shown to a client.
- `approved_for_production`: can be implemented or promoted into production UI.
- `rejected`: do not use.

## Required before production

```text
Reviewed by:
Date:
Safety status:
Claims status:
Data sensitivity status:
Handoff target:
```
