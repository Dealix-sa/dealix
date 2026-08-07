# Dealix Token Budget Policy — سياسة ميزانية التوكنز

Keep agent runs cheap, focused, and high-signal. Dealix already ships a full
token-optimization layer in [`token-optimizer/`](../../token-optimizer/) — 12 guides
covering `.claudeignore`, CLAUDE.md hygiene, session management, model routing,
MCP discipline, subagents, hooks, prompt templates, file handling, monitoring, git
hygiene, and env config. This policy turns that layer into a daily habit.

---

## The golden rule

> **Every line Claude does not read = tokens saved.** / كل سطر لا يراه Claude = توكنز محفوظة.

## Rules

1. **Read `AGENTS.md` first.** It is the map; it prevents re-discovery.
2. **Use repo maps and targeted reads** before opening large files. Read the part
   you need, not the whole file.
3. **Prefer the quick regression bundle** (in `AGENTS.md`) over the full suite while
   iterating; run the full suite only before you ship.
4. **Small PRs.** A focused diff costs less to produce, review, and verify.
5. **Link, don't paste.** Reference a doc by path instead of pasting it into context.
6. **Right model for the job.** Cheaper models for summarize/triage; the strongest
   model for architecture and security decisions (`token-optimizer/04-model-routing/`).
7. **Delegate narrow work to subagents** (`token-optimizer/06-subagents/`) so each
   keeps a small, relevant context.
8. **MCP discipline** (`token-optimizer/05-mcp-discipline/`) — only load the tools a
   task needs.
9. **Stop when acceptance criteria are met.** Don't gold-plate.

## Apply the settings (once per environment)

```bash
bash token-optimizer/12-environment-config/apply-all.sh
```

This installs the optimized `.claudeignore`, settings, and hooks from the
token-optimizer layer.

## Measure (optional weekly)

`token-optimizer/10-tools-monitoring/` covers usage monitoring. When you review
spend, capture the takeaways in `reports/agents/TOKEN_BUDGET_REVIEW.md` (kept out of
git by default; see `.gitignore`) and feed any rule changes back into this file.

---

See also: [`AGENT_DAILY_RUNBOOK.md`](AGENT_DAILY_RUNBOOK.md) ·
[`token-optimizer/README.md`](../../token-optimizer/README.md).
