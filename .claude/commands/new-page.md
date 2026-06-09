---
description: Scaffold a new Arabic-first, RTL-safe website page in frontend/ with exactly one CTA.
---

# /new-page

Create a new route under `frontend/src/app/[locale]/` using the `write-bilingual-page` skill.

Inputs: route path, page purpose, the single main CTA target (Business OS Score / Diagnostic / Command Sprint).

Steps:
1. Restate scope and the files you expect to touch.
2. Reuse existing tokens/components; add copy to `frontend/messages/{ar,en}.json` (Arabic first).
3. Exactly one main CTA. RTL-safe. No FUTURE module shown as LIVE.
4. Run `cd frontend && npm run lint && npm run typecheck && npm run build`.
5. Run the `audit-positioning` skill.
6. Show changed files + `git diff --stat`. Do not commit until approved.
