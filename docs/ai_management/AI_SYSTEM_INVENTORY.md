# AI System Inventory

> Every AI agent and pipeline, named, mapped, and owned.
> An un-inventoried agent is an un-governed agent.

## Inventory Schema

For each agent / pipeline:

```
- id: AI-NN
  name: "..."
  purpose: "..."
  owner: Sami
  inputs:
    - "..."
  outputs:
    - "..."
  models_used:
    - vendor: "..."
      model: "..."
      version: "..."
  autonomy_tier: A0 / A1 / A2 / A3
  human_in_loop: where in the flow
  data_classes:
    - public / internal / customer_personal
  retention: "..."
  evaluation_suite: path/to/eval
  release_status: pre-prod / prod / deprecated
  last_release_gate: yyyy-mm-dd
```

## Inventory

### AI-01 — Lead Scorer

- Purpose: Score new leads on ICP rubric.
- Inputs: lead row (company, role, sector, signals).
- Outputs: 0–25 score, A/B/C/D tag.
- Autonomy: A0 (analysis only).
- Data: internal.
- Models: classifier; LLM for unstructured signal extraction.

### AI-02 — Outreach Draft Generator

- Purpose: Draft personalised DM/email per qualified lead.
- Inputs: lead row + ICP context + sector pack.
- Outputs: bilingual draft message + cited evidence anchors.
- Autonomy: A1 (draft only).
- Data: internal; output reviewed before any A3 send.
- Models: LLM.

### AI-03 — Sample Pack Builder

- Purpose: Build a 1-page Signal Sample for a prospect.
- Inputs: target ICP, 3 named accounts, signals.
- Outputs: PDF / Markdown sample with evidence links.
- Autonomy: A1.
- Data: internal + cited public data.

### AI-04 — Executive Memo Drafter

- Purpose: Summarise a Sprint into an executive memo.
- Inputs: Sprint dataset.
- Outputs: 1-page memo with caveats and unknowns.
- Autonomy: A1.

### AI-05 — QA Checker

- Purpose: Run the QA checklist on a Proof Pack pre-handoff.
- Inputs: Proof Pack candidate.
- Outputs: pass/fail per check; list of issues.
- Autonomy: A0–A1.

### AI-06 — Friction Log Triage

- Purpose: Cluster recent customer comments / loss reasons.
- Inputs: friction log + loss reasons.
- Outputs: pattern summary.
- Autonomy: A0.

### AI-07 — Doctrine Verifier

- Purpose: Scan repo for forbidden phrases and missing evidence links.
- Inputs: repo content.
- Outputs: violation report.
- Autonomy: A0.

## Adding a new agent

1. Define purpose, inputs, outputs.
2. Map to autonomy tier (default: lowest viable).
3. Add to threat model (`AI_THREAT_MODEL.md`).
4. Define eval suite.
5. Pass release gate (`AI_AGENT_RELEASE_GATE.md`).
6. Add to this inventory.
7. Add to risk register.

## Deprecating an agent

1. Mark `release_status: deprecated`.
2. Move associated evals to `evals/_deprecated/`.
3. Document in `KILL_LIST.md` if structurally retired.
