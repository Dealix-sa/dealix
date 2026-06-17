---
name: claims-check
description: Read-only review of external-facing copy for unsafe claims. Use before publishing any website page, growth asset, or proposal. Flags guaranteed revenue/ROI, fake proof, fake scarcity, and any FUTURE/BETA module described as live. Cross-checks against docs/governance/CLAIMS_REGISTER.md and docs/00_platform_truth/MODULE_STATUS_MAP.md.
---

# Claims Check

A read-only governance check. It does not edit files — it reports.

## When to use

Before any copy reaches a prospect: website pages, free-tool outputs, growth assets,
proposals, posts.

## What it checks

1. **No guaranteed outcomes.** Flag "guaranteed", "نضمن", "مضمون", promised revenue/ROI/%.
2. **No fake proof.** Flag specific metrics, logos, or testimonials not traceable to a
   source in `docs/governance/CLAIMS_REGISTER.md`.
3. **No fake scarcity.** Flag "only N left", countdowns, urgency not literally true.
4. **No future-as-live.** For every module named, confirm its status in
   `docs/00_platform_truth/MODULE_STATUS_MAP.md` is `LIVE` before it is described as available.
5. **Claim registration.** Every external claim must appear in `CLAIMS_REGISTER.md` tagged
   `evidence-backed` or `hypothesis`.

## How to run it

- Grep the target file(s) for the banned patterns above (AR + EN).
- Read `MODULE_STATUS_MAP.md` and `CLAIMS_REGISTER.md`.
- Output a table: claim · location · verdict (`ok` / `reframe` / `remove`) · reason.

## Output

A findings table and a single PASS/FAIL line. Never edits — hand findings to
`proof-governance-reviewer` to fix.
