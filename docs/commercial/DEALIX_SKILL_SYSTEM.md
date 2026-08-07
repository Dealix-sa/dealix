# Dealix Skill System

## Purpose

This document defines the reusable operating skill for Dealix Autonomous Company OS.

A packaged ChatGPT skill was prepared separately as `skill.zip` with the same operating rules.

## Skill trigger scope

Use the Dealix Autonomous Company OS skill when a task involves:

- Dealix repo implementation
- GitHub PRs/issues/checks
- Production trust / Railway / CI
- Revenue Command Room
- Company Brain
- Opportunity Graph
- Approval Center
- Proof Ledger
- Autonomous Growth OS
- Self-Improvement OS
- Slack/Airtable/Contacts connector workflows
- Daily Dealix execution
- Money Now Sprint
- Client pilot playbooks

## Skill operating rules

- Treat Dealix as a Saudi B2B AI-native Company OS.
- Start with Dealix internal execution before client SaaS.
- Keep external actions draft-only and approval-first.
- Never send, publish, merge, charge, or mutate production without explicit approval.
- Never create fake proof or guaranteed claims.
- Use GitHub as source-of-truth for implementation.
- Use Slack/Airtable/Sheets as operating surfaces when available.

## Skill package contents

```txt
dealix-autonomous-company-os/
  SKILL.md
  agents/openai.yaml
  references/implementation_matrix.md
  references/safety_policy.md
```

## Required reusable workflow

1. Inspect current state.
2. Classify into P0/P1/P2/P3.
3. Create or update GitHub execution artifacts.
4. Mirror into operating board if available.
5. Generate approval queue.
6. Generate proof log.
7. Run or propose verification.
8. Report honestly what succeeded and what was blocked.

## Default verification commands

```bash
python scripts/commercial/run_company_os_daily.py --client dealix --mode draft-only --limit 50
python scripts/commercial/run_autonomous_growth_daily.py --autonomy-level 3 --mode draft-only --limit 50
python scripts/commercial/run_self_improvement_daily.py --client dealix --mode draft-only
python scripts/commercial/verify_company_os_foundation.py
python scripts/commercial/verify_autonomous_growth.py
python scripts/commercial/verify_self_improvement.py
```
