# CLAUDE.md — Dealix Operating Context for Claude Code

> Single source of truth for autonomous editors operating inside this
> repository. Read first, every session.

---

## 1. Dealix Identity

- **Wordmark:** DEALIX
- **Tagline:** INTELLIGENT DEALS. REAL GROWTH.
- **Positioning:** Dealix is a **Saudi B2B Revenue Operating System** —
  intelligent deal flow, founder-approved growth, and trust-gated AI
  execution.
- **Brand pillars:** Built on Trust · Driven by Growth · Closing Deals ·
  Focused on Results · Global Mindset, Local Impact.
- **Brand tokens:** [`docs/brand/brand-tokens.json`](docs/brand/brand-tokens.json)
  and the TypeScript mirror at
  [`apps/web/lib/brand-tokens.ts`](apps/web/lib/brand-tokens.ts).

## 2. Architecture Overview

| Layer                   | Path                                         |
|-------------------------|----------------------------------------------|
| Founder Console UI      | `apps/web/` (Next.js 15, App Router)         |
| Brand components        | `apps/web/components/brand/`                 |
| Founder shell           | `apps/web/components/founder-shell.tsx`      |
| Internal runtime client | `apps/web/lib/dealix-runtime.ts`             |
| Action client           | `apps/web/lib/dealix-actions.ts`             |
| Internal API            | `api/routers/founder_console_internal.py`    |
| Auth / runtime / policy | `api/internal/`                              |
| Policy-as-code          | `policies/dealix_control_policy.yaml`        |
| Agent registry          | `registries/agent_registry.yaml`             |
| Eval gate               | `evals/gates/dealix_agent_eval_gate.yaml`    |
| Private ops runtime     | external — default `/opt/dealix-ops-private` |
| Verifiers               | `scripts/verify_*.py`                        |
| Workers                 | `scripts/run_*.py`                           |

## 3. Brand Identity

- Colors: Deep Navy `#0B1220`, Slate `#0F1726`, Emerald Teal `#00D1A1`,
  Soft Silver `#B2BBC6`, White `#FFFFFF`.
- Use the Founder Shell on every internal page. Existing pages
  (`/control-plane`, `/agents`, `/approvals`, `/safety`, `/sandbox`,
  `/value-engine`, `/self-evolving`) are preserved as-is — wrap them in
  the shell only when they are next modified.

## 4. Never-Auto-Execute List

These actions are **NEVER** automatic, even from agents with maximal
approval class. The Founder Console queues / drafts / records intent;
nothing leaves the system without a human approval.

1. External sending (email, LinkedIn, contact form, WhatsApp, etc.)
2. Proof publication (case study, screenshot, customer name).
3. Pricing / discount / contract / refund / payment-term commitments.
4. Customer data export.
5. Destructive operations (force-push, drop, mass-delete, mass-update).
6. Any new domain / DNS / payment provider change.
7. Promising guaranteed revenue, sales, or meetings to anyone.

## 5. Required Checks (before any PR merges)

- `python scripts/verify_company_os.py` (composite)
- `python scripts/verify_brand_system.py`
- `python scripts/verify_policy_as_code.py`
- `python scripts/verify_agent_registry.py`
- `python scripts/verify_eval_gate.py`
- `python scripts/verify_prompt_output_quality.py`
- `python scripts/smoke_internal_api.py`

GitHub Actions:

- `.github/workflows/dealix-brand-growth-operating-layer.yml`
- `.github/workflows/dealix-sovereign-operating-stack.yml`
- `.github/workflows/dealix-market-entry-stack.yml`
- `.github/workflows/dealix-company-os.yml`

## 6. Private Ops Rule

Operational state (approvals, suppression list, conversation logs,
finance, trust flags, audit decisions, …) lives in the **private ops
runtime**, never in this repository. Default path:
`/opt/dealix-ops-private` (or `$PRIVATE_OPS`).

Bootstrap:

```bash
make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private
```

Contract: [`docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`](docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md).

## 7. No Fake Production Readiness Rule

Do not mark anything as “production-ready” in code, docs, or commits
unless the relevant verifier reports `PASS` and a human has signed off.
The four pillars of the operating scorecard (Revenue, Trust, Delivery,
Growth) start at `unknown` and only move when evidence exists.

## 8. No Guaranteed Claims Rule

Drafts (proposals, samples, marketing, outbound) **must not** include
language such as “guaranteed revenue”, “100% conversions”, or
“promised meetings”. The eval gate enforces this; the prompt-output
verifier scans the repo for violations.

## 9. Internal API Safety Rule

Endpoints under `/api/v1/internal/*` are token-gated. Set
`DEALIX_INTERNAL_TOKEN` in production. In dev, the token may be unset;
responses carry `auth_mode: "dev_unprotected"` so the mode is
explicit.

## 10. External-Impact Policy Rule

Every action that could touch the outside world routes through the
policy adapter (`api/internal/policy_adapter.py`) which evaluates the
rules in `policies/dealix_control_policy.yaml`. If a rule denies, the
endpoint returns HTTP 409 with the rule id and reason.

## 11. Commands

```bash
make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private
make brand-system
make growth-system
make marketing-system
make product-distribution
make policy-check
make agent-registry
make eval-gate
make brand-growth-operating-layer
make ultimate-operating-layer
make sovereign-operating-stack
make market-entry-stack
make company-os
make smoke-internal-api
```

## 12. Founder Console Pages

CEO · Sales · Approvals · Workers · Trust · Finance · Distribution ·
Delivery · Retention · Proof · Control · Audit · Evals · Product ·
Security · Sovereign · Growth · Marketing · Customer Success · Finance
Ops · Data · Experiments.

Existing pages (`/control-plane`, `/agents`, `/approvals`, `/safety`,
`/sandbox`, `/value-engine`, `/self-evolving`) are preserved and remain
the source of truth for those domains.

---

When in doubt: **prepare, queue, recommend. Never externally execute.**
