# CLAUDE.md — Claude Code Operating Guide for Dealix

This file is the entry-point for Claude Code agents working in this repo.
For deeper operational context, see **[AGENTS.md](AGENTS.md)**.

## Project at a glance

Dealix is **Governed AI Operations for Saudi B2B**: operating capability +
auditable proof, NOT AI tools or spam. The codebase is large (~4,500
source files at depth-3), already production-bound on Railway, with 39+
GitHub Actions workflows protecting the main branch.

Branch policy: agents work on isolated `claude/*` branches and open PRs.
**Never push to `main` directly.**

## The 11 non-negotiables (enforced by tests and CI)

1. **No scraping systems** — sources must be founder-submitted or licensed.
2. **No cold WhatsApp automation** — outbound WhatsApp passes approval_center.
3. **No LinkedIn automation** — drafts only, founder sends manually.
4. **No fake / un-sourced claims** — every metric carries a `source_ref`.
5. **No guaranteed sales outcomes** — copy uses "estimated", never "guaranteed".
6. **No PII in logs** — middleware redacts email/phone/national-id.
7. **No source-less knowledge answers** — RAG answers must cite passages.
8. **No external action without approval** — all outbound passes `approval_center`.
9. **No agent without identity** — every agent registered in `registries/agent_registry.yaml`.
10. **No project without Proof Pack** — every paid engagement ships a Proof Pack (score >= 70).
11. **No project without Capital Asset** — every paid engagement registers >= 1 reusable asset.

If a request would violate any of these, **refuse and propose a safe alternative**.

## Top-20 Makefile commands

| Command | Purpose |
|---|---|
| `make help` | Show all targets |
| `make install-dev` | Install dev dependencies |
| `make test` | Full pytest suite (slow; 500+ files) |
| `make lint` | ruff + black |
| `make run` | Local FastAPI (port 8000) |
| `make everything` | **Run all 26-layer verifiers (supreme gate)** |
| `make company-os` | CEO OS + Founder Mgmt + Hypergrowth verifier |
| `make brand-system` | Brand OS verifier |
| `make policy-check` | Policy-as-Code verifier |
| `make agent-registry` | Agent Registry verifier |
| `make machine-registry` | Machine Registry verifier |
| `make eval-gate` | Eval Gate verifier |
| `make capital-allocation` | Capital Allocation report + verifier |
| `make strategy-scorecard` | Strategy Metrics report |
| `make revenue-forecast` | Revenue Factory forecast |
| `make market-attack-system` | Market Attack verifier |
| `make scale-moat-system` | Scale/Moat verifier |
| `make founder-ceo-hypergrowth-layer` | Hypergrowth CEO verifier |
| `make ceo-daily-brief` | Generate today's CEO brief |
| `make smoke-internal-api` | Internal API smoke test |
| `make bootstrap-runtime` | Bootstrap `/opt/dealix-ops-private/` tree |

## Doctrine quick-reference

- Every output object must carry a `governance_decision` field.
- Every Proof Pack score must be >= 70 before delivery.
- Every customer-facing markdown ends with the bilingual disclaimer:
  *"Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"*.
- Every Value Ledger event tier matches its evidence (verified requires
  `source_ref`; `client_confirmed` requires both refs).
- Private Ops files (`/opt/dealix-ops-private/`) MUST NEVER be committed.

## Repo orientation (where things live)

| Concern | Location |
|---|---|
| Domain packages | `dealix/` (24 sub-packages) |
| FastAPI app | `api/main.py`, `api/routers/` |
| Web (enterprise) | `apps/web/` (Next.js 15, port 3100) |
| Web (frontend) | `frontend/` (legacy Next.js) |
| Verifier scripts | `scripts/verifiers/` (NEW) + many top-level `scripts/verify_*.py` |
| Supreme verifier | `scripts/verify_everything.py` |
| Policies | `policies/` |
| Registries | `registries/` |
| Eval gates | `evals/gates/` |
| Operating docs | `docs/ops/`, `docs/company/`, `docs/commercial/` |
| Private ops layout | `docs/runtime/PRIVATE_OPS_LAYOUT.md` (data NEVER committed) |

## Operating rhythm for an agent invocation

1. Read this file + `AGENTS.md`.
2. Check `git status` and current branch.
3. Read the relevant verifier under `scripts/verifiers/`.
4. Make minimal changes, then run the affected verifier.
5. Run `python scripts/verify_everything.py --layer <name>` to confirm.
6. Commit with descriptive message. Never amend the user's commits.

## What you do NOT do

- Never charge a customer (Moyasar live mode is founder-flipped only).
- Never send email/WhatsApp/LinkedIn without `approval_center` decision.
- Never rename existing modules; build canonical wrappers if needed.
- Never write code in branches other than the assigned `claude/*` branch.
- Never invent metrics or pretend a paid customer exists when none does.
- Never commit `/opt/dealix-ops-private/` contents (only the bootstrap script).

---

**Stay accountable. Ship the plan. Honor the doctrine.**
