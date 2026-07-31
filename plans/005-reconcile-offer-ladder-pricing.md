# 005 — Reconcile contradictory offer-ladder pricing across canonical docs

- **Finding:** Three docs state three different prices/models for the entry
  paid offer, with no cross-reference or reconciliation:
  - `CLAUDE.md:104-111` (canonical "Business Model Summary"): Micro Sprint =
    499 SAR; Transformation Diagnostic Sprint = 7,500–25,000 SAR (primary
    paid entry, per `CLAUDE.md:14`).
  - `COMMERCIAL_IDENTITY.md:69`: `| Pilot | First paid engagement, typically
    SAR 2,500–7,500. |`
  - `README_FOUNDER_EXECUTION.md:15`: "Clear pricing model (499 SAR pilots →
    3,999 SAR/month recurring)" — a different recurring price than
    `CLAUDE.md`'s Managed Ops tier (2,999–4,999 SAR/mo).
  A founder or salesperson pulling a price from any one of these three docs
  could quote a customer a figure that contradicts what's in the other two —
  this is a direct commercial risk, not just a docs nit.
- **Category:** doctrine
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read the files below before editing
```

## Context (inlined)
- Files in scope: `COMMERCIAL_IDENTITY.md`, `README_FOUNDER_EXECUTION.md`
- Canonical source of truth (do not change): `CLAUDE.md:98-111`
    ```markdown
    ## Business Model Summary

    | # | Offer | Price |
    |---|-------|-------|
    | 1 | Free Diagnostic | Free |
    | 2 | Micro Sprint | 499 SAR |
    | 3 | Data Pack | 1,500 SAR |
    | 4 | Managed Ops | 2,999–4,999 SAR/mo |
    | 5 | Transformation Diagnostic Sprint | 7,500–25,000 SAR |
    | 6 | Custom Enterprise System | 25,000–100,000+ SAR |
    ```
- `COMMERCIAL_IDENTITY.md:69` (current, to be fixed):
    ```markdown
    | Pilot | First paid engagement, typically SAR 2,500–7,500. |
    ```
- `README_FOUNDER_EXECUTION.md:15` (current, to be fixed):
    ```markdown
    - ✅ Clear pricing model (499 SAR pilots → 3,999 SAR/month recurring)
    ```

## Steps
1. In `COMMERCIAL_IDENTITY.md`, change the `Pilot` row (line 69) to point at
   the canonical ladder instead of restating a number, e.g.:
   `| Pilot | First paid engagement — see the offer ladder in CLAUDE.md
   ("Business Model Summary") for current pricing. |`
   **Gate:** `grep -n "2,500–7,500" COMMERCIAL_IDENTITY.md` → no output.
2. In `README_FOUNDER_EXECUTION.md:15`, replace the hardcoded figures with a
   reference to the canonical ladder, e.g.:
   `- ✅ Clear pricing model — see CLAUDE.md "Business Model Summary" for
   current offer/price mapping (Free Diagnostic → Micro Sprint → Data Pack
   → Managed Ops → Transformation Diagnostic Sprint → Custom Enterprise)`
   **Gate:** `grep -n "3,999 SAR/month" README_FOUNDER_EXECUTION.md` → no output.
3. Grep the rest of the repo (excluding `plans/`, `docs/`, `sales/`, test
   fixtures) for any other hardcoded price figures that duplicate the
   ladder and aren't already flagged by another plan, and apply the same
   "point at CLAUDE.md" fix if found:
   `grep -rn "SAR" --include="*.md" -l . | grep -v -E "plans/|docs/|sales/|CLAUDE.md"`
   **Gate:** manually confirm each hit either matches the canonical ladder
   or is fixed to reference it.

## Done criteria (machine-checkable)
- [ ] `grep -rn "2,500–7,500\|3,999 SAR" COMMERCIAL_IDENTITY.md README_FOUNDER_EXECUTION.md` → no output
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not change `CLAUDE.md`'s Business Model Summary — it is the canonical
  source these two docs must defer to.
- Do not touch `sales/` templates or `docs/DEALIX_BUSINESS_MODEL.md` — those
  are handled by a separate docs-refresh plan (see 014).

## STOP conditions
- If `CLAUDE.md`'s Business Model Summary table has changed from the
  excerpt above → STOP, re-derive the correct reference text from the new
  table before editing the other two files.
- If a price figure elsewhere in the repo is tied to a signed contract or
  live customer quote (not just a doc/playbook) → STOP, escalate to founder
  rather than silently changing a number that may be contractually binding.
