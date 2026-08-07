# 017 — Reconcile COMMERCIAL_IDENTITY.md and README_FOUNDER_EXECUTION.md to the registry

- **Finding:** (Retires `plans/005`, which targeted the wrong source of
  truth — see that file for why.) Two docs still quote fixed prices for
  the entry offer that no longer match the product's actual commercial
  model. The real source of truth,
  `auto_client_acquisition/service_catalog/registry.py`, defines exactly
  two commercially-live offerings: `free_mini_diagnostic`
  (`commercial_status="free_entry"`, price 0, registry.py:34-63) and
  `revenue_command_pilot_30d` (`commercial_status="quote_only"`,
  `price_sar=0.0`, `price_unit="custom"`, registry.py:66-111 — the
  docstring at registry.py:12-15 states plainly: "Every other price
  remains an internal experiment... until a separate approval changes
  `commercial_status`"). Against that truth:
  - `COMMERCIAL_IDENTITY.md:69`: `| Pilot | First paid engagement,
    typically SAR 2,500–7,500 |` — a fixed range the registry doesn't back.
  - `README_FOUNDER_EXECUTION.md:15`: "Clear pricing model (499 SAR
    pilots → 3,999 SAR/month recurring)".
  - `README_FOUNDER_EXECUTION.md:67`: "3 pilots signed (499 SAR payment
    received)" (a Day-30 checklist item).
  - `README_FOUNDER_EXECUTION.md:76`: "5+ renewals at 3,999 SAR/month"
    (a Day-90 checklist item).
  None of these numbers exist in the registry; quoting any of them to a
  real prospect would contradict the product's actual quote-only model.
- **Category:** doctrine / commercial-os
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read the files below before editing
python3 -c "from auto_client_acquisition.service_catalog.registry import *" 2>&1 | head -5   # confirm the module still imports before trusting its docstring's claims
grep -n "commercial_status" auto_client_acquisition/service_catalog/registry.py   # re-confirm only free_mini_diagnostic and revenue_command_pilot_30d carry a live status
```

## Context (inlined)
- Files in scope: `COMMERCIAL_IDENTITY.md`, `README_FOUNDER_EXECUTION.md`.
- **Do not touch `CLAUDE.md`** — PR #1005 (open, separate branch) already
  rewrites `CLAUDE.md`'s Business Model Summary to this same registry
  model; editing it here would conflict with that PR. This plan reads the
  canonical table from `registry.py` directly (source of truth), not from
  `CLAUDE.md` or PR #1005's branch, so it works whether or not #1005 has
  merged yet.
- Canonical facts to inline (from `registry.py`, re-verify at execution
  time via the drift-check commands above, not copied blindly):
  - Free Mini Diagnostic — free, 1 day, discovery-stage.
  - Revenue Command Pilot — 30 days — quote-only, no fixed public price,
    price/scope set after discovery.
  - Every other catalogued offering is `internal_experiment` — not a live
    public offer; do not quote a price for one.

## Steps
1. In `COMMERCIAL_IDENTITY.md:69`, replace the fixed-range row with
   quote-only language:
    ```markdown
    | Pilot | Revenue Command Pilot — 30 days, quote-only after discovery (no public fixed price). |
    ```
   **Gate:** `grep -n "2,500–7,500" COMMERCIAL_IDENTITY.md` → no output.
2. In `README_FOUNDER_EXECUTION.md:15`, replace the hardcoded figures:
    ```markdown
    - ✅ Clear commercial path (Free Mini Diagnostic → quote-only 30-day Revenue Command Pilot; price set after discovery, not a public fixed rate)
    ```
   **Gate:** `grep -n "499 SAR pilots\|3,999 SAR/month recurring" README_FOUNDER_EXECUTION.md` → no output.
3. In `README_FOUNDER_EXECUTION.md:67`, replace the Day-30 checklist item:
    ```markdown
    - [ ] 3 pilots signed (scoped quote accepted + payment evidence received)
    ```
   **Gate:** `grep -n "499 SAR payment received" README_FOUNDER_EXECUTION.md` → no output.
4. In `README_FOUNDER_EXECUTION.md:76`, replace the Day-90 checklist item:
    ```markdown
    - [ ] 5+ renewals/expansions (each priced individually after outcome review)
    ```
   **Gate:** `grep -n "3,999 SAR/month" README_FOUNDER_EXECUTION.md` → no output.
5. Grep both files once more for any remaining hardcoded SAR figure this
   plan's four targeted edits might have missed:
   `grep -n "SAR" COMMERCIAL_IDENTITY.md README_FOUNDER_EXECUTION.md`
   Review every remaining hit — fix any that states a fixed price for
   `free_mini_diagnostic` or `revenue_command_pilot_30d`; leave alone any
   that's clearly describing something else (e.g. a cost estimate for
   founder tooling, not a customer-facing price).
   **Gate:** command output reviewed; no remaining customer-facing fixed
   price for either live offer.

## Done criteria (machine-checkable)
- [ ] `grep -rn "2,500–7,500\|499 SAR\|3,999 SAR" COMMERCIAL_IDENTITY.md README_FOUNDER_EXECUTION.md` → no output
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not touch `CLAUDE.md` — owned by PR #1005.
- Do not touch `docs/DEALIX_BUSINESS_MODEL.md` — owned by PR #1011 (see
  plan 014's revision note).
- Do not touch `sales/` templates — those are customer-facing and reviewed
  separately under `.claude/rules/dealix-commercial-os.md`; if the same
  stale-price pattern exists there, report it as a new finding.
- Do not invent a specific replacement number for any removed figure — use
  quote-only / evidence-based language, matching the registry's own
  `kpi_commitment_en` phrasing style (registry.py:86-89).

## STOP conditions
- If `registry.py`'s `commercial_status` values have changed from the
  excerpt above (e.g. a third offer is now live) → STOP, re-derive the
  correct reference text from the new registry state before editing.
- If a price figure in either file is tied to a signed contract or a
  specific named customer's live quote (not just general doc/playbook
  language) → STOP, escalate to founder rather than silently changing a
  number that may be contractually binding.
