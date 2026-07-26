# Dealix — Claude Code Operating Manual

## Identity

Dealix is a Saudi-first AI Business Operating Systems company.
We build command-room OS products for Saudi B2B companies:

- Revenue Command Room OS
- Company Brain OS
- WhatsApp / Inbox Follow-up OS
- AI Outreach & Targeting OS
- Client Growth Operator OS
- AI Trust & Compliance OS
- Client Delivery OS
- Controlled Live Outbound OS (draft-only default)
- Founder Decision Desk
- Proposal / Contract / Payment OS
- Executive Proof Pack OS
- Offer Intelligence OS
- Market & Competitor Watch OS
- Customer Pain Radar
- Operations Bottleneck Scanner
- Loop Operating System
- Agentic Command Room OS
- Data Intelligence OS
- MCP Gateway
- SaaS / Tenant Foundation OS

**Primary paid entry:** Transformation Diagnostic Sprint — 7,500–25,000 SAR, 3–7 days.

---

## Architecture Summary

```
api/          FastAPI app + routers (uvicorn api.main:app)
core/         Settings, logging, errors, DB, LLM base
db/           Async SQLAlchemy + Alembic migrations
dealix/       Hermes multi-agent framework + observability
company/      Daily OS engines (micro, CRM, reports, outbox)
scripts/      CLI tools, ops checks, daily shell scripts
scripts/ops/  CI, Railway checks, security smoke
apps/web/     Next.js command room frontend (npm --prefix apps/web)
docs/ops/     Runbooks, checklists, deployment guides
sales/        Sales assets, proposals, playbooks
reports/      Runtime outputs (gitignored under reports/runtime/)
```

Key files:
- `api/main.py` — app factory; production secret guard at startup
- `core/config/settings.py` — pydantic-settings; no hardcoded secrets
- `railway.toml` — Dockerfile builder, uvicorn start, /healthz
- `Dockerfile` — multi-stage Python 3.12-slim, non-root, tini
- `Makefile` — all canonical commands
- `scripts/ops/run_full_repo_test_matrix.sh` — launch gate runner

---

## Outbound Safety Policy — NON-NEGOTIABLE

These env vars **must remain false** unless a controlled-live approval PR exists:

