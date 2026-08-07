# Plan template

Copy this into `plans/NNN-<slug>.md`. Written for the **weakest plausible
executor** — a small model that never saw the advisor session. Three properties
carry that: self-contained, verification gates, hard boundaries.

```markdown
# NNN — <imperative title, <72 chars>

- **Finding:** <one line — what's wrong and where, with file:line>
- **Category:** correctness | doctrine | security | perf | tests | debt | docs | direction
- **Wave:** <Wave N from the roadmap, or "maintenance">
- **Effort:** S | M | L   **Confidence:** HIGH | MED | LOW
- **Written against commit:** <git rev-parse HEAD>

## Drift check (run first)
```bash
git rev-parse HEAD   # if != <commit above>, re-read the files below before editing
```

## Context (inlined — no "as discussed above")
- Files in scope: `path/a.py`, `path/b.py`
- Current state (excerpt):
    ```python
    # path/a.py:40-52  (current code, pasted so the executor need not hunt)
    ...
    ```
- Repo conventions to mirror: `from __future__ import annotations`; type hints on
  all public functions; pure-function core + thin router; no emojis, no model
  name, no marketing copy in code comments. Exemplar to copy the style of:
  `auto_client_acquisition/value_os/value_ledger.py`.

## Steps
1. <exact edit — file, what to change, to what>.
   **Gate:** `python3 -m pytest tests/<file> -q` → `N passed`.
2. <next edit>.
   **Gate:** `<command>` → `<expected output>`.
3. Add a test for every new public function.
   **Gate:** `python3 -m pytest tests/<new_test> -q` → passes.

## Done criteria (machine-checkable — executor never judges success)
- [ ] `make full-repo-test` → all required gates PASS
- [ ] `npm --prefix apps/web run verify` → PASS  *(only if apps/web changed)*
- [ ] `python3 scripts/verify_no_auto_external_send.py` → exit 0

## Out of scope (do not touch)
- <explicit list — files/areas the executor must leave alone>

## STOP conditions (report, do not improvise)
- If any doctrine guard test fails → STOP, report; do not edit the test.
- If the change would require flipping an `*_SEND_ENABLED` flag or editing
  `_validate_production_secrets` → STOP, escalate to founder.
- If current code doesn't match the excerpt above → STOP, re-run drift check.
- If a done-criterion command doesn't exist as written → STOP, report.
```

## Why each property matters
- **Self-contained** — the executor has no session memory; inline every path,
  excerpt, convention, and verified command.
- **Verification gates** — every step ends in a command + expected output, so
  "done" is machine-checkable, not a judgment call.
- **Hard boundaries** — explicit out-of-scope + STOP conditions stop a small
  model from improvising when reality diverges from the plan.
