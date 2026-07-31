# 014 — Refresh stale canonical docs and retire the conflicting legacy reference

> **Revised 2026-07-31 (Founder-360 reconciliation):** the original Step 2
> below (a staleness-stamp patch to `docs/DEALIX_BUSINESS_MODEL.md`) is
> dropped. PR #1011 (open, branch `ops/founder-360-market-truth-20260731`)
> already fully rewrites that file into a "Market Validation Edition
> v2.0-draft" — a staleness-stamp patch on top of the *old* content would
> be immediately obsoleted once #1011 merges, or would conflict with it if
> applied first. Everything else in this plan (`CEO_OPERATING_CONTEXT.md`,
> `SYSTEM_COMPLETE_REFERENCE.md`, the `00_constitution`/`00_foundation`
> duplicate cleanup) is untouched by #1011 and remains in scope unchanged.

- **Finding:** `docs/CEO_OPERATING_CONTEXT.md` is frozen at 2026-06-10
  (`docs/CEO_OPERATING_CONTEXT.md:41`: "## Current Confirmed State (as of
  Wave 1)") while the repo has since produced Wave 3 through Wave 17
  artifacts under `docs/` (20+ `WAVE*_EVIDENCE_TABLE.md` /
  `_CURRENT_REALITY.md` files) — this "current state" doc is 7+ weeks and
  ~16 Waves out of date. Separately, `SYSTEM_COMPLETE_REFERENCE.md`
  (root, 45KB) describes an entirely different, older architecture — a
  "5-Layer Automation Stack" (Lead Research → Lead Qualification → Sales
  Qualification Agent → Approval Queue UI → Pilot Delivery Orchestrator)
  referencing files like `FOUNDER_DAILY_EXECUTION_PLAYBOOK.md` and
  `dealix_founder_daily_complete.sh` — with no mention of Hermes,
  `apps/web`, or the FastAPI/Railway stack that CLAUDE.md's "Architecture
  Summary" centers on. It has a single git log entry (`3c46c6d`, a lint
  pass, not a content update), meaning it was never reconciled after the
  architecture moved on — anyone (including a future Claude Code session)
  reading it to orient themselves gets a factually wrong picture of the
  system. `docs/00_constitution/` and `docs/00_foundation/` also duplicate
  the same four files verbatim (`DEALIX_CONSTITUTION.md`,
  `NON_NEGOTIABLES.md`, `OPERATING_EQUATION.md`, `GOOD_REVENUE_BAD_REVENUE.md`,
  `WHAT_DEALIX_REFUSES.md`).
- **Category:** docs
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read the files below before editing — check whether they've already been updated
```

## Context (inlined)
- Files in scope: `docs/CEO_OPERATING_CONTEXT.md`,
  `SYSTEM_COMPLETE_REFERENCE.md`, `docs/00_constitution/`,
  `docs/00_foundation/`.
- `docs/DEALIX_BUSINESS_MODEL.md` is explicitly **out of scope** — see the
  revision note at the top of this file. Do not touch it; PR #1011 owns it.
- This plan does not ask the executor to invent new business facts (e.g.
  a real customer count) — it asks for date-stamp/staleness-marker fixes
  and one structural cleanup (duplicate dirs, orphaned legacy doc), the
  same pattern as plan 004's CLAUDE.md fix.
- `diff -rq docs/00_constitution/ docs/00_foundation/` should be run first
  to confirm the exact duplication before touching either directory.

## Steps
1. In `docs/CEO_OPERATING_CONTEXT.md`, update the "## Current Confirmed
   State (as of Wave 1)" heading to reference the actual current Wave (per
   `CLAUDE.md`'s "Wave Roadmap" table) or, if the content itself is
   Wave-1-specific and now superseded, replace the heading with "## State
   as of Wave 1 (historical — see CLAUDE.md for current Wave status)" so
   readers aren't misled into thinking it's current. Add a top-of-file
   "**Last reviewed:**" stamp using today's actual repo-visible date
   context (do not fabricate a specific "verified" claim about business
   facts — only date the doc itself).
   **Gate:** `grep -n "Last reviewed" docs/CEO_OPERATING_CONTEXT.md` → 1 match.
2. Run `diff -rq docs/00_constitution/ docs/00_foundation/` to confirm
   which files are byte-identical duplicates. For each exact duplicate,
   keep the copy under `docs/00_constitution/` (it sorts first,
   alphabetically the more likely intended canonical location — confirm by
   checking which one CLAUDE.md or other docs link to via
   `grep -rn "00_foundation\|00_constitution" --include="*.md" docs/ CLAUDE.md`)
   and replace the other with a one-line pointer file, e.g.
   `docs/00_foundation/DEALIX_CONSTITUTION.md` becomes:
   `# Moved\n\nSee \`docs/00_constitution/DEALIX_CONSTITUTION.md\`.`
   Only do this for files confirmed byte-identical by the diff — if any
   pair has diverged content, STOP for that pair (see STOP conditions) and
   leave both in place.
   **Gate:** `diff -rq docs/00_constitution/ docs/00_foundation/` on the
   still-present files shows only expected pointer-file differences, not
   silently lost content.