```
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

**Allowed:** generate drafts, proposals, WhatsApp payload drafts, email drafts, approval cards, command room reports, proof packs, audit logs, classification results.

**Forbidden:** automatic WhatsApp/SMS/email sending, cold outbound without opt-in, LinkedIn automation/scraping, sending without human approval.

---

## Secrets Policy — NON-NEGOTIABLE

- Never commit `.env`, API keys, tokens, or credential values.
- Never print secret values in logs, tests, markdown, or PRs.
- Never commit `.secrets.baseline` with actual secrets.
- Generate secrets locally; paste only into Railway/GitHub Secrets UI.

---

## Execution Constraints — MANDATORY

- **No Docker** — do not run `docker`, `docker-compose`, or `make` unless explicitly told.
- **No `npm run dev`** — never start the frontend dev server in a PR workflow.
- **No auto-send** — never send WhatsApp, email, or any external message.
- **No auto-invoicing** — never issue invoices or contracts automatically.
- **No secrets in commits** — never commit `.env`, API keys, or credentials.
- **No mega-pushes** — if a change touches more than 3 unrelated systems, split it.
- **No fake data** — no fake customers, logos, testimonials, or guaranteed ROI claims.

---

## Verification Commands (safe, always allowed)

```bash
python3 --version
git status --short
git log --oneline -10
bash -n scripts/<script>.sh                         # syntax only
python3 scripts/ops/check_railway_production_env.py # prints names, never values
python3 scripts/ops/security_smoke_ci.py
python3 scripts/verify_no_auto_external_send.py
python3 scripts/verify_company_launch_ready.py
make full-repo-test                                 # full launch gate
npm --prefix apps/web run verify                    # frontend typecheck+build
```

---

## Test Matrix

Run: `make full-repo-test`

Required gates (must all pass):
- `python-version`
- `python-compileall-core-surfaces`
- `env-contract`
- `security-smoke` (CI-safe, no secrets)
- `no-auto-external-send`
- `company-launch-ready`
- `pytest-launch-critical-suite` (tests/test_full_repo_matrix_contract.py + tests/test_growth_sales_cards.py)
- `apps-web-npm-ci`
- `apps-web-verify`

Optional/diagnostic (failures are non-blocking):
- `pytest-full-suite-diagnostic`
- `launch-os-dry-runs`
- `production-verify-bundle`
- `testsprite-env-check`
- `testsprite-mcp-smoke`

**Current status:** PASS (as of 2026-06-30)

---

## Railway Deployment Rules

- `railway.toml` builder = DOCKERFILE, start = uvicorn api.main:app
- Dockerfile = multi-stage Python 3.12-slim, non-root, tini
- Health = `/healthz`, timeout = 300s
- **Do not remove the production secret guard** in `api/main.py:_validate_production_secrets`
- If Railway fails: fix billing, source, and env vars — not the security guard
- Required Railway variables: see `docs/ops/RAILWAY_GO_LIVE_CHECKLIST.md`
- Full recovery procedure: see `docs/ops/RAILWAY_RECOVERY_RUNBOOK.md`
- Generate secrets locally: `python -c "import secrets; print(secrets.token_hex(32))"`
- Validate: `make railway-env-check`

---

## GitHub / CI Rules

- Required CI: `.github/workflows/full-repo-test-matrix.yml`
- All PRs start as **draft** — never auto-merge
- Branch naming: `feat/<wave-name>` or `claude/<slug>` for agent branches
- One Wave per PR — never merge multiple Waves in one PR
- Never create workflows that run Docker or npm dev server
- Never commit generated reports, runtime CSVs, or approval queues
- PR must include: what changed, validation output, what NOT to do next
- Allowed: docs, scripts, schema, templates, static assets

---

## Generated File Policy

- Runtime output: `company/runtime/` — gitignored
- Never commit: `*_REPORT.md` daily outputs, `*.csv` generated leads, `approval_queue*`
- Never commit: `reports/runtime/` contents
- Templates and static docs: commit freely

---

## Daily Operating Commands

```bash
bash scripts/dealix_command_day.sh   # all engines + Command Room → reports/command_room/index.html
./scripts/dealix_micro_day.sh        # morning CEO pack
./scripts/dealix_revenue_day.sh      # after Wave 2 lands
./scripts/dealix_intake_day.sh       # after Wave 2 lands
./scripts/dealix_followup_day.sh     # after Wave 5+
./scripts/dealix_trust_day.sh        # after Wave 5+
```

---

## Wave Roadmap

| Wave | Branch | Purpose |
|------|--------|---------|
| 1 | `feat/ceo-operating-context` | CLAUDE.md + CEO context docs |
| 2 | `feat/revenue-engine-v2` | Daily commercial pack generation |
| 3 | `feat/intake-presentation-os` | Client intake + presentation engine |
| 4 | `feat/website-conversion-upgrade` | Website conversion pages |
| 5 | `feat/crm-followup-os` | CRM + follow-up cadence |
| 6 | `feat/client-delivery-os` | Client delivery + Diagnostic Sprint OS |
| 7 | `feat/trust-launch-os` | Trust pack + launch readiness |

**Rule:** Never start Wave N+1 before Wave N PR is merged.

---

## Approval Gates

Require explicit founder (Sami Assiri) approval before execution:

- Sending any external message (WhatsApp, email, LinkedIn)
- Issuing a proposal or invoice
- Merging a PR to `main`
- Rotating secrets or changing Railway config
- Publishing website changes to production
- Enabling live outbound (any channel)

---

## Business Model Summary

| # | Offer | Price |
|---|-------|-------|
| 1 | Free Diagnostic | Free |
| 2 | Micro Sprint | 499 SAR |
| 3 | Data Pack | 1,500 SAR |
| 4 | Managed Ops | 2,999–4,999 SAR/mo |
| 5 | Transformation Diagnostic Sprint | 7,500–25,000 SAR |
| 6 | Custom Enterprise System | 25,000–100,000+ SAR |

See `docs/DEALIX_BUSINESS_MODEL.md` for full detail.

---

## Key File Locations

| Purpose | Path |
|---------|------|
| App entry point | `api/main.py` |
| Settings | `core/config/settings.py` |
| Railway config | `railway.toml` |
| Docker build | `Dockerfile` |
| Full test matrix | `scripts/ops/run_full_repo_test_matrix.sh` |
| Railway env check | `scripts/ops/check_railway_production_env.py` |
| Railway go-live | `docs/ops/RAILWAY_GO_LIVE_CHECKLIST.md` |
| Railway recovery | `docs/ops/RAILWAY_RECOVERY_RUNBOOK.md` |
| Micro daily script | `scripts/dealix_micro_day.sh` |
| Lead research | `company/lead_research/` |
| CRM | `company/crm/` |
| Outbox | `company/outbox/` |
| Runtime outputs | `company/runtime/` (gitignored) |
| CEO context | `docs/CEO_OPERATING_CONTEXT.md` |
| Business model | `docs/DEALIX_BUSINESS_MODEL.md` |
| Safe execution | `docs/DEALIX_SAFE_EXECUTION_RULES.md` |
| Sales assets | `sales/` |
| Agent rules | `.claude/rules/` |
| Codebase advisor skill | `.claude/skills/improve/` |
| improve executor agent | `.claude/agents/improve-executor.md` |
| Improvement backlog | `plans/` (INDEX + seeded plans) |
| Provider registry guard | `scripts/ops/check_provider_registry_freshness.py` |
| improve outbound bridge (draft-only) | `auto_client_acquisition/gtm_os/improve_followup.py` |
| Diagnostic report template | `sales/DIAGNOSTIC_REPORT_TEMPLATE_AR.md` |
| improve delivery SOP (AR) | `sales/IMPROVE_DIAGNOSTIC_DELIVERY_SOP_AR.md` |
| improve commercial playbook | `docs/IMPROVE_COMMERCIAL_PLAYBOOK.md` |
| improve integration doc | `docs/IMPROVE_SKILL_INTEGRATION.md` |

---

## Codebase Advisor Skill (`improve`)

`.claude/skills/improve/` — adapted from `shadcn/improve` (MIT). Run `/improve`
(or `/improve quick`, `/improve branch`, `/improve <category>`) to audit the repo
and produce **executable plans** in `plans/`. It uses the expensive model to
advise and hands execution to a cheap executor (via the free-LLM provider radar)
in a disposable worktree. It **never edits source, never mutates the tree, never
weakens a guard** — the only writes go to `plans/`, and merging stays a founder
approval gate. Doubles as the delivery engine for the Free Diagnostic and
Transformation Diagnostic Sprint offers — see `docs/IMPROVE_SKILL_INTEGRATION.md`.

---

## Known Launch Status (2026-06-30)

- **Repo matrix:** PASS (all required gates green)
- **Railway:** Billing past due — founder must pay to redeploy
- **Frontend:** `npm --prefix apps/web run verify` PASS
- **Production API:** Not yet live (Railway billing issue)
- **Live outbound:** DISABLED (draft-only default)
- **Secrets in repo:** NONE confirmed

---

## What NOT to Do

- Do not rebuild from scratch — the repo already has Company OS, Founder OS, Micro OS.
- Do not run `dealix_micro_day.sh` inside a PR workflow validation step.
- Do not create `.github/workflows` that auto-run Docker or npm dev server.
- Do not create giant "all-in-one" scripts.
- Do not assume `company/runtime/` files exist — always create with fallbacks.
- Do not weaken security to make Railway boot. Fix Railway configuration instead.
- Do not claim features not yet implemented.
- Do not generate fake ROI numbers, fake clients, or fake testimonials.
