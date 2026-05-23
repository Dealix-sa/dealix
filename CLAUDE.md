# CLAUDE.md — Dealix Operating Constitution for AI Agents

This file is the canonical operating brief for any AI agent (Claude Code, sub-agents, copilots, schedulers, CI bots) that touches the Dealix repository at `/home/user/dealix`.

Read it before editing anything.

---

## Identity

**Dealix** is a Saudi B2B revenue intelligence platform that turns raw market signal into safe, governed, evidence-backed commercial action for sales, growth, and finance teams.

**Stack:** Python 3.11 (FastAPI) backend, Next.js (`apps/web`) frontend, JSONL + CSV operating ledgers, governed agent runtime.

**Audience:** Saudi enterprise GTM teams and the Dealix founder.

**Tagline:** `INTELLIGENT DEALS. REAL GROWTH.`

---

## Brand Palette (single source of truth)

| Token | Hex | Use |
|-------|-----|-----|
| Deep Navy | `#0B1220` | Primary surface, headers |
| Emerald Teal | `#00D1A1` | Accent, calls-to-action, evidence highlights |
| Soft Silver | `#B2BBC6` | Body text on dark, secondary UI |
| Slate | `#0F1726` | Cards, surfaces over Deep Navy |
| White | `#FFFFFF` | Inverse text |

The canonical machine-readable copy lives in `docs/brand/brand-tokens.json` and is mirrored to `apps/web/lib/brand-tokens.ts`.

Brand pillars (5): `Intelligence`, `Trust`, `Speed`, `Sovereignty`, `Saudi-First`.

---

## Architecture Overview

| Surface | Path | Purpose |
|---------|------|---------|
| Public API | `api/routers/` | Customer-facing routes |
| Internal API | `api/routers/internal/` (when added) | Founder/ops-only routes, token gated |
| Auto Client Acquisition | `auto_client_acquisition/` | Data OS, Governance OS, Proof OS, Value OS, Capital OS, Adoption OS, Friction Log, Sales OS, Email, Payment Ops, Client OS |
| Frontend | `apps/web/` | Next.js app + brand components |
| Worker scripts | `scripts/` | One-shot CLIs, verifiers, daily/weekly operators |
| Private runtime ops | `$PRIVATE_OPS` (default `/opt/dealix-ops-private`) | CSV ledgers; **never committed** |
| Policies | `policies/` | YAML control policies enforced in verifiers + agent runtime |
| Registries | `registries/` | Agent registry, tool registry |
| Evals | `evals/` (+ `evals/gates/`) | Eval suites and gating manifests |
| Docs | `docs/<area>/` | Brand, Growth, Marketing, Intelligence, Product, Security, Evals |

---

## 12 Non-Negotiables

1. **No A3 auto-execution.** Any A3-class action (external impact, money, contracts, public statements) requires human approval logged in `approvals/approval_queue.csv`.
2. **No outreach to suppressed contacts.** The `outreach/suppression_list.csv` is law. Match by email and phone hash.
3. **No guaranteed revenue or outcome claims.** Marketing, sales, and proposal copy must not promise revenue, deals, ROI guarantees, or "100%" outcomes.
4. **High-risk actions require evidence.** Any pricing change, contract change, or public proof publication must reference a stored evidence record.
5. **Source Passport before AI.** Any external data source ingested into the brain must have a `SourcePassport` (see `auto_client_acquisition/data_os/`).
6. **PII never leaves the tenant boundary without approval.** Detect and gate at `auto_client_acquisition/governance_os/`.
7. **No cold WhatsApp, no LinkedIn automation, no scraping engines.** Doctrine guards in `tests/` enforce this.
8. **Every output ships with a governance status and ProofPack when applicable.**
9. **Internal API is token-gated.** All `/api/v1/internal/...` routes require `X-Dealix-Internal-Token: $DEALIX_INTERNAL_TOKEN`.
10. **External impact policy.** No agent may take an action with external impact (sends, posts, payments, contract edits) without an explicit approval class A2/A3 plus a registered tool.
11. **No fake production readiness.** Verifier scripts must not report "ready" for anything that has not been functionally checked.
12. **No secrets in the repo.** Secrets live in environment variables. Workflows must not echo them.

