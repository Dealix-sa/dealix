# Dealix — Claude Code Operating Manual

## Identity

Dealix is a Saudi-first AI Business Transformation company. We build operating
systems (OS) for Saudi B2B companies: WhatsApp Revenue OS, Review Intelligence OS,
AI Business Command Center, Brand Intelligence OS, Growth Engine OS, Customer
Experience OS, AI Agent Workforce OS, and Custom Enterprise Systems.

Primary paid entry: **Transformation Diagnostic Sprint** — 7,500–25,000 SAR, 3–7 days.

---

## Development Rules (read before every session)

### PR Discipline
- One Wave per PR. Never merge multiple Waves in one PR.
- Branch naming: `feat/<wave-name>` (e.g., `feat/revenue-engine-v2`)
- All PRs start as **draft**. Never auto-merge.
- PR must include: what changed, validation output, what NOT to do next.

### Execution Constraints — MANDATORY
- **No Docker** — do not run `docker`, `docker-compose`, or `make` unless explicitly told.
- **No `npm run dev`** — never start the frontend dev server in a PR workflow.
- **No auto-send** — never send WhatsApp, email, or any external message.
- **No auto-invoicing** — never issue invoices or contracts automatically.
- **No secrets in commits** — never commit `.env`, API keys, or credentials.
- **No mega-pushes** — if a change touches more than 3 unrelated systems, split it.

### Generated File Policy
- All runtime output lives under `company/runtime/` — **gitignored**.
- Never commit: `*_REPORT.md` daily outputs, `*.csv` generated leads, `approval_queue*`.
- Templates and static docs: commit freely.

### Validation (safe commands only)
```bash
python --version
git status --short
bash -n scripts/<script>.sh          # syntax check only
python company/<module>/<script>.py  # dry-run python scripts
```

---

## Daily Operating Commands

```bash
# Morning CEO pack
./scripts/dealix_micro_day.sh

# After Wave 2 lands
./scripts/dealix_revenue_day.sh
./scripts/dealix_intake_day.sh

# After Wave 5+
./scripts/dealix_followup_day.sh
./scripts/dealix_trust_day.sh
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

**Rule**: Never start Wave N+1 before Wave N PR is merged.

---

## Approval Gates

These actions require explicit founder approval before execution:

- Sending any external message (WhatsApp, email, LinkedIn)
- Issuing a proposal or invoice
- Merging a PR to `main`
- Rotating secrets or changing Railway config
- Publishing website changes to production

---

## Business Model Summary

See `docs/DEALIX_BUSINESS_MODEL.md` for full detail.

**Offer ladder:**
1. Free Diagnostic (lead magnet, 30 min)
2. Micro Sprint — 499 SAR (quick win proof)
3. Data Pack — 1,500 SAR (one-time data asset)
4. Managed Ops — 2,999–4,999 SAR/month
5. Transformation Diagnostic Sprint — 7,500–25,000 SAR
6. Custom Enterprise System — 25,000–100,000+ SAR

---

## Key File Locations

| Purpose | Path |
|---------|------|
| Micro daily script | `scripts/dealix_micro_day.sh` |
| Micro master engine | `company/micro/micro_master.py` |
| Lead research | `company/lead_research/` |
| CRM | `company/crm/` |
| Outbox | `company/outbox/` |
| Daily reports | `company/reports/` |
| Runtime outputs | `company/runtime/` (gitignored) |
| CEO context | `docs/CEO_OPERATING_CONTEXT.md` |
| Business model | `docs/DEALIX_BUSINESS_MODEL.md` |
| Safe execution rules | `docs/DEALIX_SAFE_EXECUTION_RULES.md` |

---

## What NOT to Do

- Do not rebuild from scratch — the repo already has Company OS, Founder OS, Micro OS.
- Do not run `dealix_micro_day.sh` inside a PR workflow validation step.
- Do not create `.github/workflows` that auto-run Docker or npm build.
- Do not create giant "all-in-one" scripts.
- Do not assume `company/runtime/` files exist — always create with fallbacks.
