---
description: Create a new Dealix growth asset that routes to exactly one approved CTA.
---

# /new-growth-asset

Create a growth asset (content, tool spec, nurture step, partner/referral piece) under `docs/06_growth/`.

Rules:
- It MUST route to exactly one of: **Business OS Score**, **Diagnostic**, or **Command Sprint**.
- No cold WhatsApp, no LinkedIn automation, no scraping, no auto-send, no fake scarcity.
- Nurture is draft-only and consent-based.

Steps:
1. State the asset type and its single CTA target.
2. Draft it on the Business OS frame (run `audit-positioning`).
3. Note the growth loop it feeds (free-tool→Score→Sprint, proof→content→inbound, referral→partner, nurture→re-engage→Diagnostic).
4. Show changed files. Do not commit until approved.
