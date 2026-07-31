# 005 — RETIRED → see 017

**Status:** 🗄️ Retired 2026-07-31 during the Founder-360 reconciliation pass.
Not deleted — kept for audit-trail continuity, same convention used when
PRs #1006-#1008 were closed as superseded rather than erased.

## Why this plan was retired

This plan was written against the offer-ladder table then visible in
`main`'s `CLAUDE.md:98-111` (the old 6-rung fixed-price ladder: Free
Diagnostic / Micro Sprint 499 SAR / Data Pack 1,500 SAR / Managed Ops
2,999–4,999 SAR/mo / Transformation Diagnostic Sprint 7,500–25,000 SAR /
Custom Enterprise 25,000–100,000+ SAR), and proposed pointing
`COMMERCIAL_IDENTITY.md` and `README_FOUNDER_EXECUTION.md` at that table.

During the Founder-360 reconciliation pass (2026-07-31) it became clear
that table is itself stale and about to be replaced: **PR #1005** (open,
not yet merged as of this writing) rewrites `CLAUDE.md`'s Business Model
Summary and `.claude/rules/dealix-commercial-os.md`'s offer ladder to match
the 2-offer model already live in code
(`auto_client_acquisition/service_catalog/registry.py`'s `commercial_status`
field: `free_mini_diagnostic` = `free_entry`, `revenue_command_pilot_30d` =
`quote_only`, 15 other catalogued offerings = `internal_experiment`).

Executing this plan as originally written would have pointed two docs at a
table that PR #1005 is about to delete — creating fresh inconsistency
instead of fixing it.

## What replaced it

**`plans/017-reconcile-pricing-docs-to-registry.md`** covers the same two
target files (`COMMERCIAL_IDENTITY.md`, `README_FOUNDER_EXECUTION.md`),
retargeted to inline the canonical table directly from
`auto_client_acquisition/service_catalog/registry.py` (the actual source of
truth) instead of from `CLAUDE.md`, so it isn't blocked on PR #1005
merging and won't go stale again if the registry changes independently of
that PR. It also explicitly excludes `CLAUDE.md` from its scope — that file
belongs to PR #1005's branch.

See `plans/INDEX.md`'s "Founder-360 reconciliation (2026-07-31)" section
for the full cross-reference.
