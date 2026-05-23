# Learning Loop

The Learning Loop is the discipline of converting every experiment outcome, customer interaction, and policy decision into a recorded, searchable learning that future decisions can read.

**Source of truth:** `$PRIVATE_OPS/learning_log.csv`
**Owner:** Founder
**Trust gate:** A1 — learnings are reviewed monthly.

## Row schema

```
learning_id, recorded_at, source_type, source_id,
headline, evidence, generalisation, counterexamples,
linked_change[], status
```

`source_type`: `experiment`, `client_engagement`, `policy_decision`, `external_event`, `red_team`, `audit_finding`.

`status`: `proposed`, `tentative`, `confirmed`, `superseded`, `retracted`.

## What makes a good learning

A learning is not "the experiment passed". A learning is a generalisable observation supported by evidence. The standard fields:

| Field | Question |
|-------|----------|
| Headline | One sentence the founder can recall |
| Evidence | What data, what artifact, what observation |
| Generalisation | Where else this likely holds |
| Counterexamples | Where this might not hold |
| Linked change | What in the OS we changed because of it |

## Cadence

| Cadence | Activity |
|---------|----------|
| Weekly | New learnings reviewed for promotion to `tentative` |
| Monthly | `tentative` reviewed for promotion to `confirmed` |
| Quarterly | `confirmed` reviewed; supersession and retraction |

## Promotion rules

| From | To | Requirement |
|------|----|-----------:|
| Proposed | Tentative | Evidence in two independent sources |
| Tentative | Confirmed | Either an experiment or three corroborating observations |
| Confirmed | Superseded | A better learning explains the same facts |
| Confirmed | Retracted | Counter-evidence that breaks the generalisation |

## Connection to other systems

| System | Connection |
|--------|-----------|
| Experiment Backlog | Every concluded experiment writes a candidate learning |
| Capital Ledger (`docs/09_capital_os/CAPITAL_LEDGER.md`) | Confirmed learnings become reusable capital |
| Policy as Code | Confirmed learnings may motivate policy changes |
| Brand voice | Confirmed learnings may update Brand Voice Examples |

## Failure modes

- **Recording theatre:** learnings logged but never used. Detection: linked-change density audit. Recovery: monthly review of unused confirmed learnings.
- **Premature confirmation:** a learning promoted without evidence. Detection: founder review. Recovery: demote to tentative.
- **Counterevidence ignored:** a confirmed learning persists despite contradicting facts. Detection: quarterly audit. Recovery: retract.

## Recovery path

If learning quality degrades (high retraction rate, low linked-change rate), the founder pauses promotion and runs a learning audit.

## Metrics

- Learnings recorded per quarter.
- Promotion rate (proposed → tentative → confirmed).
- Retraction rate per quarter.
- Linked-change density (linked changes per confirmed learning).

## Disclaimer

Learnings are interpretations of evidence. They do not guarantee future outcomes. Estimated value is not Verified value.
