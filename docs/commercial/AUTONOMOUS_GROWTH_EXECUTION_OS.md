# Dealix Autonomous Growth & Strategy Execution OS

## Purpose

This document defines the execution layer that turns Dealix from a passive product into a daily operating company system.

The goal is not spam, uncontrolled outbound, or a generic CRM. The goal is an approval-first execution engine that can understand Dealix strategies, choose the highest-value work, execute safe internal actions, prepare external actions for human approval, and produce proof every day.

## Operating doctrine

Dealix must remain:

- Saudi-first
- Arabic-first
- Approval-first
- Proof-backed
- Draft-only by default
- No cold WhatsApp
- No prohibited scraping
- No guaranteed revenue claims
- No government-access claims
- No fake proof
- No secrets in prompts, logs, reports, or git

## What the system does every day

The daily engine should:

1. Load the strategy registry.
2. Read available commercial and technical context.
3. Prioritize the most valuable strategies for the day.
4. Execute internal-safe actions.
5. Create approval queues for external/high-risk actions.
6. Produce outreach drafts only.
7. Produce content drafts only.
8. Produce partner/referral/SEO growth suggestions.
9. Produce a proof log.
10. Produce a founder daily report.
11. Store learning notes for the next run.

## Autonomy levels

| Level | Name | Allowed behavior |
|---|---|---|
| 0 | Observe | Read context only. |
| 1 | Analyze | Summarize, prioritize, classify, and score. |
| 2 | Draft | Generate reports, drafts, plans, and recommendations. |
| 3 | Internal execute | Write reports, queues, proof logs, and local artifacts. |
| 4 | Repo execute | Prepare branches/PR drafts, run tests, and make internal patches when explicitly enabled. |
| 5 | External execute | Send, publish, merge, charge, change production. Blocked unless explicit approval is implemented. |

Default production posture: **Level 3, draft-only**.

## Strategy registry

The strategy registry should include:

- technical_trust
- revenue_sprint
- saudi_market_access
- foreign_company_targeting
- local_b2b_growth
- b2g_readiness
- content_factory
- proof_pack
- partner_growth
- referral_loop
- seo_market_reports
- founder_daily_ops

Each strategy defines:

- goal
- target customer
- inputs
- allowed actions
- blocked actions
- steps
- outputs
- KPIs
- approval requirements
- stop conditions
- proof requirements
- learning rules

## Growth without bans

Dealix should grow through value loops, not spam loops:

- Saudi Opportunity Snapshots
- Revenue Leak Scanner checklists
- B2G readiness checklists
- proof-pack content
- founder LinkedIn/X drafts
- SEO market reports
- referral prompts
- partner intro drafts

Forbidden:

- cold WhatsApp blasts
- mass LinkedIn automation
- email scraping that violates terms
- fake personalization
- fake case studies
- guaranteed revenue claims
- government-access claims
- bypassing platform rate limits

## Local model / server posture

Dealix can use local models, but the model server must be private:

- Ollama for local/simple tasks.
- vLLM for future GPU production serving.
- OpenRouter/Groq/fallback providers only when needed.
- Never expose Ollama/vLLM publicly without auth, firewall, VPN/Tailscale, and rate limits.
- Never send secrets or customer-sensitive data to untrusted models.

## First implementation target

The first implementation should compose with the Saudi Opportunity Command Room rather than duplicate it:

- Use `dealix/opportunity_graph` for companies, scoring, drafts, approvals, reports, and proof packs.
- Use draft-only runners.
- Add a daily GitHub Action only after the runner is deterministic and does not require secrets.
- Keep generated reports and JSON queues out of git unless they are samples.

## Acceptance criteria

The system is ready for daily use only when:

1. It can run without secrets.
2. It generates a daily report.
3. It generates an action queue.
4. It generates an approval queue.
5. It generates a proof log.
6. It never sends externally.
7. It never publishes content.
8. It never merges PRs.
9. It never changes production.
10. It records what is safe, what is blocked, and what requires founder approval.
