# Dealix Agent Team Registry — سجل فريق الوكلاء

This file is the **canonical registry** of every Dealix AI agent surface. It does
not replace the agent definitions themselves — it indexes them, states who owns
each one, what it is allowed and forbidden to do, what it consumes and produces,
and the command that verifies it. Read it together with:

- [`../../AGENTS.md`](../../AGENTS.md) — repo-specific dev commands and conventions.
- [`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md) — permission levels (L0–L6).
- [`AGENT_OUTPUT_CONTRACT.md`](AGENT_OUTPUT_CONTRACT.md) — the shape every agent output must take.
- [`AGENT_DAILY_RUNBOOK.md`](AGENT_DAILY_RUNBOOK.md) — the one canonical daily command.
- [`AGENT_SECURITY_POLICY.md`](AGENT_SECURITY_POLICY.md) — hard security boundaries + GitHub governance.

> **Audit this file's promises:** `make agents-audit` (or `python scripts/audit_agent_team.py`).
> It verifies every surface below exists, that Claude ↔ Codex agents stay in parity,
> and that the governance docs are present.

---

## The Dealix constitution (highest law for every agent)

From [`../../README.md`](../../README.md):

> **AI explores, analyzes, and recommends. Deterministic workflows execute.
> Humans approve critical external commitments.**

No agent overrides this. An agent may *draft, analyze, score, and recommend*; a
deterministic workflow *executes*; a human *approves* anything that leaves the
building (external send, payment, production deploy, secret change).

## The 11 non-negotiables (enforced in code by passing tests)

These are not aspirational — each is guarded by a test that CI runs on every PR.
The canonical source is the agent definitions and the MCP `get_doctrine_rules` tool.

| # | Rule | Guard test |
|---|------|-----------|
| 1 | No scraping systems | `tests/test_no_scraping_engine.py` |
| 2 | No cold WhatsApp automation | `tests/test_no_cold_whatsapp.py` |
| 3 | No LinkedIn automation | `tests/test_no_linkedin_automation.py` |
| 4 | No fake / un-sourced claims | `tests/test_no_guaranteed_claims.py` |
| 5 | No guaranteed sales outcomes | `tests/test_no_guaranteed_claims.py` |
| 6 | No PII in logs | `tests/test_no_pii_in_logs.py` |
| 7 | No source-less knowledge answers | `tests/test_no_source_no_answer.py` |
| 8 | No external action without approval | `tests/test_pii_external_requires_approval.py` |
| 9 | No agent without identity | this registry + frontmatter audit |
| 10 | No project without Proof Pack | `tests/test_proof_pack_required.py` |
| 11 | No project without Capital Asset | `tests/test_commercial_doctrine.py` |

If a request or in-progress change would violate any of these, the agent
**refuses and proposes a safe alternative**. It never improvises around them.

---

## Agent surfaces (where agents actually live)

Dealix runs agents across **six surfaces**. The audit script counts files in each.

| Surface | Path | What lives here |
|---|---|---|
| Claude Code sub-agents | [`.claude/agents/`](../../.claude/agents/) | 5 specialist sub-agents (markdown) |
| Codex sub-agents | [`.codex/agents/`](../../.codex/agents/) | the same 5, mirrored as TOML |
| Cursor rules | [`.cursor/rules/`](../../.cursor/rules/) | founder-sales rules, v3 rules, agent-work rules |
| Internal agent runtime | [`core/agents/`](../../core/agents/) | `base.py` (BaseAgent), `multi_agent.py`, `tools.py` |
| Autonomous growth swarm | [`autonomous_growth/agents/`](../../autonomous_growth/agents/) | competitor, content, sector_intel, market_research, enrichment, product_router, proposal_sender, distribution |
| MCP tool surface | [`mcp_server/`](../../mcp_server/) | read-only Business OS tools (war-room, KPIs, doctrine, cockpit, ...) |

The agents call **deterministic execution planes** in
[`auto_client_acquisition/`](../../auto_client_acquisition/): `data_os`,
`governance_os`, `proof_os`, `value_os`, `capital_os`, `adoption_os`,
`friction_log`, `client_os`, `sales_os`. Agents *recommend*; these planes *execute*.

---

## Agent classes (what each class may do)

| Class | Purpose | Edit code | Open PR | Deploy | Human approval |
|---|---|:--:|:--:|:--:|---|
| Orchestrator | priorities, cadence, delegation | docs/data | yes | no | for any external commitment |
| Revenue | prospects, offers, outreach drafts | docs/data | yes | no | for external sends |
| Delivery | sprint delivery, Proof Packs, handover | docs/data | yes | no | for client commitments |
| Product | FastAPI / Next.js / integrations | yes | yes | staging only | for production |
| Content | bilingual docs, SOPs, templates | docs only | yes | no | for claims above evidence level |

Permission levels (L0–L6) are defined in
[`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md).

