# 022 — Canonical first-ICP + 30-day discovery funnel doc (not a 6th ICP doc)

- **Finding:** Same sprawl pattern found in plans 013/014/021: **five**
  separate ICP documents already exist, none reflecting the narrow
  first-five-customer filter PR #1011 defines — `docs/company/ICP.md`
  (98 lines), `docs/commercial/ICP_MATRIX_AR.md` (224 lines, "توسيع
  `icp_primary.yaml` بمصفوفة شاملة لـ 10 شرائح B2B سعودية" — expands to
  **10 broad B2B segments**, the opposite of a narrow first-ICP),
  `docs/POSITIONING_AND_ICP.md` (137 lines, dated 2026-05-07),
  `docs/29_sales_os/ICP_SCORECARD.md` (14 lines, minimal), and
  `docs/targeting/ICP_SCORING_SYSTEM_AR.md` (123 lines, has an executable
  scorer: `scripts/icp_score_dry_run.py`). None of these currently encode
  PR #1011's specific guidance (branch
  `ops/founder-360-market-truth-20260731`, rewriting
  `docs/DEALIX_BUSINESS_MODEL.md`): focus the first five customers on
  Saudi B2B SaaS/business-services companies, ~20-200 employees,
  founder/GM-level decision access, a specific revenue-ops pain, usable
  data, willing to run a measured 30-day pilot — and explicitly *defer*
  banks, government, heavy enterprise transformation, and mass outbound
  until repeatability is proven. `docs/commercial/ICP_MATRIX_AR.md`'s
  10-segment breadth is the direct opposite of that discipline. Drafting a
  sixth ICP document would repeat the exact mistake; the actual gap is an
  **operational funnel checklist** translating the (soon-to-be-canonical)
  narrow ICP into day-by-day discovery actions, which none of the five
  existing docs provide — they're all profile/scoring docs, not funnel
  operating docs. `sales/DISCOVERY_CALL_SCRIPT_AR.md` already exists as
  the call-script half of this; there's no funnel-stage/qualification-gate
  doc alongside it.
- **Category:** docs / sales
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-check whether PR #1011 has merged and whether any of the 5 ICP docs have since been updated
```

## Context (inlined)
- New file to add: `sales/FIRST_ICP_DISCOVERY_FUNNEL_AR.md`.
- Files to annotate (pointer only, not rewrite): `docs/company/ICP.md`,
  `docs/commercial/ICP_MATRIX_AR.md`, `docs/POSITIONING_AND_ICP.md`,
  `docs/29_sales_os/ICP_SCORECARD.md`, `docs/targeting/ICP_SCORING_SYSTEM_AR.md`.
- If PR #1011 has merged by execution time, cross-reference
  `docs/DEALIX_BUSINESS_MODEL.md`'s ICP section directly instead of
  restating it. If it hasn't merged yet, inline the specific facts listed
  in the Finding above (they were read directly from #1011's diff during
  this audit, not copied from an assumption) rather than leaving a
  dangling reference to an unmerged doc.
- Do not touch `scripts/icp_score_dry_run.py` or its schema/template —
  those are a separate scoring mechanism that can stay as-is; this plan
  only adds the missing funnel-operations layer on top.

## Steps
1. Write `sales/FIRST_ICP_DISCOVERY_FUNNEL_AR.md` covering exactly:
   - The narrow first-ICP filter (from the Finding above / #1011).
   - The explicit defer list (banks, government, heavy enterprise,
     anonymous mass outbound, guaranteed-revenue requests).
   - The 30-day funnel stages: 30 legitimate target accounts (sourced from
     network/referrals, no scraping) → 10 discovery conversations → 3
     qualified pilot opportunities → 1 paid pilot.
   - The qualification exit criteria a lead must meet before being called
     "qualified": specific pain, accountable decision owner, lawfully
     usable data, measurable baseline possible, willingness to accept
     approval gates, budget/timing discussed, no guarantee/compliance-
     bypass request.
   - A cross-reference to `sales/DISCOVERY_CALL_SCRIPT_AR.md` for the
     call script itself (do not duplicate its content).
   Use hypothesis language throughout per
   `.claude/rules/dealix-commercial-os.md` ("نتوقع" / "we expect", never
   "مضمون" / guaranteed).
   **Gate:** `wc -l sales/FIRST_ICP_DISCOVERY_FUNNEL_AR.md` → file exists,
   non-trivial length (expect 60-120 lines, not a stub).
2. Add a one-line pointer near the top of each of the 5 existing ICP docs
   noting they describe a broader/future-state ICP and pointing at the
   new funnel doc for the current first-five-customer filter, e.g.:
    ```markdown
    > **Current launch phase:** the active filter for the first five
    > customers is narrower than this document — see
    > `sales/FIRST_ICP_DISCOVERY_FUNNEL_AR.md`.
    ```
   Do not delete or rewrite the body of any of the 5 docs — they may still
   be useful for later, broader-market phases.
   **Gate:** `grep -l "FIRST_ICP_DISCOVERY_FUNNEL_AR" docs/company/ICP.md docs/commercial/ICP_MATRIX_AR.md docs/POSITIONING_AND_ICP.md docs/29_sales_os/ICP_SCORECARD.md docs/targeting/ICP_SCORING_SYSTEM_AR.md | wc -l` → `5`.

## Done criteria (machine-checkable)
- [ ] `test -f sales/FIRST_ICP_DISCOVERY_FUNNEL_AR.md`
- [ ] `grep -l "FIRST_ICP_DISCOVERY_FUNNEL_AR" docs/company/ICP.md docs/commercial/ICP_MATRIX_AR.md docs/POSITIONING_AND_ICP.md docs/29_sales_os/ICP_SCORECARD.md docs/targeting/ICP_SCORING_SYSTEM_AR.md | wc -l` → `5`
- [ ] `python3 -m pytest tests/test_no_guaranteed_claims.py -q` → passes unchanged (new doc must not trip doctrine language if that test scans `sales/`; confirm scope first)
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not create a 6th standalone ICP scoring/matrix document — extend/
  point at the existing 5, add only the funnel-operations layer that's
  genuinely missing.
- Do not touch `scripts/icp_score_dry_run.py`, its schema, or example
  template.
- Do not touch `sales/DISCOVERY_CALL_SCRIPT_AR.md`'s content — cross-
  reference it, don't duplicate or rewrite it.
- Do not name specific target companies or prospects in the new doc — it's
  a process/criteria document, not a lead list.

## STOP conditions
- If PR #1011 has merged by execution time and
  `docs/DEALIX_BUSINESS_MODEL.md`'s actual merged ICP section differs from
  the Finding's description above (re-derived from the pre-merge diff) →
  STOP, re-read the merged file and use its exact language instead.
- If `tests/test_no_guaranteed_claims.py` or any other doctrine guard test
  scans `sales/*.md` content and the new file trips it → STOP, revise the
  new doc's language rather than modifying the test.
