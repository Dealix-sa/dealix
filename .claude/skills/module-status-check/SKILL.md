---
name: module-status-check
description: Read-only check that every one of the 14 Business OS modules has a valid status in docs/00_platform_truth/MODULE_STATUS_MAP.md and that no FUTURE/BETA module is described as live anywhere in public copy or docs. Reconciles claimed status against real code under auto_client_acquisition/*_os/.
---

# Module Status Check

Read-only. Enforces hard rule 9 (no future module presented as live).

## When to use

Before publishing, and whenever `MODULE_STATUS_MAP.md` or any module-describing copy changes.

## The 14 modules

Command OS · Market Intelligence OS · Revenue OS · Proof OS · Delivery OS · Client OS ·
Support OS · Finance OS · Data OS · Governance OS · Knowledge OS · Agent OS · Partner OS ·
Academy OS.

## What it checks

1. **Completeness.** All 14 modules appear in `MODULE_STATUS_MAP.md`.
2. **Valid status.** Each is one of `LIVE`, `BETA`, `INTERNAL`, `DOCS_ONLY`, `BLOCKED`,
   `FUTURE`, `DEPRECATED`.
3. **Honesty vs code.** A module tagged `LIVE` should have backing code under
   `auto_client_acquisition/*_os/`; flag `LIVE` claims with no code.
4. **No future-as-live in copy.** Grep website/docs for any non-LIVE module described as
   available now.

## Output

A table: module · claimed status · code present? · public-copy conflicts · verdict.
PASS only if all 14 present, statuses valid, and no future-as-live conflicts.