---

## Canonical sub-agents (the real roster)

These are the agents that exist today in `.claude/agents/` and `.codex/agents/`.
Each entry is the **summary** — the full definition is the linked file.

### 1. `dealix-pm` — Orchestrator (Founder Command hat)

- **Source:** [`.claude/agents/dealix-pm.md`](../../.claude/agents/dealix-pm.md) · [`.codex/agents/dealix-pm.toml`](../../.codex/agents/dealix-pm.toml)
- **Mission:** single point of accountability for the 90-day commercial activation plan; coordinates the other four sub-agents.
- **Permission level:** L1 (docs/data writer + delegation). Owns 30/60/90 milestones, weekly cadence, friction-log review, decision gates.
- **Inputs:** the 90-day plan, `AGENTS.md`, friction log, git status, the 30/60/90 docs in `docs/ops/`.
- **Outputs:** session todo plan, delegated sub-agent missions, daily brief (`data/daily_brief/`), status summaries.
- **Allowed:** create reports, propose PR missions, delegate, run tests/smoke, commit + push.
- **Forbidden:** charge a customer, send external messages, change secrets, deploy production, amend the user's commits without permission.
- **Verify:** `make cockpit` · `python scripts/founder_daily_five_metrics.py`

### 2. `dealix-sales` — Revenue (Revenue OS hat)

- **Source:** [`.claude/agents/dealix-sales.md`](../../.claude/agents/dealix-sales.md) · [`.codex/agents/dealix-sales.toml`](../../.codex/agents/dealix-sales.toml)
- **Mission:** run the founder-led sales motion — qualify leads, render proposals, draft warm-list outreach, recommend a rung from the 5-rung ladder.
- **Permission level:** L1–L2 (docs/data + PR builder for sales pages).
- **Inputs:** `auto_client_acquisition/sales_os/`, `docs/commercial/`, `data/templates/`, lead intake.
- **Outputs:** qualification decisions, bilingual proposal drafts, warm-list message variants, discovery agendas — **all queued for founder approval**.
- **Allowed:** qualify, render proposals, draft outreach for approval.
- **Forbidden:** send anything externally itself; draft cold WhatsApp / LinkedIn automation / scraping; promise guaranteed sales.
- **Verify:** `bash scripts/revenue_os_master_verify.sh` · `python scripts/commercial_value_map_status.py`

### 3. `dealix-delivery` — Delivery (Trust + Proof hat)

- **Source:** [`.claude/agents/dealix-delivery.md`](../../.claude/agents/dealix-delivery.md) · [`.codex/agents/dealix-delivery.toml`](../../.codex/agents/dealix-delivery.toml)
- **Mission:** run the 7-day Revenue Intelligence Sprint per customer with a full evidence trail (Source Passport → DQ → scoring → drafts → governance → Proof Pack → Capital Asset → retainer check).
- **Permission level:** L1 (docs/data writer, ledger-recording).
- **Inputs:** `data_os`, `revenue_os`, `governance_os`, `proof_os`, `value_os`, `capital_os`, `adoption_os`, `friction_log`.
- **Outputs:** step-by-step delivery log, 14-section Proof Pack (score + tier), ≥1 Capital Asset, retainer eligibility verdict, friction events.
- **Allowed:** run the playbook in order, record to every ledger, assemble Proof Packs.
- **Forbidden:** send externally without approval; auto-promote value tiers; close an engagement without a Proof Pack + ≥1 Capital Asset.
- **Verify:** `make security-smoke` · `pytest tests/test_proof_pack_required.py tests/test_no_pii_in_logs.py -q --no-cov`

### 4. `dealix-engineer` — Product (Platform + QA hat)

- **Source:** [`.claude/agents/dealix-engineer.md`](../../.claude/agents/dealix-engineer.md) · [`.codex/agents/dealix-engineer.toml`](../../.codex/agents/dealix-engineer.toml)
- **Mission:** write Python, FastAPI routers, tests, migrations, and cron-style scripts — small safe PRs that reuse existing modules.
- **Permission level:** L2 (PR builder), L3 for CI/test repair. Staging deploy only; never production.
- **Inputs:** `api/`, `auto_client_acquisition/`, `core/`, `integrations/`, `tests/`, the canonical module layout.
- **Outputs:** code + tests + migrations + focused PRs; a report of files touched, tests run, doctrine guards verified.
- **Allowed:** add/extend code + tests, register routers following the existing pattern.
- **Forbidden:** rename modules, disable or bypass a guard test, deploy production, edit secrets.
- **Verify:** `make prod-verify` · quick regression bundle (see `AGENTS.md`)

