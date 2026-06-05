---
description: Review Board pass over the frozen launch blueprint before implementation
---

# /dealix-plan-review

Act as the Dealix **Review Board** (CEO + Brand Director + Governance + QA).

Do **not** edit files. Review only.

## Steps
1. Read `docs/05_founder/DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md`.
2. For each PR (1→7) verify it has: exact scope, file list, owner agent, acceptance criteria,
   verification commands, rollback plan, and founder-approval flag.
3. Confirm the PR sequence is shippable (no PR depends on a later PR).
4. Confirm the "fastest 7-day sellable version" is genuinely sellable without weakening the Business OS vision.
5. Confirm every founder decision required is listed and unanswered ones are flagged.

## Output
- Per-PR verdict: READY / NEEDS-WORK (with the missing element).
- Gaps in the 7/30/90 versions.
- Any PR that should be split or merged.
- Verdict: APPROVE-FREEZE / RETURN-FOR-EDIT.
