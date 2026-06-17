---
description: Improve the Dealix website (frontend/ + landing/) incrementally — premium, Arabic-first, one CTA per page, governance-safe — then run the real build gate.
---

Use `website-architect`, `brand-director`, `visual-identity-designer`, `conversion-specialist`,
and `proof-governance-reviewer`.

**Improve the existing surfaces — do not start a from-scratch rewrite.**
- `frontend/` (Next.js, RTL via `next-intl`) — build: `cd frontend && npm ci && npm run build`.
- `landing/` (static HTML + `styles.css`).
There is no root `npm run build`.

Build or improve these page intents (map to real routes/files; create only if truly missing):
`/` · Arabic home · Platform · Command Sprint · Business OS · Pricing · Industries · Security · Start.

Rules:
- Arabic-first · premium dark enterprise · one primary CTA per page
- no guaranteed revenue · no fake proof · no generic SaaS · Command Sprint is the first wedge
- module status label on every capability claim

After implementation:
- `cd frontend && npm run build && npm run lint`
- `python scripts/verify_website_positioning.py`
- fix failures if safe; otherwise report exact failing command + cause + proposed fix
- report changed files and the CTA flow per page
