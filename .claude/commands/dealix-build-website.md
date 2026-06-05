---
description: Plan or build a Dealix website page against the Website Conversion Map
---

# /dealix-build-website

Drive the website layer (PR 3 scope) one page at a time.

## Source of truth
- "Website Conversion Map" in `docs/05_founder/DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md`.

## Per-page contract (must hold before a page is "done")
- target audience, pain, core promise, proof/output shown, **single** primary CTA, status, analytics event.
- CTA routes to Business OS Score, Diagnostic, or Command Sprint.
- No guaranteed claims; no future module shown as live.
- `npm run build` passes (frontend) before marking done.

## When invoked
1. Ask which page (default: the next page with status `NEXT` on the Execution Board).
2. State the page's row from the Conversion Map before writing anything.
3. Implement only that page + its analytics event wiring.
4. End with the exact verification command and the acceptance checklist result.