---

## Never Auto-Execute

The following classes of action are **never** performed by an agent without an explicit, fresh, human approval recorded in `approvals/approval_queue.csv`:

- Sending email, SMS, or WhatsApp to a customer
- Posting to public social channels
- Charging, refunding, or modifying a payment method
- Editing or signing a contract / DPA / proposal
- Publishing a public case study, testimonial, or press release
- Changing a price on a customer-facing surface
- Exporting customer data outside the tenant
- Deleting, dropping, or truncating any production table
- Force-pushing to `main` or rewriting protected branch history
- Granting or revoking IAM/role permissions

If in doubt, escalate to the founder via `founder/operating_scorecard.md`.

---

## Required Checks (must pass before merge)

- `make policy-check` — policy-as-code validation
- `make agent-registry` — agent registry validation
- `make eval-gate` — eval gate manifest validation
- `make brand-system` / `make growth-system` / `make marketing-system` / `make product-distribution` — surface verifications
- `make brand-growth-operating-layer` — composite brand+growth+marketing
- `make ultimate-operating-layer` — composite full ops
- `make sovereign-operating-stack` — composite + security gate
- `make market-entry-stack` — full scorecard
- `make smoke-internal-api` — internal API smoke (safe if server is down)

The doctrine guards under `tests/` (see `tests/test_no_source_passport_no_ai.py`, `tests/test_pii_external_requires_approval.py`, `tests/test_no_cold_whatsapp.py`, `tests/test_no_linkedin_automation.py`, `tests/test_no_scraping_engine.py`, `tests/test_no_guaranteed_claims.py`, `tests/test_output_requires_governance_status.py`, `tests/test_proof_pack_required.py`) are the floor — never disable, never skip.

---

## Private Ops Rule

Operational ledgers (lead intelligence, outreach queue, approval queue, trust flags, cash collected, etc.) live **outside** the repo under the directory pointed to by `PRIVATE_OPS` (default `/opt/dealix-ops-private`).

- Bootstrap: `make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private`
- All worker scripts accept `--root` and default to `$PRIVATE_OPS`.
- No CSV under `PRIVATE_OPS` is ever committed.

---

## No Fake Production Readiness

A check is allowed to report "pass" only if the artifact it claims to verify physically exists and meets the declared shape. Verifier scripts:

- Must `exit 1` on any missing or malformed artifact.
- Must print a clear summary identifying which check failed.
- Must never silently `continue-on-error` for verifier steps.

---

## Internal API Safety

- All routers under `api/routers/internal/` (when added) require the header `X-Dealix-Internal-Token: $DEALIX_INTERNAL_TOKEN`.
- In dev mode (`DEALIX_INTERNAL_DEV=1`), a missing token is allowed but logged.
- Internal API endpoints never accept tenant-mutating writes; they are observability only.

---

## External Impact Policy

An action has **external impact** if it reaches a third party (email, SMS, WhatsApp, payment processor, social platform), modifies a customer-facing surface (price, contract, public page), or moves real money.

Rules:

- Agents may only request external-impact actions through a registered tool listed in `registries/agent_registry.yaml`.
- The tool entry must declare `external_action_allowed: true` and the agent must be cleared at `approval_class_max: A2` or `A3`.
- Every external-impact request lands in `approvals/approval_queue.csv` with severity, evidence pointer, and tool name; the founder (or designated approver) flips it to `approved` before execution.
- Execution is logged to `trust/approval_decisions.csv`.

---

## Commands (Section A surface)

```
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
make smoke-internal-api
```

Run `make help` for the full list including v5 and v10 founder tooling already present in the Makefile.
