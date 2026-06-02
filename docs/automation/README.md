# Dealix Automation OS · نظام الأتمتة

> **Start here.** The governance layer that turns Dealix's existing automation
> (CI, security, deploys, founder scripts, the automation router) into one
> **least-privilege operating system** the founder can command — without ever
> handing an agent the destruct button.

This folder is **doctrine + wiring**, not new machinery. It documents how the
parts that already ship in the repo are governed and commanded.

## Read in this order · اقرأ بهذا الترتيب

| # | File | What it answers |
| --- | --- | --- |
| 1 | [`AUTOMATION_PERMISSION_MODEL.md`](AUTOMATION_PERMISSION_MODEL.md) | What can an agent do? → the **L0–L6 ladder**, the 3 rings, the 11 non-negotiables, least-privilege workflows. |
| 2 | [`CLOUD_CODE_COMMAND_CENTER.md`](CLOUD_CODE_COMMAND_CENTER.md) | How do I command it? → Issues, `workflow_dispatch`, the manual agent, the standing mission prompt. |
| 3 | [`EXTERNAL_AUTOMATION_BLUEPRINT.md`](EXTERNAL_AUTOMATION_BLUEPRINT.md) | How does the outside world plug in? → n8n / CRM / webhooks, **queue-only, never auto-send**. |

## The one rule · القاعدة الواحدة

> Maximum productivity, never the destruct button.
> Agents read, edit, PR, test, and deploy **staging**. Merge, production, secrets,
> deletes, and any external send stay in the founder's hand.

## Wired to (already in repo) · موصول بـ

- **Command surfaces:** [`.github/ISSUE_TEMPLATE/agent-command.yml`](../../.github/ISSUE_TEMPLATE/agent-command.yml) · [`.github/workflows/dealix-agent.yml`](../../.github/workflows/dealix-agent.yml) *(manual dispatch only)*
- **Enforcement:** `.github/workflows/ci.yml` (doctrine-guard tests) · `auto_client_acquisition/governance_os/` (runtime policy)
- **Doctrine:** [`../intelligence/AGENT_CONTROL_DOCTRINE.md`](../intelligence/AGENT_CONTROL_DOCTRINE.md) · [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md)
- **Audit:** [`../governance/AGENT_REGISTRY.md`](../governance/AGENT_REGISTRY.md) · [`../governance/AI_RUN_LEDGER.md`](../governance/AI_RUN_LEDGER.md)
- **Founder cadence:** `make cockpit` · `governed-full-ops-daily.yml` · `founder_weekly_scorecard.yml`
