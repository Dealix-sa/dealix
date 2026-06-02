# Dealix Automation Permission Model · نموذج صلاحيات الأتمتة

> **القاعدة الواحدة:** أعطِ الوكلاء أقصى إنتاجية، ولا تعطهم "زر التدمير".
> **One rule:** give agents maximum productivity, never the destruct button.

This document is the **operating contract** for every automated actor in Dealix —
Claude Code, GitHub Actions, the FastAPI automation router, and any external
(n8n / Make / Zapier) workflow. It does **not** replace the doctrine; it layers a
**least-privilege ladder** on top of the runtime guards that already exist.

Anchored in:
- `docs/intelligence/AGENT_CONTROL_DOCTRINE.md` — every agent declares identity, owner, permissions, autonomy, tool access, allowed outputs, forbidden actions, audit, eval, decommission.
- `docs/00_constitution/NON_NEGOTIABLES.md` + the CI doctrine-guard tests (the **non-negotiables**).
- `auto_client_acquisition/governance_os/` — the **runtime** policy engine (`decide`, `is_forbidden`, `contains_unsafe_claim`).
- `AGENTS.md` — repo conventions ("small safe changes", "never enable auto external sends in any environment").

---

## 0) Two layers of enforcement · طبقتا الإنفاذ

Permissions here are **advisory intent**. They are enforced by two mechanisms that
already ship in the repo — this model only makes them explicit and assigns levels.

| Layer | Mechanism | Where |
| --- | --- | --- |
| **Build-time** | Doctrine-guard tests must pass in CI | `.github/workflows/ci.yml` → "Doctrine guard tests" |
| **Run-time** | `governance_os.decide(action, context)` / `is_forbidden(channel, mode)` / `contains_unsafe_claim(text)` | `auto_client_acquisition/governance_os/` |

> An automation that "has L4" still cannot send a cold WhatsApp message — the
> runtime gate refuses it regardless of level. **Level ≠ exemption from doctrine.**

---

## 1) The permission ladder (L0–L6) · سلّم الصلاحيات

| Level | Capability · الصلاحية | Real surfaces in this repo · الأسطح الحقيقية | Approval? · موافقة؟ |
| --- | --- | --- | --- |
| **L0** | Read / analyze / research · قراءة وتحليل | `Read`/`Grep`/`Glob`; `make help`, `make cockpit`, `make v5-status`, `make v5-digest`, `make doctor`, `python scripts/founder_*_status.py` | لا · No |
| **L1** | Write reports / docs / local ledgers · كتابة تقارير ووثائق | `docs/**`, `reports/**`, `data/founder_briefs/**`, `var/*.jsonl` (`DEALIX_*_PATH`) | لا · No |
| **L2** | Branch + Pull Request (no merge) · فرع و PR بدون دمج | `git checkout -b`, push branch, open PR against `main` | لا، لكن **بلا دمج** · No, but **no merge** |
| **L3** | Run CI / tests / re-run failed jobs · تشغيل الفحوص | `make lint`, `make type-check`, `make test`, `make security-smoke`, `make env-check`, `make prod-verify`; Actions re-run | لا · No |
| **L4** | Deploy to **staging** · نشر إلى staging | "Staging smoke" + Railway staging service | تلقائي بعد CI أو dispatch · Auto-after-CI or dispatch |
| **L5** | Deploy to **production** · نشر إلى الإنتاج | "Deploy to Production" (`deploy.yml`, `environment: production`) | **موافقة يدوية** · **Manual approval** |
| **L6** | Delete / secrets / force-push / destructive DB / disable CI / remove tests | — | **ممنوع افتراضيًا** · **Forbidden by default** |

### What each level explicitly includes

- **L0–L1** never touch git history, deploys, or external systems. Output is files.
- **L2** opens a PR; the PR is the unit of review. Agents **never** `git push` to `main`.
- **L3** runs the same checks CI runs. Agents **fix the root cause**, never weaken or skip a guard (`AGENTS.md`, `dealix-engineer` doctrine).
- **L4** is allowed only when CI is green. Staging is disposable.
- **L5** requires a human reviewer on the GitHub `production` Environment (already configured in `deploy.yml`).
- **L6** is the destruct button. Default = **no**. See §3.

---

## 2) Autonomy ladder ↔ agent autonomy levels · ربط السلّم بمستويات استقلالية الوكيل

The `agent-command` issue template and `dealix-agent.yml` workflow accept an
**autonomy** input. It maps 1:1 to the ladder:

| Autonomy input | Grants | Withholds |
| --- | --- | --- |
| `report_only` | L0–L1 | branches, PRs, deploys |
| `pr_only` *(default)* | L0–L3 | merge, deploy, secrets |
| `staging_allowed` | L0–L4 | production, merge, secrets |
| *(founder only — no input)* | L5–L6 | — |

> **Default everywhere is `pr_only`.** Raising autonomy is a deliberate founder act,
> recorded on the issue/PR and in `docs/governance/AI_RUN_LEDGER.md`.

---

## 3) The three rings · الحلقات الثلاث

