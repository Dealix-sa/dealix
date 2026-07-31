# 004 — Refresh CLAUDE.md's stale "Known Launch Status" block

- **Finding:** `CLAUDE.md:282-289` freezes a "Known Launch Status (2026-06-30)"
  block claiming Railway billing is past due and the production API is not
  live. `CLAUDE.md` itself was last edited 2026-07-26 (commit `1e441fe`,
  PR #859) without touching this block, and 59+ commits since 2026-06-30
  contradict it: `d34f942` "restore authoritative Railway deployment proof",
  `0152aa8` "verify CLI deploy SHA at live endpoint", `6adce26` "wire up
  billing API and tenant guards", `bb20792` "rebuild governed self-serve
  foundation". This is the file every Claude Code session reads first —
  a stale status here misleads every future session (including this one)
  about whether Railway/production is actually live.
- **Category:** doctrine
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read CLAUDE.md before editing
```

## Context (inlined)
- File in scope: `CLAUDE.md`
- Current state (excerpt, `CLAUDE.md:282-289`):
    ```markdown
    ## Known Launch Status (2026-06-30)

    - **Repo matrix:** PASS (all required gates green)
    - **Railway:** Billing past due — founder must pay to redeploy
    - **Frontend:** `npm --prefix apps/web run verify` PASS
    - **Production API:** Not yet live (Railway billing issue)
    - **Live outbound:** DISABLED (draft-only default)
    - **Secrets in repo:** NONE confirmed
    ```
- This plan does **not** ask the executor to guess the current Railway
  state (it cannot know that) — it asks the executor to (a) make the
  status block self-dating and easy to re-verify, and (b) explicitly mark
  the frozen claims as unverified since the stamped date, so nobody
  mistakes a month-old snapshot for current fact.

## Steps
1. In `CLAUDE.md`, replace the block at lines 282-289 with a version that
   keeps the same claims but adds a visible "last verified" stamp and a
   pointer to the live check commands, e.g.:
    ```markdown
    ## Known Launch Status

    **Last verified:** 2026-06-30 — re-run the checks below before trusting
    this block; do not assume it still holds.

    - **Repo matrix:** PASS as of last verification (all required gates green)
    - **Railway:** Billing past due as of last verification — founder must
      pay to redeploy. Re-check: `curl -fsS https://api.dealix.me/healthz`
    - **Frontend:** `npm --prefix apps/web run verify` PASS as of last verification
    - **Production API:** Not yet live as of last verification (Railway billing issue)
    - **Live outbound:** DISABLED (draft-only default) — verify via
      `curl -fsS https://api.dealix.me/api/status` (must show `external_send_enabled: false`)
    - **Secrets in repo:** NONE confirmed as of last verification — re-run
      `python3 scripts/ops/security_smoke_ci.py`
    ```
   Do not invent a new status (do not claim Railway is now live) — only
   add the staleness disclosure and re-verify pointers.
   **Gate:** `grep -n "Last verified" CLAUDE.md` → prints the new line.
2. Add one sentence to CLAUDE.md's "Verification Commands" section (around
   line 61-73) noting that the Known Launch Status block should be
   re-stamped whenever these commands are re-run with a different result.
   **Gate:** `grep -n "re-stamp" CLAUDE.md` → prints the new line.

## Done criteria (machine-checkable)
- [ ] `grep -c "Last verified" CLAUDE.md` → `1`
- [ ] `make full-repo-test` → all required gates PASS (this is a docs-only
      change; it must not alter behavior)

## Out of scope (do not touch)
- Do not change the actual claimed values (Railway/billing/secrets status) —
  this plan only makes the staleness visible, it does not re-verify Railway.
- Do not touch any other section of CLAUDE.md.

## STOP conditions
- If `CLAUDE.md:282-289` no longer matches the excerpt above → STOP,
  re-run drift check, the block may have already been refreshed.
- If asked to change the actual Railway/production claims → STOP, that
  requires the founder to run the live checks, not an executor guess.
