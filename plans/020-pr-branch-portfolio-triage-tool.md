# 020 — Add staleness + duplicate-title detection to the existing PR triage tool

- **Finding:** `scripts/triage_open_prs.py` and its policy doc
  (`docs/agents/PR_TRIAGE_POLICY.md`) already exist and do most of what
  issue #938 ("Portfolio Stabilization Control Tower") needs: they fetch
  every open PR via `gh pr list`, sort into 6 buckets (draft / security /
  dependencies / agent / docs / needs_review), and write a report —
  humans decide, the tool never merges (`triage_open_prs.py:6-7`). This
  should be **extended, not replaced or duplicated** — writing a second,
  competing triage script would repeat the exact sprawl pattern this
  backlog is trying to fix elsewhere (see plan 019's note on 37+ existing
  smoke scripts).
  Two capabilities the policy doc promises but the tool doesn't yet
  compute:
  1. **Staleness.** The policy states (`docs/agents/PR_TRIAGE_POLICY.md`,
     "Hygiene rules"): "A PR with no update in 30+ days and conflicts →
     propose close with a note." `build_buckets()` (`triage_open_prs.py:79-85`)
     only sorts by `updatedAt` within a bucket — it never computes an age
     in days or flags anything as past the 30-day threshold, so the
     hygiene rule currently requires a human to eyeball timestamps.
  2. **Duplicate-title detection.** Confirmed via GitHub API during this
     audit: PRs #989 ("fix(railway): require exact deployment proof"),
     #995 (identical title), #1002 and #1004 (both "fix(railway): trust
     CLI deployment ID before live SHA proof") are four separate PRs
     re-submitting essentially the same fix under near-identical titles —
     all now closed, but demonstrating exactly the pattern issue #938
     flags as a triage problem ("~45 open PRs pending triage... dependabot,
     ci-security, docs-wave, engine-wave buckets"). `classify()`
     (`triage_open_prs.py:38-56`) has no mechanism to detect that two open
     PRs are near-duplicates of each other.
- **Category:** tech-debt / ops
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read scripts/triage_open_prs.py before editing
```

## Context (inlined)
- Files in scope: `scripts/triage_open_prs.py`,
  `docs/agents/PR_TRIAGE_POLICY.md` (update to describe the new fields).
- The tool degrades gracefully when `gh` isn't installed
  (`fetch_prs()`, `triage_open_prs.py:59-76`, returns `None` →
  `write_skipped_report`) — preserve this behavior exactly; do not
  introduce a hard dependency on network/API access that breaks the
  "always exits 0" contract (`triage_open_prs.py:14`).
- `fetch_prs()`'s `gh pr list --json` fields
  (`number,title,author,createdAt,updatedAt,labels,isDraft`) already
  include `createdAt`/`updatedAt` — no new API field is needed for the
  staleness computation, only new logic on data already fetched.

## Steps
1. Add a `days_stale(pr: dict) -> int` helper computing
   `(now - updatedAt).days` from the ISO timestamp already fetched.
   Add a `STALE_THRESHOLD_DAYS = 30` constant matching the policy doc's
   stated rule.
   **Gate:** `python3 -c "from scripts.triage_open_prs import days_stale; print(callable(days_stale))"` → `True`.
2. In `render_markdown()`, add a new top-level section before the bucket
   breakdown: "## Stale (30+ days, no update)" listing every PR across all
   buckets past `STALE_THRESHOLD_DAYS`, sorted oldest-first. This
   surfaces the policy's hygiene rule as a standing report section instead
   of requiring a human to scan every bucket for old timestamps.
   **Gate:** `grep -n "## Stale" scripts/triage_open_prs.py` → 1 match (in the render function's output template).
3. Add a `find_near_duplicate_titles(prs: list[dict]) -> list[tuple[dict, dict]]`
   function using a simple, dependency-free normalization + comparison
   (lowercase, strip conventional-commit prefixes like `fix(...):`/`feat(...):`,
   strip punctuation, then compare via `difflib.SequenceMatcher` ratio —
   `difflib` is stdlib, adds no new dependency). Flag pairs above a
   conservative similarity threshold (e.g. ratio > 0.75) as candidates,
   not certainties — the report should say "possible duplicate, human
   confirms" not "duplicate."
   **Gate:** unit test (see step 4) confirms it flags a synthetic pair
   like "fix(railway): require exact deployment proof" vs "fix(railway):
   trust CLI deployment ID before live SHA proof" style near-matches
   without false-flagging clearly unrelated titles.
4. Add `tests/test_triage_open_prs_staleness_and_duplicates.py` covering:
   `days_stale()` on a few fixed timestamps, `find_near_duplicate_titles()`
   on a small synthetic PR list including one confirmed-similar pair and
   one confirmed-dissimilar pair, and a smoke test that `main()` still
   returns 0 and writes `DEALIX_PR_TRIAGE=SKIPPED` when `gh` is mocked as
   unavailable (preserving the existing graceful-degradation contract).
   **Gate:** `python3 -m pytest tests/test_triage_open_prs_staleness_and_duplicates.py -q` → passes.
5. Add a "## Possible duplicates" section to `render_markdown()`'s output,
   listing each flagged pair with both PR numbers/titles and the
   similarity score, clearly labeled as a human-confirms suggestion.
   **Gate:** `grep -n "## Possible duplicates" scripts/triage_open_prs.py` → 1 match.
6. Update `docs/agents/PR_TRIAGE_POLICY.md` to describe the two new report
   sections (Stale, Possible duplicates) under a new "## Automated
   signals" heading, without changing the existing bucket table or the
   "humans decide" rule.
   **Gate:** `grep -n "Automated signals" docs/agents/PR_TRIAGE_POLICY.md` → 1 match.

## Done criteria (machine-checkable)
- [ ] `python3 -m pytest tests/test_triage_open_prs_staleness_and_duplicates.py -q` → passes
- [ ] `python3 scripts/triage_open_prs.py; echo $?` → `0` (whether or not
      `gh` is available in the execution environment — the skip path must
      still succeed)
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not merge, close, comment on, or modify any PR — this tool remains
  strictly read-only/reporting, per its own docstring and issue #938's
  explicit safety contract ("No merges without founder approval").
- Do not add branch-level (non-PR) scanning in this plan — issue #938 and
  this tool are PR-scoped; a separate branch-sprawl audit (hundreds of
  branches with no open PR) is a distinct, larger follow-up, not bundled
  here to keep this plan's diff reviewable.
- Do not change the existing 6 buckets or their classification rules —
  only add the two new report sections on top.
- Do not add a new external dependency — use stdlib `difflib` only.

## STOP conditions
- If `triage_open_prs.py`'s structure has changed substantially from the
  excerpts above → STOP, re-read the file fresh before adding functions
  in a different style than the rest of the file.
- If the duplicate-detection heuristic produces more than a handful of
  false positives when run against the real current open-PR set → STOP,
  raise the similarity threshold or narrow the normalization rather than
  shipping a noisy report section founders will learn to ignore.
