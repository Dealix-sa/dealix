# Open Design to Dealix OS

## Source reviewed

Source repository: `nexu-io/open-design`

Open Design is a local-first, open-source design workspace built around agentic design loops, design systems, skills, plugins, artifact streaming, sandboxed preview, and exportable outputs.

Dealix should not vendor the full Open Design repository into this repo. The repository is large, desktop-oriented, and built as its own product/workspace. Instead, Dealix should absorb the operating pattern:

```text
brief -> design system contract -> agent skill -> artifact -> critique -> export -> handoff
```

## Why this matters for Dealix

Dealix needs a practical design/product engine for:

- sales decks
- landing pages
- dashboards
- command room screens
- proposal pages
- client proof packs
- onboarding flows
- mobile/desktop prototypes
- brand-consistent visual assets

The best adaptation is a Dealix-native **Design Command Room OS** that lives inside the project and guides agents while preserving Dealix's stack, brand, safety rules, and commercial launch priorities.

## What to copy conceptually

| Open Design pattern | Dealix adaptation |
|---|---|
| `DESIGN.md` as brand contract | `docs/design/DEALIX_DESIGN.md` as the canonical Dealix design contract |
| Skills + design systems | Project-level skills under `.agents/skills/dealix/` |
| Artifact streaming | Generate reviewable HTML/MD/PDF-ready artifacts in `reports/`, `apps/web`, or `docs/` |
| Sandboxed preview | Keep generated artifacts isolated from production routes until approved |
| CLI/agent compatibility | Support Claude Code, Codex, Cursor, Kimi, OpenCode, and similar agents through project docs |
| Automation page | Dealix loops: revenue, company brain, delivery, design, proof pack, release |
| MCP/integrations concept | Future optional integration only; do not block Dealix core on MCP |

## What not to do

Do not:

- copy the whole Open Design repo into Dealix
- add Electron/Desktop runtime into Dealix now
- add Node 24/pnpm 10 constraints to Dealix just because Open Design uses them
- add large image/media assets from Open Design
- add unrelated plugin stores
- replace Dealix's current frontend architecture
- weaken outbound safety gates
- create generated artifacts directly in production UI without review

## Dealix-native target architecture

```text
Dealix Design Command Room OS
├── Brand Contract
│   └── docs/design/DEALIX_DESIGN.md
├── Agent Skill
│   └── .agents/skills/dealix/design-command-room/SKILL.md
├── Artifact Rules
│   └── docs/design/ARTIFACT_RULES.md
├── Output Surfaces
│   ├── apps/web/app/
│   ├── reports/command_room/
│   ├── reports/proof/
│   └── sales/
└── Validation
    ├── visual review checklist
    ├── accessibility checklist
    ├── brand consistency checklist
    └── no fake claims / no live outbound gate
```

## First Dealix use cases

### 1. Revenue Command Room UI

Generate a clear dashboard screen for daily targets, follow-up queue, proposal pipeline, approval cards, live-send status, and next 10 actions.

### 2. Founder War Room

Generate a CEO view for what changed today, highest-value decision, blockers, cash/revenue risks, delivery risks, and recommended action.

### 3. Client Proof Pack

Generate proof pack pages for diagnosis, before/after workflow, prepared actions, verified results, and next 30 days.

### 4. Sales deck generator

Generate client-specific decks from prospect sector, pain hypothesis, Dealix offer, proof and assumptions, and implementation timeline.

### 5. Landing page generator

Generate brand-consistent pages for Dealix homepage, Saudi B2B AI OS offer, Revenue Command Room service, Client Growth Operator service, and Company Brain OS service.

## Design output contract

Every Dealix design artifact must include:

```text
artifact_name
business_goal
primary_user
source_context
brand_tokens_used
screens_or_sections
copy_claims_reviewed
safety_status
handoff_target
approval_status
```

## Artifact approval states

```text
draft
needs_review
approved_for_demo
approved_for_client
approved_for_production
rejected
```

No artifact may move to production without review.

## Brand safety

All generated pages, decks, and proof packs must avoid fake ROI, fake testimonials, fake customers, unverifiable partnership claims, guaranteed revenue claims, dark patterns, hidden automation claims, and live outbound implications unless gates exist.

## Recommended next implementation PRs

1. Add `docs/design/DEALIX_DESIGN.md` as canonical brand contract.
2. Add `docs/design/ARTIFACT_RULES.md`.
3. Add `scripts/design/generate_design_artifact.py`.
4. Add `reports/design/latest.md` output.
5. Add `make design-room` target.
6. Add one reviewed HTML prototype for Revenue Command Room.

## Current PR scope

This PR intentionally adds docs and agent instructions only. It does not vendor Open Design, alter dependencies, or change production runtime.
