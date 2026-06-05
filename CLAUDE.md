# CLAUDE.md — Dealix Company OS

> This file is the operating constitution for any Claude Code session in this repo.
> It tells Claude **who Dealix is**, **what is safe**, **how to work**, and **how to verify**.
> It does **not** replace the canonical doctrine — it points to it and enforces it.

## How this repo is governed (read order)

1. **`CLAUDE.md`** (this file) — session constitution + working method.
2. **`AGENTS.md`** — repo anatomy, local dev commands, resolved issues (do not re-diagnose).
3. **`docs/00_constitution/`** — canonical doctrine:
   - `DEALIX_CONSTITUTION.md`, `DEALIX_LAWS.md`, `NON_NEGOTIABLES.md`,
     `WHAT_DEALIX_REFUSES.md`, `GOOD_REVENUE_BAD_REVENUE.md`, `OPERATING_EQUATION.md`.
4. **`docs/00_foundation/`** — parallel numbered constitution (positioning, wedge, refusals).
5. **`docs/00_platform_truth/`** — brand / visual / messaging / product-family / module-status (Company OS layer).

If this file and the canonical constitution ever disagree, **the canonical constitution wins** and this file must be corrected.

---

## Identity

Dealix is a **Saudi-first AI Business Operating System** company.

Dealix is **not**:
- a CRM
- a chatbot
- a marketing agency
- a WhatsApp bot
- a generic AI tool
- "only Revenue OS"

Dealix turns scattered WhatsApp, Excel, meetings, offers, follow-ups, delivery, client memory,
finance, data, governance, and executive decisions into **one governed operating rhythm**:

- What is happening?
- What should happen next?
- Who approves?
- What is the evidence?
- What is the next action?

## First commercial wedge

The first sellable offer is the **Dealix Command Sprint**. It includes:

- Market Intelligence Lite
- Revenue Map
- Proof Register
- Executive Command Brief
- Approval Register
- Next Action Board
- Delivery Lite
- Upsell Recommendation

> The Command Sprint sits at the top of the existing five-rung commercial ladder
> (Free Diagnostic → Sprint → Data Pack → Managed Ops → Custom AI). See
> `docs/01_go_to_market/COMMERCIAL_LADDER.md`.

## Core operating systems

1. Command OS · 2. Market Intelligence OS · 3. Revenue OS · 4. Proof OS ·
5. Delivery OS · 6. Client OS · 7. Support OS · 8. Finance OS · 9. Data OS ·
10. Governance OS · 11. Knowledge OS · 12. Agent OS · 13. Partner OS · 14. Academy OS

Each system has a **status label** (see below). Never present a `FUTURE` or `DOCS_ONLY` system as `LIVE`.

---

## Hard rules (non-negotiable)

These mirror `docs/00_constitution/NON_NEGOTIABLES.md` and `WHAT_DEALIX_REFUSES.md`.

**Never:**
- guarantee revenue or specific financial outcomes
- create or imply fake proof, fake testimonials, or fake scarcity
- enable auto-send of any external message in any environment
- enable cold WhatsApp / LinkedIn automation
- scrape behind login or scrape personal data
- publish a customer name, logo, or quote without written approval
- use customer data for model training
- create any customer-facing external action without founder approval
- present a future / beta / docs-only module as live
- make a public claim without evidence

**Every external-facing claim must be one of:**
- evidence-backed (linked to a Proof Pack / Claims Register entry), **or**
- explicitly framed as a hypothesis, **or**
- rewritten safely.

**Every page must have exactly one primary CTA**, chosen from:
- Get Business OS Score
- Book Diagnostic
- Start Command Sprint

## Module status labels

Use exactly one per module/feature/page claim:

`LIVE` · `BETA` · `INTERNAL` · `DOCS_ONLY` · `BLOCKED` · `FUTURE` · `DEPRECATED`

Source of truth: `docs/00_platform_truth/MODULE_STATUS_MAP.md`.

---

## Website direction

The website surfaces are:
- **`landing/`** — static HTML/CSS/JS public pages.
- **`frontend/`** — Next.js dashboard + public funnel (`/[locale]` routes, RTL via `next-intl`).

The website must feel: premium · Saudi/GCC enterprise · executive · clean · dark · high-contrast ·
Arabic-first · English-ready · serious (not playful) · operating-system style (not generic SaaS).

Avoid: childish AI gradients · vague AI claims · clutter · multiple competing CTAs ·
generic startup language · overpromising.

> **Do not** start a from-scratch website rewrite. Improve the existing `frontend/` and `landing/`
> surfaces incrementally. Map intent to the real routes — there is no root `npm run build`;
> the build lives in `frontend/`.

## Growth direction

Growth is built on loops, not blasts: free tools · sector pages · founder-led content ·
SEO/GEO · proof-to-content loop · partner distribution · referral · academy-as-marketing ·
nurture sequences · conversion experiments.

Every growth asset must route to exactly one of: **Business OS Score · Diagnostic · Command Sprint**.

No spam. No fake scarcity. No fake testimonials. No external publishing without founder approval.

---

## Required verification

This repo's real gates (see `Makefile`):

```bash
# Frontend (website) — build lives in frontend/, not root
cd frontend && npm ci && npm run build && npm run lint && npm run typecheck

# Backend / platform gates
make env-check                       # validate .env contract
make security-smoke                  # dependency-free security smoke (scripts/security_smoke.py)
make prod-verify                     # canonical production-readiness bundle

# Company OS positioning gate (new)
python scripts/verify_website_positioning.py
```

If a command fails: **do not hide it.** Quote the exact failing command, summarize the likely
root cause, and propose the next fix. Never mark a launch ready while a gate is red.

## Working method (for large changes)

1. **Explore** — read before writing; respect resolved issues in `AGENTS.md`.
2. **Audit** — `/dealix-audit` (no edits).
3. **Plan** — small, reviewable steps.
4. **Implement** — incremental; no uncontrolled rewrites.
5. **Verify** — run the gates above.
6. **Report** — files changed + why + what's sellable now vs future + gate results + blockers.
7. **Commit** — only after verification passes or a blocker is documented.

## The Claude Company OS (team, skills, commands)

- **Agents** (`.claude/agents/`): the existing delivery/sales/content/engineer/pm agents, plus the
  launch team — `brand-director`, `visual-identity-designer`, `website-architect`,
  `growth-strategist`, `seo-geo-agent`, `conversion-specialist`, `proof-governance-reviewer`, `qa-verifier`.
- **Skills** (`.claude/skills/`): `dealix-brand`, `dealix-website`, `dealix-growth`,
  `dealix-governance`, `dealix-delivery`, `dealix-verification`.
- **Commands** (`.claude/commands/`): `/dealix-audit`, `/dealix-brand`, `/dealix-build-website`,
  `/dealix-growth-os`, `/dealix-verify`.

Run order for a launch pass: `/dealix-audit` → `/dealix-brand` → `/dealix-build-website` →
`/dealix-growth-os` → `/dealix-verify`.
