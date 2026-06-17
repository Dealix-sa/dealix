---
name: one-cta-check
description: Read-only check that each website page has exactly one main CTA routing to Business OS Score, Diagnostic, or Command Sprint. Use when reviewing any page under frontend/src/app/[locale]/. Flags pages with zero or more than one primary CTA, and CTAs that route anywhere other than the three approved destinations.
---

# One-CTA Check

Read-only. Enforces hard rule 14 (one main CTA per page) and hard rule 15 (route to an
approved destination).

## When to use

Whenever a page in `frontend/src/app/[locale]/` is created or changed.

## What it checks

1. **Exactly one main CTA** per page. Secondary links allowed only if visually subordinate.
2. **Routing.** The main CTA links to one of: `/business-os-score`, `/dealix-diagnostic`
   (Diagnostic), or `/command-sprint`.
3. **No competing primary actions** (two equally-weighted buttons = fail).

## How to run it

- Identify the page's primary button/CTA component(s).
- Count primary CTAs; read their `href`/route.
- Output a table: route · CTA label · destination · verdict.

## Output

Per-page table + PASS/FAIL. Pages with 0 or >1 main CTA, or an off-list destination, FAIL.
Hand fixes to `conversion-specialist` / `website-architect`.
