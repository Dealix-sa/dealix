# Dealix Agent Daily Runbook — دليل التشغيل اليومي للوكلاء

One canonical path. Dealix already has a strong daily/weekly operating spine — this
runbook **consolidates** it; it does not invent a new command. The rule is
*registry → audit → runbook → metrics → triage → activation*.

Read with [`AGENT_TEAM_REGISTRY.md`](AGENT_TEAM_REGISTRY.md). The deeper founder
docs are [`docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md`](../ops/FOUNDER_DAILY_OPERATING_RHYTHM.md)
and [`docs/ops/FOUNDER_AGENT_PLAYBOOK_AR.md`](../ops/FOUNDER_AGENT_PLAYBOOK_AR.md) —
this file links to them rather than duplicating them.

---

## 1. Daily — offline, safe, no external sends

Run from the repo root. None of these write to production or send anything.

```bash
make doctor                                          # env contract + single alembic head + security smoke
python scripts/audit_agent_team.py                   # agent fleet is governed (registry + parity + docs)
python scripts/verify_full_autonomous_ops_stack.py   # the autonomous ops stack is wired
python scripts/run_dealix_daily_ops.py --skip-api    # offline daily loop → data/founder_briefs/
python scripts/run_dealix_complete_autonomous_day.py # full autonomous day (read/recommend only)
bash scripts/founder_one_command.sh                  # one-command maximum automation
```

The day's brief lands in `data/founder_briefs/`; the agent audit lands in
`reports/agents/`.

## 2. Weekly — gates + scorecard

```bash
bash scripts/founder_weekly_loop.sh        # Sunday gates
make agents-audit                          # confirm no agent drifted out of the registry
make pr-triage                             # bucket open PRs (see PR_TRIAGE_POLICY.md)
```

## 3. Before production / live (human-approved only)

```bash
make prod-verify                                   # canonical production-readiness bundle
bash scripts/verify_founder_ops_launch.sh          # launch gate
bash scripts/verify_dealix_commercial_go_live.sh   # commercial go-live verdict
```

> Live external sends, payment cutover, and production deploys are **human
> actions**. No agent runs section 3 autonomously.

---

## The per-agent loop (every invocation)

1. **Read first:** `AGENTS.md` → [`AGENT_TEAM_REGISTRY.md`](AGENT_TEAM_REGISTRY.md) →
   the agent's own definition.
2. **Identify** business impact + risk level + the verification command (the
   [output contract](AGENT_OUTPUT_CONTRACT.md) fields).
3. **Stay in lane:** respect the agent's default permission level
   ([matrix](AGENT_PERMISSION_MATRIX.md)). Escalate only with human approval.
4. **Do the smallest safe change.** Reuse before adding; link before duplicating.
5. **Verify** with the command from the registry. Report pass/fail honestly.
6. **Close** with the 8-field [output contract](AGENT_OUTPUT_CONTRACT.md) footer.

## Token discipline

Keep runs cheap and high-signal — see [`TOKEN_BUDGET_POLICY.md`](TOKEN_BUDGET_POLICY.md)
and [`token-optimizer/`](../../token-optimizer/). Read targeted files, prefer the
quick regression bundle over the full suite, stop when acceptance criteria are met.

---

## First-time setup (once per environment)

```bash
python -m pip install -e ".[dev]"                       # dev tooling
bash token-optimizer/12-environment-config/apply-all.sh # apply token-saving settings
make doctor
python scripts/audit_agent_team.py
```
