---
name: audit-positioning
description: Audit any copy, page, or doc for Dealix positioning drift and unsafe claims. Use before publishing customer-facing content. Checks the Business OS frame, the one-CTA rule, forbidden words, guaranteed-revenue/auto-send/cold-WhatsApp/scraping language, unapproved customer names, unverifiable stats, PDPL overclaim, and future-as-live.
---

# Skill: audit-positioning

## When to use
Before any website page, doc, or growth asset goes customer-facing.

## Steps
1. Read the target file(s).
2. Check the **Business OS frame**: reject CRM / chatbot / WhatsApp bot / agency / generic AI / "Revenue-only" framing. Rewrite to Business OS.
3. Check **one main CTA** per page (secondary links de-emphasized).
4. Grep for forbidden patterns: `نضمن`, `guaranteed`, auto-send, cold WhatsApp, LinkedIn automation, scraping, fake scarcity.
5. Check for **unapproved customer names** and **unverifiable stats** (e.g. "3.2x", "500+ clients", "99.9%").
6. Check **PDPL** is described as PARTIAL (not native/complete).
7. Check every module label against `docs/00_platform_truth/MODULE_STATUS_MAP.md` — no FUTURE-as-LIVE.
8. Output PASS/BLOCK with file+line for each issue and a safe rewrite.

## References
`CLAUDE.md` §6, `docs/00_platform_truth/MESSAGING_HOUSE.md`, `docs/governance/FORBIDDEN_ACTIONS.md`, `dealix/registers/no_overclaim.yaml`.