### ✅ Allowed automatically · مسموح تلقائيًا (no approval)
- Read repo, run read-only diagnostics (`make cockpit`, `make doctor`, `*status*.py`).
- Generate reports, docs, sales **drafts**, playbooks, ops SOPs.
- Update local JSONL ledgers (`var/*.jsonl` via `DEALIX_*_PATH`).
- Create branches, open PRs.
- Run `make lint / type-check / test / security-smoke / env-check`.
- Deploy to **staging** after CI is green.
- **Queue** outreach drafts for founder approval (queue ≠ send).

### 🔶 Requires explicit founder approval · يتطلب موافقة صريحة
- Merge to `main`.
- Production deployment ("Deploy to Production", `environment: production`).
- Database migrations against production.
- Changing or rotating secrets (`scripts/rotate_secrets.sh` is founder-run).
- Deleting files; removing or skipping tests; weakening a doctrine guard.
- Changing authentication, payment logic, or customer-data workflows.
- **Any** external send to a customer (see next ring).

### ⛔ Forbidden · ممنوع (the non-negotiables)
These fail the build via the CI doctrine-guard tests and/or are refused at runtime
by `governance_os`. They are **never** unlocked by a permission level.

| # | Non-negotiable | Guard test |
| --- | --- | --- |
| 1 | No scraping engine | `tests/test_no_scraping_engine.py`, `tests/test_no_linkedin_scraper_string_anywhere.py` |
| 2 | No cold WhatsApp | `tests/test_no_cold_whatsapp.py` |
| 3 | No LinkedIn automation | `tests/test_no_linkedin_automation.py` |
| 4 | No guaranteed / fake claims | `tests/test_no_guaranteed_claims.py` |
| 5 | No AI action without a Source Passport | `tests/test_no_source_passport_no_ai.py` |
| 6 | No answer without a source | `tests/test_no_source_no_answer.py` |
| 7 | Every output carries a governance status | `tests/test_output_requires_governance_status.py` |
| 8 | Proof Pack required before upsell/claim | `tests/test_proof_pack_required.py` |
| 9 | No PII in logs | `tests/test_no_pii_in_logs.py` |
| 10 | PII leaving the system requires approval | `tests/test_pii_external_requires_approval.py` |
| 11 | Commercial doctrine guardrails | `tests/test_commercial_doctrine.py`, `tests/test_doctrine_guardrails.py` |

> **Master operational rule (`AGENTS.md`):** *never enable auto external sends in any
> environment.* Automation may **draft** and **queue**; a human releases the send.

Also forbidden for any automated actor: printing/echoing secrets, committing `.env`,
force-pushing `main`, disabling CI, skipping tests to go green, putting un-redacted
customer data into prompts.

---

## 4) Least-privilege GitHub Actions · أقل صلاحية في الـ workflows

Every workflow declares the **minimum** token scope. Patterns already used in-repo:

- Read-only by default: `permissions: { contents: read }` (see `ci.yml`).
- Agent / autopilot jobs that open PRs: `contents: write`, `pull-requests: write`,
  `issues: write`, `actions: read` — nothing more.
- Production deploy uses the GitHub `production` **Environment** (required reviewers),
  not a broad token.
- Prefer OIDC (`id-token: write`) over long-lived cloud keys where the provider supports it.

> Do not grant a workflow `contents: write` if it only reads. Do not add deploy
> permissions to a reporting job.

---

## 5) Every agent must declare a passport · بطاقة هوية لكل وكيل

Per `AGENT_CONTROL_DOCTRINE.md`, an automated actor is only legitimate if it declares:

| Field | Dealix source of truth |
| --- | --- |
| identity · owner | `docs/governance/AGENT_REGISTRY.md` |
| permissions · autonomy | this file (L0–L6) + the autonomy input |
| tool access · allowed outputs · forbidden actions | the agent's spec (`.claude/agents/*.md`) + §3 |
| audit | `docs/governance/AI_RUN_LEDGER.md`, `docs/ledgers/GOVERNANCE_LEDGER.md` |
| eval | doctrine-guard tests + `make prod-verify` |
| decommission | remove the workflow / revoke the secret / `docs/product/AGENT_LIFECYCLE_MANAGEMENT.md` |

---

## 6) Quick reference · مرجع سريع

```text
report_only   →  read + write docs/reports/ledgers
pr_only       →  + branch + PR + run tests        (DEFAULT)
staging_allowed → + deploy staging after green CI
founder only  →  merge · production · secrets · deletes · destructive DB
NEVER (any level): scraping · cold WhatsApp · LinkedIn automation · fake proof
                   · PII in logs · un-approved external send
```

**Related:** [`EXTERNAL_AUTOMATION_BLUEPRINT.md`](EXTERNAL_AUTOMATION_BLUEPRINT.md) ·
[`CLOUD_CODE_COMMAND_CENTER.md`](CLOUD_CODE_COMMAND_CENTER.md) ·
[`../intelligence/AGENT_CONTROL_DOCTRINE.md`](../intelligence/AGENT_CONTROL_DOCTRINE.md)
