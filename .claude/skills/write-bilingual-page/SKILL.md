---
name: write-bilingual-page
description: Create or update an Arabic-first, English-ready, RTL-safe page in frontend/ with exactly one main CTA. Use when building website routes. Reuses existing design tokens and next-intl message catalogs; never invents a new design system or adds a second primary CTA.
---

# Skill: write-bilingual-page

## When to use
Building or rewriting a route under `frontend/src/app/[locale]/`.

## Steps
1. Read the existing tokens (`frontend/src/styles/dealix-system.css`, `dealix-brand.css`) and reuse components from `frontend/src/components/`.
2. Add copy to BOTH `frontend/messages/ar.json` and `frontend/messages/en.json` (Arabic first).
3. Build the page with **exactly one** main CTA; de-emphasize secondary links.
4. Verify RTL on `/ar` (`[dir="rtl"]`).
5. Confirm every module label matches `docs/00_platform_truth/MODULE_STATUS_MAP.md`.
6. Run `cd frontend && npm run lint && npm run typecheck && npm run build`.
7. Run the `audit-positioning` skill on the new copy before finishing.

## Rules
- Arabic-first. No childish gradients, no clutter, executive command-center look.
- No new dependencies without justification. No pricing changes unless this is a pricing PR.
