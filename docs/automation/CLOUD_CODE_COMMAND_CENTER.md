# Dealix Cloud Code Command Center · مركز قيادة الوكلاء

> One place that tells the founder **how to command the automation** and how the
> automation is **kept on a leash**. مكان واحد: كيف تأمر الأتمتة، وكيف تبقى مضبوطة.

Read first: [`AUTOMATION_PERMISSION_MODEL.md`](AUTOMATION_PERMISSION_MODEL.md) (the L0–L6 ladder).

---

## 1) How to give a command · كيف تعطي أمرًا

There are exactly **three** founder-facing command surfaces. Each ends in a **PR you review** —
never a silent change to `main`, never an external send.

| Surface | Use it for | Lands at |
| --- | --- | --- |
| **GitHub Issue** (`agent-command` template) | a scoped mission with acceptance criteria | a draft PR |
| **`workflow_dispatch`** on `dealix-agent.yml` | run the agent now, manually, with an autonomy level | a draft PR |
| **Existing scheduled workflows** | the daily/weekly operating cadence (already wired) | reports + PRs |

> The Claude agent workflow (`dealix-agent.yml`) is **manual-dispatch only**. It does
> **not** auto-trigger on issue comments — a deliberate choice for a public repo
> (no paid agent runs from external `@mentions`). See §4.

### A. Command by Issue
1. New Issue → **"Dealix Agent Command"** template.
2. Fill: Area, Mission, **Autonomy** (`report_only` / `pr_only` / `staging_allowed`), Acceptance Criteria.
3. Trigger the run yourself: Actions → **Dealix Agent (manual)** → Run workflow → paste the issue number / mission.
4. Review the draft PR. Merge is **always** your hand (L5).

### B. Command by dispatch (fastest)
- Actions → **Dealix Agent (manual)** → Run workflow → set `mission` + `autonomy`.

---

## 2) The autonomy ladder in practice · سلّم الاستقلالية عمليًا

| Stage | What the agent may do | Autonomy input |
| --- | --- | --- |
| 1. Full PR automation | read, edit, branch, PR, run tests | `pr_only` *(default)* |
| 2. Auto-staging | + deploy staging after green CI | `staging_allowed` |
| 3. Auto-repair | open a fix PR when CI fails | `pr_only` (via Issue) |
| 4. Revenue prep | turn a new prospect into a **queued** outreach draft | `report_only` / `pr_only` |
| 5. Production w/ approval | prepare the release; **you** approve the Environment | founder only (L5) |
| 6. Controlled autopilot | only docs/reports/sales-draft PRs may be fast-merged; code & prod never | founder policy |

Start at stage 1. Climb only when each lower stage has been boring for a while.

---

## 3) The operating cadence (already wired) · الإيقاع التشغيلي القائم

The command center does **not** add new schedulers — it points at what runs today.

| When | Workflow / command | Output |
| --- | --- | --- |
| Daily AM | `make cockpit` · `scripts/dealix_founder_daily_brief.py` · `governed-full-ops-daily.yml` | founder brief + governed ops run |
| Daily | `founder_commercial_daily.yml` · `daily-revenue-machine.yml` | commercial run |
| Weekly | `founder_weekly_scorecard.yml` · `cto_weekly_anchor.yml` · `commercial-expand-weekly.yml` | scorecards + expansion |
| On PR | `ci.yml` (quality, tests, doctrine guards, coverage gate) · `security.yml` · CodeQL · Scorecard | green gate |
| On deploy | "Staging smoke" → "Deploy to Production" (`environment: production`) → "Production Smoke" | safe release |

Founder UI: `/[locale]/cloud` (command center) and `/[locale]/ops/founder` (90-min cockpit).

---

## 4) The manual agent workflow · الوكيل اليدوي

`.github/workflows/dealix-agent.yml`:
- **Trigger:** `workflow_dispatch` only. No `issues` / `issue_comment` triggers.
- **Secret:** requires `ANTHROPIC_API_KEY` (repo secret). A preflight step **no-ops gracefully** if the secret is absent — the workflow is inert until you opt in.
- **Permissions (least-privilege):** `contents: write`, `pull-requests: write`, `issues: write`, `actions: read`.
- **Operating rules baked into the prompt:** small safe changes; **PR only, never merge**; never deploy production; never touch secrets; never auto-send; run Python checks (`make lint`, `make test`, `make security-smoke`, doctrine guards) — **not** npm; every PR carries business impact, tests run, risk, rollback, next founder action.

> Enabling: add `ANTHROPIC_API_KEY` in repo Settings → Secrets, then dispatch the
> workflow. Until then it is documented but dormant — zero cost, zero attack surface.

---

## 5) The standing mission prompt · أمر التشغيل الثابت

Paste into the Issue mission or the dispatch input when you want the broad operating run:

```text
You are the Dealix automation agent. Autonomy: pr_only (unless raised).
Read AGENTS.md and docs/automation/ first. Increase revenue readiness, founder
leverage, and delivery capacity with small, safe, reviewable PRs.

Rules:
- Prefer PRs over direct main edits. Never merge. Never deploy production.
- Never print/commit secrets. Never delete important files. Never weaken auth,
  env validation, CI, tests, or a doctrine guard.
- Never auto-send to a customer — draft and queue only.
- Run: make lint · make type-check · make test · make security-smoke (Python, not npm).
- Honor the 11 non-negotiables (docs/automation/AUTOMATION_PERMISSION_MODEL.md §3).

Final PR must include: business impact · technical changes · files changed ·
tests run · risks · rollback · next founder action.
```

**Related:** [`AUTOMATION_PERMISSION_MODEL.md`](AUTOMATION_PERMISSION_MODEL.md) ·
[`EXTERNAL_AUTOMATION_BLUEPRINT.md`](EXTERNAL_AUTOMATION_BLUEPRINT.md) ·
[`../../.github/ISSUE_TEMPLATE/agent-command.yml`](../../.github/ISSUE_TEMPLATE/agent-command.yml)
