# Dealix Agent Governance — حوكمة فريق الوكلاء

The control room for the Dealix agent ecosystem. Dealix already has the muscles
(`.claude/agents`, `.codex/agents`, `.cursor/rules`, `core/agents`,
`autonomous_growth/agents`, `mcp_server`, `token-optimizer`, strong CI, production
gates, founder scripts). These docs are the single place that answers: *who are the
agents, what may each one do, what does each produce, and what is forbidden?*

## Read in this order

1. [`AGENT_TEAM_REGISTRY.md`](AGENT_TEAM_REGISTRY.md) — the canonical roster: surfaces, the 5 real sub-agents, the 11 non-negotiables, and how to add an agent.
2. [`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md) — permission levels L0–L6 and each agent's default; the hard rules.
3. [`AGENT_OUTPUT_CONTRACT.md`](AGENT_OUTPUT_CONTRACT.md) — the 8-field footer every agent output must take, with the evidence ladder.
4. [`AGENT_DAILY_RUNBOOK.md`](AGENT_DAILY_RUNBOOK.md) — the one canonical daily command (links existing scripts, no new wrapper).
5. [`AGENT_SECURITY_POLICY.md`](AGENT_SECURITY_POLICY.md) — hard boundaries + recommended GitHub branch protection / required checks / rulesets.
6. [`TOKEN_BUDGET_POLICY.md`](TOKEN_BUDGET_POLICY.md) — keep runs cheap; uses the `token-optimizer/` layer.
7. [`PR_TRIAGE_POLICY.md`](PR_TRIAGE_POLICY.md) — sort open PRs into actionable buckets; humans merge.

## Verify the fleet is governed

```bash
make agents-audit     # python scripts/audit_agent_team.py
```

This checks every agent surface exists, that Claude ↔ Codex sub-agents stay in
parity, that each agent declares its identity (frontmatter), that the governance
docs above are present, and that the doctrine guard tests exist. CI runs the same
check on every PR via [`../../.github/workflows/agent-team-audit.yml`](../../.github/workflows/agent-team-audit.yml).

## Related

- [`../../AGENTS.md`](../../AGENTS.md) — repo dev commands + conventions (read first).
- [`../ops/FOUNDER_AGENT_PLAYBOOK_AR.md`](../ops/FOUNDER_AGENT_PLAYBOOK_AR.md) — founder-facing agent playbook (AR).
- [`../../token-optimizer/README.md`](../../token-optimizer/README.md) — token-saving layer.
