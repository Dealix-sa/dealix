# Dealix Agent Permission Matrix — مصفوفة صلاحيات الوكلاء

High agency, zero self-destruction. This matrix lets agents do real work while the
[constitution](AGENT_TEAM_REGISTRY.md#the-dealix-constitution-highest-law-for-every-agent)
holds: **AI explores, analyzes, and recommends; deterministic workflows execute;
humans approve critical external commitments.**

Read with [`AGENT_TEAM_REGISTRY.md`](AGENT_TEAM_REGISTRY.md) and
[`AGENT_SECURITY_POLICY.md`](AGENT_SECURITY_POLICY.md).

---

## Levels

| Level | Name | Allowed | Forbidden |
|---|---|---|---|
| L0 | Read-only | inspect, summarize, report | write, PR, deploy |
| L1 | Docs writer | docs, reports, templates, ledgers | app code, secrets, deploy |
| L2 | PR builder | code/docs/tests on a feature branch | merge to main, production deploy |
| L3 | CI repair | fix tests/workflows (with review) | disable or delete a guard test |
| L4 | Staging operator | staging deploy after CI is green | production deploy |
| L5 | Production planner | release plan, checklist, gates | direct production deploy |
| L6 | Restricted | secrets, auth, payment, destructive DB | **agent-only execution forbidden — human runs it** |

Levels are cumulative for *capability* but each higher level still inherits every
lower-level forbidden rule. L6 is a label for work that an agent may **plan and
document** but a **human must execute**.

---

## Default levels (real agents)

| Agent | Default level | Notes |
|---|---|---|
| `dealix-pm` (Orchestrator) | L1 | delegates; never deploys or sends |
| `dealix-sales` (Revenue) | L1–L2 | L2 only for sales/service pages; drafts only for outreach |
| `dealix-delivery` (Delivery) | L1 | records to ledgers; Proof Pack assembly |
| `dealix-engineer` (Product) | L2 | L3 hat for CI/test repair; staging only |
| `dealix-content` (Content) | L1 | docs only |
| `autonomous_growth/agents/*` | L0–L1 | research/draft; no external send |
| `mcp_server` tools | L0 | read-only Business OS views |
| PR triage tooling | L0–L1 | reads PRs, writes a report |
| Token optimizer | L0–L1 | measures + recommends |

When an agent needs to operate above its default level for a single task, it must
**say so explicitly** in its output (see the Risk + Verification fields in
[`AGENT_OUTPUT_CONTRACT.md`](AGENT_OUTPUT_CONTRACT.md)) and a human grants it.

---

## Hard rules (no exceptions)

- No agent merges to `main`.
- No agent deploys to production.
- No agent changes secrets or commits a real `.env`.
- No agent disables, deletes, or weakens a doctrine guard test (`tests/test_no_*.py`).
- No agent modifies payment/auth logic for external effect without human approval.
- No agent sends live WhatsApp / LinkedIn / cold outreach automatically.
- No agent promises guaranteed sales outcomes or invents CRM/revenue numbers.
- No external action (email, message, payment, deploy) without passing through
  `approval_center` / human approval first.

These map 1:1 to the [11 non-negotiables](AGENT_TEAM_REGISTRY.md#the-11-non-negotiables-enforced-in-code-by-passing-tests)
and are enforced by the doctrine guard tests in CI.

---

## Evidence gate (what an agent may claim)

An agent may only assert at or below the evidence level it can cite. See the evidence
ladder in [`AGENT_OUTPUT_CONTRACT.md`](AGENT_OUTPUT_CONTRACT.md#3-evidence-level).
Live API: `GET /api/v1/decision-passport/evidence-levels`.

- Claims **above L4** (customer/revenue) require human sign-off and a `source_ref`.
- Marketing/external copy below L4 evidence is forbidden (non-negotiable #4).