3. For `SYSTEM_COMPLETE_REFERENCE.md`, add a prominent banner at the very
   top of the file marking it as a legacy/historical architecture
   description superseded by `CLAUDE.md`'s "Architecture Summary":
    ```markdown
    > **⚠ Historical document.** This describes an earlier iteration of
    > the system (the pre-Hermes/pre-`apps/web` architecture). For the
    > current architecture, see `CLAUDE.md` → "Architecture Summary".
    > Kept for historical reference only; do not use this to orient a new
    > contributor or answer "what does Dealix's system look like today."
    ```
   Do not rewrite or delete the rest of the file's content — that's a
   larger effort and the file may have historical value.
   **Gate:** `head -5 SYSTEM_COMPLETE_REFERENCE.md | grep -q "Historical document"` → true.

## Done criteria (machine-checkable)
- [ ] `grep -n "Last reviewed" docs/CEO_OPERATING_CONTEXT.md` → 1 match
- [ ] `head -5 SYSTEM_COMPLETE_REFERENCE.md | grep -q "Historical document"` → true
- [ ] `make full-repo-test` → all required gates PASS (docs-only change, must not alter behavior/tests)

## Out of scope (do not touch)
- Do not touch `docs/DEALIX_BUSINESS_MODEL.md` — owned by PR #1011 (see
  revision note at the top of this file).
- Do not attempt to reorganize the full `docs/` tree (3,163 files, 93
  numeric-prefixed dirs) in this plan — that is a much larger structural
  project needing its own dedicated, founder-sequenced plan; this plan
  only fixes the specific stale/conflicting docs named above.
- Do not delete `SYSTEM_COMPLETE_REFERENCE.md` or rewrite its body content.
- Do not merge `docs/00_constitution/` and `docs/00_foundation/` beyond the
  exact-duplicate files confirmed by `diff -rq` in step 2.
- Do not fabricate any new business fact, customer count, or metric while
  "updating" `docs/CEO_OPERATING_CONTEXT.md` — only fix staleness framing
  and cross-references, per the doctrine rules in
  `.claude/rules/dealix-commercial-os.md`.

## STOP conditions
- If any file pair in `docs/00_constitution/` vs `docs/00_foundation/`
  is NOT byte-identical → STOP for that pair specifically, leave both
  files untouched, and report the divergence (it may be an intentional
  fork, not accidental duplication).
- If `CLAUDE.md` or another doc's internal links would break by converting
  a duplicate into a pointer file → STOP, fix the referencing links first
  or choose the other directory as canonical instead.
- If the "Current Confirmed State" section in `docs/CEO_OPERATING_CONTEXT.md`
  contains claims that look load-bearing for an active sales conversation
  (e.g. specific named prospects) → STOP and report rather than editing;
  that content needs founder review, not a mechanical date-stamp fix.
