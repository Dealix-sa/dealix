# CLAUDE.md — Dealix Company OS guidance for AI assistants

This file is read by Claude Code (and any other AI tool that respects
`CLAUDE.md`) before acting in this repo. The repo's actual operating
doctrine lives in `docs/governance/` — this file points to it.

## The 11 non-negotiables (do NOT violate)

Sources: `docs/governance/AI_ACTION_CONTROL.md`,
`docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`, the Dealix Constitution.

1. **NO_LIVE_SEND** — No external customer messaging without explicit
   founder approval. Drafts only.
2. **NO_LIVE_CHARGE** — No production payment processing. Moyasar test
   mode + manual bank transfer only.
3. **NO_COLD_WHATSAPP** — Cold WhatsApp automation strictly forbidden.
4. **NO_LINKEDIN_AUTOMATION** — LinkedIn DM automation banned.
5. **NO_SCRAPING** — No production web scraping or purchased list blast.
6. **NO_FAKE_PROOF** — Proof claims must cite source. No invented metrics.
7. **NO_FAKE_REVENUE** — Revenue = payment evidence only. Draft invoices,
   verbal interest, diagnostics ≠ revenue.
8. **NO_UNAPPROVED_TESTIMONIAL** — No customer name / logo / case study
   public mention without signed permission.
9. **NO_PROOF_LEVEL_OVERCLAIMING** — Proof level L0–L1 blocks external
   marketing; L2–L3 internal only; L4+ requires approval + customer consent.
10. **NO_UNSOURCED_NUMERIC_CLAIM** — Every metric in customer-facing
    materials cites source OR carries `is_estimate=true`.
11. **NO_CROSS_TENANT_OPERATIONAL_ACCESS** — Strict tenant isolation;
    no founder viewing another customer's data.

## Canonical module map

| Concern | Source of truth |
|---|---|
| Approval gates | `dealix/config/approval_policy.yaml` |
| Claim guards | `dealix/config/claim_policy.yaml` |
| Forbidden actions | `auto_client_acquisition/governance_os/policies/default_registry.yaml` |
| Agent registry | `auto_client_acquisition/agent_governance/agent_registry.py` |
| Machine registry | `dealix/execution_assurance/registry.yaml` |
| Service ladder | `docs/COMPANY_SERVICE_LADDER.md` |
| 7-day Sprint | `docs/V14_7_DAY_REVENUE_PLAN.md` |
| Service catalog | `dealix/services/SERVICE_READINESS_MATRIX.yaml` |
| Master verifier | `scripts/verify_everything.py` (or `make everything`) |

The thin wrappers in `policies/`, `registries/`, `evals/gates/` are
single-surface views; verifiers read the canonical files. **Never edit
the wrappers without first editing the canonical file.**

## Article 13 Build Order (immutable)

Scaling beyond Phase G (first revenue) is forbidden until **3 paid
pilots** are collected. The Founder Console under `/api/v1/internal/*`
is internal infra and does not constitute a customer-facing surface.

## Approval-first contract

Every external or irreversible action class must route through the
approval center (`auto_client_acquisition/approval_center/`). The
approval ledger in `$PRIVATE_OPS/trust/approval_decisions.csv` records
every decision. **No bypass.**

## Private ops convention

- Path: `/opt/dealix` (override via `$PRIVATE_OPS`).
- Bearer: `$DEALIX_ADMIN_API_KEY` (or `$ADMIN_API_KEYS`).
- Never commit anything under `/opt/dealix` to the repo.
- Bootstrap: `make bootstrap-runtime`.

## `make everything` — the single judge

The master verifier is `scripts/verify_everything.py`. It runs every
sub-verifier, checks the hard-rule invariants (live_charge gated,
WhatsApp/LinkedIn/scrape forbidden, ROI/guarantee banned), and prints
a `DEALIX_EVERYTHING=pass|fail` verdict. **Treat `make everything = pass`
as a release gate.**

## What to do BEFORE pushing a PR

```bash
make everything
make smoke-internal-api       # optional; skips if API not running
npm --prefix apps/web run build  # if you touched the frontend
```

## What NOT to do

- Don't add external send code paths.
- Don't add a "live charge" backdoor.
- Don't publish proof packs or case studies via code.
- Don't weaken a verifier to make CI green.
- Don't introduce a parallel `policies/` or `registries/` schema; extend
  the existing canon.
- Don't override the 11 non-negotiables without a doctrine RFC + 5-OS
  owner review.
