# Dealix Agent Skills Pack

## Executive decision

This repository is the main Dealix project repository, so Dealix agent skills should live here as **project-level operating instructions**, not only in the standalone `Dealix-sa/skills` CLI repository.

The purpose of this pack is to give Claude Code, Codex, Cursor, Kimi Code, OpenCode, Roo, Continue, and similar agents a consistent way to work on Dealix without re-explaining the entire project every time.

## What this pack does

It adds Dealix-specific skills under:

```text
.agents/skills/dealix/
```

This location follows the common project-level skills convention used by agent tooling. The skills are intentionally markdown-only: they do not change runtime code, dependencies, outbound settings, database schema, or deployment behavior.

## Included skills

| Skill | Purpose |
|---|---|
| `dealix-release-engineer` | Stabilize PRs, CI, build, Railway/frontend/backend surfaces, and safe release gates |
| `dealix-revenue-command-room` | Run target scoring, drafts, follow-ups, proposal briefs, and revenue reports |
| `dealix-company-brain-os` | Convert company signals into daily founder decisions and weekly memos |
| `dealix-client-growth-operator` | Prepare controlled channel actions for email, WhatsApp, LinkedIn, phone, and proposals |
| `dealix-client-delivery-os` | Deliver client work through intake, diagnosis, scope, blueprint, proof pack, and handoff |
| `dealix-loop-operating-system` | Convert scattered scripts into bounded operating loops with verifiers and reports |
| `dealix-trust-and-outbound-safety` | Review claims, privacy, consent, opt-out, approval cards, and outbound policy gates |

## Safety baseline

Every Dealix skill assumes this baseline unless a later controlled-live PR explicitly changes it:

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Rules for agents

1. Do not push directly to `main`.
2. Do not use admin merge.
3. Do not enable live outbound by default.
4. Do not create fake ROI, fake clients, fake testimonials, fake logos, or guaranteed revenue claims.
5. Do not automate LinkedIn DMs, WhatsApp sends, SMS, robocalls, or website form spam.
6. Prefer small PRs with validation reports.
7. Keep generated reports/outbox artifacts out of source commits unless intentionally part of a release proof pack.
8. Always produce a final report with branch, files changed, commands run, safety status, blockers, and next action.

## Recommended usage sequence

When working on Dealix, use skills in this order:

1. `dealix-release-engineer`
2. `dealix-loop-operating-system`
3. `dealix-revenue-command-room`
4. `dealix-company-brain-os`
5. `dealix-client-growth-operator`
6. `dealix-client-delivery-os`
7. `dealix-trust-and-outbound-safety`

## Discovery

Because these skills are committed directly inside the Dealix repo, supported agents can read them from project context. If using the external `skills` CLI, run from the Dealix repo after this PR is merged:

```bash
npx skills list
npx skills use . --skill dealix-release-engineer --full-depth
```

## Future expansion

Next useful project skills:

- `dealix-hubspot-os`
- `dealix-railway-production-ops`
- `dealix-saas-foundation`
- `dealix-website-brand-os`
- `dealix-market-watch-os`
- `dealix-proof-pack-os`
