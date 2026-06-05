---
name: dealix-verification
description: Verification gates for build, lint, types, security, env, positioning, and launch readiness. Apply after meaningful code or launch changes and before declaring launch-ready.
---

# Dealix Verification Skill

## For code changes
```bash
cd frontend && npm run build && npm run lint && npm run typecheck   # website
make env-check && make security-smoke                               # platform
python scripts/verify_website_positioning.py                        # positioning
```

## For launch changes (also verify)
- no guaranteed-revenue claims · no fake proof · no auto-send / cold-automation language
- exactly one primary CTA per page · module statuses present · Claims Register exists

## For CI / workflows (least privilege)
- default `permissions: contents: read`; widen only the specific scope needed
- never put plaintext secrets in workflows; redaction is not guaranteed
- never interpolate untrusted context (PR titles/bodies) directly into shell — use env vars

## On failure
Never hide it. Quote the exact failing command + output, name the likely cause, propose the fix.
Read for depth: `Makefile`, `scripts/security_smoke.py`, `scripts/verify_website_positioning.py`.
