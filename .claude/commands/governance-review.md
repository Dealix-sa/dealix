---
description: Run a proof & governance review on the current diff or a named file before it ships.
---

# /governance-review

Invoke the `proof-governance-reviewer` agent (or `audit-positioning` skill) on the target.

Check and report each violation with file + line + safe rewrite:
- Guaranteed revenue ("نضمن"/"guaranteed" + numbers), fabricated metrics, fake scarcity.
- Auto-send, cold WhatsApp, LinkedIn automation, scraping behind login.
- Unapproved customer names / case studies; unverifiable stats ("3.2x", "500+", "99.9%").
- PDPL claimed as native/complete (it is PARTIAL today).
- Any FUTURE/BETA module shown as LIVE (check `docs/00_platform_truth/MODULE_STATUS_MAP.md`).

Output a PASS / BLOCK verdict. BLOCK if any violation remains.

Authoritative sources: `docs/governance/FORBIDDEN_ACTIONS.md`, `docs/governance/TRUST_SAFETY_CHARTER.md`, `dealix/registers/no_overclaim.yaml`.
