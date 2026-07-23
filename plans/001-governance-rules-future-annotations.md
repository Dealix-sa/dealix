# 001 — `from __future__ import annotations` on governance rule mirrors

- **Finding:** The engineer quality bar requires `from __future__ import
  annotations` on all modules, but six governance rule mirrors omit it:
  `auto_client_acquisition/governance_os/rules/{pii_requires_review,
  external_action_requires_approval,no_guaranteed_claims,no_linkedin_automation,
  no_cold_whatsapp,no_scraping}.py`. They are part of the guarded doctrine
  surface, so consistency here matters more than in a throwaway script.
- **Category:** tech-debt   **Wave:** maintenance
- **Effort:** S   **Confidence:** MED  *(cosmetic — these files currently carry
  no type annotations, so the import is consistency-only, not a bug fix)*
- **Written against commit:** 2ec6a6c
- **Status:** 📋 TODO — good first task for a cheap executor: mechanical, gated,
  zero behavioral change.

## Drift check (run first)
```bash
git rev-parse HEAD
for f in auto_client_acquisition/governance_os/rules/pii_requires_review.py \
         auto_client_acquisition/governance_os/rules/external_action_requires_approval.py \
         auto_client_acquisition/governance_os/rules/no_guaranteed_claims.py \
         auto_client_acquisition/governance_os/rules/no_linkedin_automation.py \
         auto_client_acquisition/governance_os/rules/no_cold_whatsapp.py \
         auto_client_acquisition/governance_os/rules/no_scraping.py; do
  grep -q 'from __future__ import annotations' "$f" && echo "ALREADY $f"
done   # any ALREADY output → that file was fixed independently; skip it
```

## Current state (excerpt — the pattern to preserve)
```python
# auto_client_acquisition/governance_os/rules/no_cold_whatsapp.py:1-3
"""Programmatic mirror of declarative rule: no cold WhatsApp."""

RULE_SLUG = "no_cold_whatsapp"
```

## Steps
For each of the six files: insert `from __future__ import annotations` as the
first statement **after** the module docstring, separated by one blank line
before the existing code. Do not reorder or touch `RULE_SLUG` or any logic.

**Gate (per file):** `python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" <file>` → exit 0.

## Done criteria (machine-checkable)
- [ ] All six files contain `from __future__ import annotations`.
- [ ] `python3 -m compileall -q auto_client_acquisition/governance_os` → exit 0
- [ ] Doctrine guards still green:
      `tests/test_no_cold_whatsapp.py`, `tests/test_no_guaranteed_claims.py`,
      `tests/test_no_linkedin_automation.py`, `tests/test_no_scraping_engine.py`

## Out of scope
- Do NOT add type annotations to these files in the same change.
- Do NOT touch any other module under `governance_os/`.

## STOP conditions
- If inserting the import changes any doctrine test result → STOP, revert, report.
  The import is a no-op; a failure means something else is wrong.
- If a file has no module docstring → put the import on line 1, then report the
  missing docstring separately (do not write one).