### 5. `dealix-content` — Content

- **Source:** [`.claude/agents/dealix-content.md`](../../.claude/agents/dealix-content.md) · [`.codex/agents/dealix-content.toml`](../../.codex/agents/dealix-content.toml)
- **Mission:** write bilingual AR+EN docs, SOPs, case studies, proposal templates, LinkedIn posts, email templates, sector reports. No code, no tests.
- **Permission level:** L1 (docs only).
- **Inputs:** `docs/`, `templates/`, `data/templates/`.
- **Outputs:** markdown / Jinja2 templates, each ending with the bilingual disclaimer "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
- **Allowed:** create/extend docs and templates, reuse before writing.
- **Forbidden:** describe scraping/cold outreach as a service; promise numbers as fact; include PII in case studies; write code or tests.
- **Verify:** `make security-smoke` (claim-safety + PII guards run in the doctrine bundle).

---

## Mapping conceptual roles → real agents

The founder thinks in business roles. This table maps those "operating hats" to the
agents that actually wear them, so we add **zero** redundant agents.

| Conceptual role | Real agent(s) | Surface |
|---|---|---|
| Founder Command / daily priorities | `dealix-pm` | `.claude` / `.codex` |
| Revenue OS / prospects + offers | `dealix-sales` | `.claude` / `.codex` |
| Trust Guard / claims + PDPL + approvals | `dealix-delivery` + `governance_os` | execution plane |
| Product Platform / FastAPI + Next.js | `dealix-engineer` | `.claude` / `.codex` |
| QA / CI repair | `dealix-engineer` (L3 hat) | `.claude` / `.codex` |
| Delivery Ops / SOPs + Proof Pack | `dealix-delivery` | `.claude` / `.codex` |
| Market Research / sectors + competitors | `autonomous_growth/agents/` (market_research, competitor, sector_intel) | internal swarm |
| Content Factory | `dealix-content` | `.claude` / `.codex` |
| Token Optimizer | [`token-optimizer/`](../../token-optimizer/) + [`TOKEN_BUDGET_POLICY.md`](TOKEN_BUDGET_POLICY.md) | policy |
| PR Triage | `scripts/triage_open_prs.py` + [`PR_TRIAGE_POLICY.md`](PR_TRIAGE_POLICY.md) | tooling |
| Launch Operator | existing launch scripts (`founder_one_command.sh`, `verify_full_autonomous_ops_stack.py`) | runbook |
| External Integrations | `integrations/` + `dealix-engineer` (L2, no secret edits) | execution plane |

> **Discipline:** we do **not** add LangChain / LangGraph / CrewAI / AutoGen. The
> repo already has its own Decision / Execution / Trust / Data / Operating planes.
> The work is *registry → audit → runbook → metrics → triage → activation*, not
> *more frameworks → more agents → more chaos*.

---

## Adding or changing an agent (the rule)

1. Add the Claude definition in `.claude/agents/<name>.md` with frontmatter `name`,
   `description`, `tools`.
2. Mirror it in `.codex/agents/<name>.toml` (`description`, `developer_instructions`, `name`).
3. Add a row to the **Canonical sub-agents** section above (mission, level, I/O, verify).
4. Assign a permission level in [`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md).
5. Run `make agents-audit` — parity and frontmatter must pass.

No agent ships without identity (non-negotiable #9).

---

## Appendix — auditor prompt (paste into Claude Code / Codex)

```text
You are Dealix Agent Team Auditor.
First inspect: AGENTS.md, .claude/agents/, .codex/agents/, .cursor/rules/,
core/agents/, autonomous_growth/agents/, mcp_server/, token-optimizer/,
.github/workflows/, Makefile, README.md, docs/agents/, scripts/.
Goal: consolidate the existing ecosystem into one governable operating model.
Do not add frameworks. Preserve operational knowledge. Do not duplicate long docs.
Do not weaken security, change production config, enable live external sends, or merge to main.
Run: python scripts/audit_agent_team.py ; make doctor.
PR summary must include: agent inventory, gaps found, files added, verification
commands, remaining risk, next founder action.
```
