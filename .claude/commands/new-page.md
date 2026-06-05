---
description: Scaffold a new Dealix website page that follows the one-CTA rule, AR+EN i18n parity, and the dark executive style. Usage: /new-page <route> <one-cta-destination>
---

# /new-page

Scaffold a compliant Next.js page in the primary frontend. Arguments: the route slug and the
single CTA destination (Business OS Score / Diagnostic / Command Sprint).

Steps:
1. Create `frontend/src/app/[locale]/<route>/page.tsx` using the dark executive style and the
   Navy/Gold tokens from `docs/00_platform_truth/VISUAL_IDENTITY_SYSTEM.md`.
2. Add **exactly one main CTA** routing to the given approved destination.
3. Add every visible string to **both** `frontend/messages/ar.json` and
   `frontend/messages/en.json` (AR-first, EN parallel).
4. Ensure no claim is used unless it is in `docs/governance/CLAIMS_REGISTER.md`.
5. Run `cd frontend && npm run build` and report the result.

After scaffolding, hand off to `one-cta-check` and `claims-check` before publishing. Do not
commit or push without founder approval.
