# CLAUDE.md — Dealix Operating Constitution

> This file is **context, not a lock.** It tells every Claude Code session what Dealix is, what it is not, and how to work here. Hard enforcement lives in CI gates (`/.github/workflows/dealix-launch-gates.yml`, planned in PR 7), not in this file. When in doubt, this file + `docs/00_platform_truth/MODULE_STATUS_MAP.md` are the source of truth.

## 1. What Dealix is

Dealix is a **Saudi-first AI Business Operating System**. It helps companies turn scattered WhatsApp, Excel, meetings, offers, follow-ups, delivery, client memory, support, finance, data, governance, and executive decisions into one operating rhythm that answers five questions:

1. What is happening?
2. What should happen next?
3. Who approves?
4. What is the evidence?
5. What is the next action?

## 2. What Dealix is NOT

Never describe or build Dealix as any of these: CRM · chatbot · WhatsApp bot · marketing agency · generic AI tool · "only Revenue OS" · "only a targeting engine". Revenue is **one wedge** inside the Business OS, not the whole company.

## 3. First sellable wedge — Command Sprint

**Command Sprint** is the first paid offer. It is the **rebrand of the existing live 499 SAR "7-Day Revenue Proof Sprint"** — same price, same 7-day delivery, repackaged with eight components: Market Intelligence Lite · Revenue Map · Proof Register · Executive Command Brief · Approval Register · Next Action Board · Delivery Lite · Upsell Recommendation. It is **not** a new ladder rung.

## 4. The offer ladder (canonical)

Source of truth: `docs/OFFER_LADDER_AND_PRICING.md`. Six rungs:

| Rung | Offer | Price | Status |
|------|-------|-------|--------|
| 0 | Free AI Ops Diagnostic | Free | LIVE |
| 1 | **Command Sprint** (was 7-Day Revenue Proof Sprint) | 499 SAR | LIVE |
| 2 | Data-to-Revenue Pack | 1,500 SAR | LIVE (founder-assisted) |
| 3 | Managed Revenue Ops | 2,999–4,999 SAR/mo | BETA (founder-assisted — disclose) |
| 4 | Executive Command Center | 7,500–15,000 SAR/mo | BETA (founder-assisted — disclose) |
| 5 | Agency Partner OS | Custom + rev-share | BETA (founder-assisted — disclose) |

Rungs 3–5 are **founder-assisted / semi-automated today** and must never be sold as fully managed/automated. Always surface that disclosure.

## 5. The 14 OS modules

`Command OS · Market Intelligence OS · Revenue OS · Proof OS · Delivery OS · Client OS · Support OS · Finance OS · Data OS · Governance OS · Knowledge OS · Agent OS · Partner OS · Academy OS`. The live spine today is **Revenue / Proof / Command / Governance**; everything else is BETA/FUTURE. Every module's status is governed by `docs/00_platform_truth/MODULE_STATUS_MAP.md`. **Never present a FUTURE module as live.**

## 6. Hard rules (non-negotiable)

- No guaranteed-revenue claims (no "نضمن" / "guaranteed" + revenue numbers).
- No fake proof, no fabricated metrics, no fake scarcity.
- No auto-send. No cold WhatsApp automation. No LinkedIn automation. No scraping behind login.
- No public customer names or case studies without written approval.
- No customer-facing external action without founder approval.
- No future module presented as live.
- Every external claim must be evidence-backed, framed as a hypothesis, or rewritten safely.
- Every website page has **exactly one** main CTA.
- Every growth asset routes to exactly one of: **Business OS Score**, **Diagnostic**, or **Command Sprint**.
- PDPL status is **PARTIAL** today (no DPO yet, retention defined but not DB-enforced). Do not claim "PDPL-native/complete."

These align with the repo's existing doctrine (`docs/governance/FORBIDDEN_ACTIONS.md`, `docs/governance/TRUST_SAFETY_CHARTER.md`, `dealix/registers/no_overclaim.yaml`). Those registers remain authoritative.

## 7. How to work here (workflow)

**Plan → Approve → PR → Verify → Approve → next PR.** One PR at a time. Never jump to code before a plan is approved. Every PR begins with the Execution Contract (`.claude/commands/verify-launch.md` references it) and ends by showing changed files, running verification, `git diff --stat`, reporting blockers, recommending the next PR, and **waiting for founder approval**.

## 8. Repo map (essentials)

- Website: `frontend/` — Next.js 15 + React 19, next-intl (`ar`/`en`), Tailwind, real RTL. Design tokens: `frontend/src/styles/dealix-system.css`, `dealix-brand.css`. Scripts: `npm run dev|build|start|lint|typecheck` (**no `test`**).
- A second app `apps/web/` exists and is **out of scope** for the launch website work.
- Backend: Python FastAPI (`api/`, `core/`, `dealix/`), pytest, `Makefile` targets (`env-check`, `security-smoke`, `prod-verify`, `v5-*`), `scripts/*.py`.
- Truth layer (created by the launch): `docs/00_platform_truth/`.
- Governance (existing, authoritative): `docs/governance/`, `dealix/registers/*.yaml`.
- Agent guide (existing): `AGENTS.md`.

## 9. Verification commands (real)

```
cd frontend && npm ci && npm run lint && npm run typecheck && npm run build
make env-check
python scripts/security_smoke.py
make prod-verify            # after: make install-dev
# launch gates (created in PR 7):
python scripts/verify_website_positioning.py
python scripts/verify_growth_assets.py
python scripts/verify_launch_readiness.py
```

There is **no `npm run test`** — JS verification is build + lint + typecheck; Python tests run via pytest / `make test`.

## 10. Launch agents

The launch team lives in `.claude/agents/`: `founder-ceo-operator`, `brand-director`, `visual-identity-designer`, `website-architect`, `growth-strategist`, `seo-geo-agent`, `conversion-specialist`, `proof-governance-reviewer`, `delivery-architect`, `qa-verifier`. They coordinate with the existing execution agents (`dealix-engineer`, `dealix-delivery`, `dealix-sales`, `dealix-pm`, `dealix-content`). Use agents by phase — not all agents on everything (see `docs/00_platform_truth/LAUNCH_CONTROL_TOWER.md`).
