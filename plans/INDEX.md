# Improvement backlog — INDEX

Seeded by the first `improve` audit against commit `2ec6a6c`
(`.claude/skills/improve/`). Findings are vetted (every `file:line` re-read
before listing). This is a living backlog — refresh with `/improve reconcile`.

## Priority order

| # | Plan | Category | Effort | Confidence | Wave | Status |
|---|------|----------|--------|-----------|------|--------|
| 002 | [Provider registry freshness guard](002-provider-registry-freshness-guard.md) | doctrine/DX | S | HIGH | maintenance | ✅ DONE (this PR) |
| 003 | [Catalog the 57 verify_*.py scripts](003-verify-scripts-catalog.md) | docs/DX | S | HIGH | maintenance | 📋 TODO |
| 001 | [`__future__` annotations on governance rule mirrors](001-governance-rules-future-annotations.md) | tech-debt | S | MED | maintenance | 📋 TODO |

## Dependency notes
- All three are independent; each can be executed on its own branch.
- 002 landed directly in this PR (see `scripts/ops/check_provider_registry_freshness.py`
  + `tests/test_provider_registry_freshness.py`). Kept here as the canonical
  worked example of a closed audit→plan→execute→verify loop.

## Rejected findings (recorded so they don't resurface)
- **[GI-01] `!scripts/lib/` / `!apps/web/lib/` gitignore negations** — looked like
  the same broken-parent bug as `.claude/`, but the parent dirs (`scripts/`,
  `apps/web/`) are **not** wholesale-ignored, so re-inclusion works
  (`git check-ignore scripts/lib/... ` → trackable). By-design. Not a finding.
- **[FUT-02] `from __future__ import annotations` missing repo-wide** — only
  flagged where it actually matters (see 001, scoped to the doctrine mirrors that
  are part of a guarded surface). Not raised as a blanket 1000-file sweep — that
  would be churn without evidence of harm.
