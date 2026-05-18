# Dealix Agent Organization

Dealix runs on a coordinated organization of specialized AI agents — a
"pyramid" with `dealix-pm` as the single point of accountability orchestrating
an executive layer and an execution layer.

> Agent definitions live in `.claude/agents/*.md` (Claude Code local config,
> gitignored by repo convention). This document is the tracked, canonical
> description of the organization and how it operates.

## Governing rule

No agent ever sends external communications, charges a customer, or violates
the 11 non-negotiables. Every prospect-facing artifact (outreach, proposals,
social posts) is produced as a **draft** — the founder's approval is the only
send/publish trigger for prospect channels. Dealix's own-brand content may be
scheduled for publishing after the `safe_publishing_gate`.

## Executive / strategic layer

| Agent | Role | Owns |
|---|---|---|
| `dealix-pm` | Project management / orchestration | Plan execution, milestones, weekly cadence, delegation, decision gates |
| `dealix-strategy` | Strategy | Market & competitive analysis, positioning, offer/pricing strategy, roadmap sequencing, freeze/build-trigger calls |
| `dealix-finance` | Finance | Unit economics, pricing models, revenue forecasting, cash runway, capital/value ledgers |
| `dealix-marketing` | Marketing | Demand-gen strategy, campaign and content-calendar planning, lead-magnet strategy |
| `dealix-success` | Customer Success | Onboarding, account health scoring, retention, retainer expansion |
| `dealix-ops` | Operations | System health, verifier scripts, the 8 doctrine gates, friction-log review, launch readiness |

## Execution layer

| Agent | Role | Owns |
|---|---|---|
| `dealix-sales` | Sales | Lead qualification, outreach drafts, proposals, offer recommendation |
| `dealix-content` | Content | Bilingual docs, SOPs, case studies, proposal templates, posts, sector reports |
| `dealix-delivery` | Delivery | The 7-day Revenue Intelligence Sprint pipeline, Proof Pack assembly |
| `dealix-engineer` | Engineering | Python/FastAPI code, tests, database migrations, cron scripts |

## How work flows

1. The user — or `dealix-pm` — frames a goal.
2. `dealix-pm` delegates: the executive layer (strategy, finance, marketing,
   success) for analysis and plans; the execution layer (sales, content,
   delivery, engineer) for the work; `dealix-ops` for verification.
3. Executive agents advise and brief; they do not write product code or send
   messages. Execution agents do the work and hand external-facing output back
   as drafts.
4. `dealix-ops` confirms the doctrine gates and test suite stay green after
   every change.

## The 11 non-negotiables

1. No scraping systems. 2. No cold WhatsApp automation. 3. No LinkedIn
automation. 4. No fake / un-sourced claims. 5. No guaranteed sales outcomes.
6. No PII in logs. 7. No source-less knowledge answers. 8. No external action
without approval. 9. No agent without identity. 10. No project without a Proof
Pack. 11. No project without a Capital Asset.
