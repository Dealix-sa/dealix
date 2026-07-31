# 006 — Remove guaranteed-outcome language from founder execution docs

- **Finding:** `README_FOUNDER_EXECUTION.md` and `FOUNDER_QUICK_REFERENCE.txt`
  contain outcome-as-certainty language that violates the repo's own
  "Claim rules — NON-NEGOTIABLE" (`.claude/rules/dealix-commercial-os.md`:
  "No guaranteed ROI claims... Use hypothesis language only... NOT
  'مضمون' / NOT 'guaranteed'"):
  - `README_FOUNDER_EXECUTION.md:411`: "Deliver 1 end-to-end, and renewal is
    80% likely." — an invented statistic; no data source anywhere in the
    repo supports an 80% renewal rate (the repo has zero customers per its
    own "Known Launch Status").
  - `README_FOUNDER_EXECUTION.md:412`: "By Day 90, you'll have 12+ customers
    and 20K+ SAR MRR. You'll be a real company." — stated as a near-certain
    outcome of following the playbook, not a target/hypothesis.
  - `README_FOUNDER_EXECUTION.md:409`: "Send 5 per week, and you'll have 3
    pilots by Day 30." — same pattern, causal certainty with no basis.
  This is the exact pattern `.claude/rules/dealix-commercial-os.md` and
  CLAUDE.md's "What NOT to Do" (line ~301: "Do not generate fake ROI
  numbers... or guaranteed ROI claims") forbid — and it's happening inside
  the repo's own internal playbook, not just customer-facing copy.
- **Category:** doctrine
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read the files below before editing
```

## Context (inlined)
- Files in scope: `README_FOUNDER_EXECUTION.md`, `FOUNDER_QUICK_REFERENCE.txt`
- Current state (`README_FOUNDER_EXECUTION.md:405-414`):
    ```markdown
    You have everything you need. The system is ready. The market is ready.

    What you need now is courage to send 1 WhatsApp.

    Send 5 per week, and you'll have 3 pilots by Day 30. Deliver 1 end-to-end, and renewal is 80% likely.

    By Day 90, you'll have 12+ customers and 20K+ SAR MRR. You'll be a real company.

    But it all starts with one WhatsApp tomorrow at 8:15 AM.

    Go.
    ```
- Required tone, per `.claude/rules/dealix-commercial-os.md` "Language
  rules": use "نتوقع / we expect", "الهدف هو / the goal is", "سنقيس / we
  will measure" — never "مضمون / guaranteed" or stated-as-fact outcomes.

## Steps
1. Rewrite `README_FOUNDER_EXECUTION.md:405-414` to hypothesis language,
   keeping the same structure and motivational intent but removing invented
   statistics and certainty framing, e.g.:
    ```markdown
    You have everything you need. The system is ready.

    What you need now is to send 1 WhatsApp.

    The goal: send 5 per week and reach 3 pilots by Day 30 — this is a
    target based on the funnel assumptions in this playbook, not a
    guarantee. Track actual conversion in `company/crm/` and update the
    assumptions as real data comes in.

    The Day 90 target is 12+ customers and 20K+ SAR MRR — we'll measure
    against this weekly, not assume it.

    It starts with one WhatsApp tomorrow at 8:15 AM.
    ```
   **Gate:** `grep -n "80% likely\|you'll be a real company" README_FOUNDER_EXECUTION.md` → no output.
2. Scan `README_FOUNDER_EXECUTION.md` and `FOUNDER_QUICK_REFERENCE.txt` in
   full for any other "and you'll have X" / "guaranteed" / invented
   percentage patterns not already covered by step 1, and apply the same
   hypothesis-language rewrite.
   **Gate:** `grep -niE "guaranteed|% likely|you'll have|you'll be" README_FOUNDER_EXECUTION.md FOUNDER_QUICK_REFERENCE.txt` → no output (except inside a code block showing the "before" text as a documented anti-pattern, if any).
3. Re-run the repo's own doctrine test for this rule to confirm it wasn't
   already covering these files (it isn't — `tests/test_no_guaranteed_claims.py`
   checks structured governance output, not internal markdown playbooks —
   confirm this and do not attempt to add these files to that test's scope
   unless the finding specifically says so).
   **Gate:** `python3 -m pytest tests/test_no_guaranteed_claims.py -q` → passes, unchanged.

## Done criteria (machine-checkable)
- [ ] `grep -rniE "guaranteed|% likely renewal" README_FOUNDER_EXECUTION.md FOUNDER_QUICK_REFERENCE.txt` → no output
- [ ] `python3 -m pytest tests/test_no_guaranteed_claims.py -q` → passes
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not touch `tests/test_no_guaranteed_claims.py` itself.
- Do not touch `sales/` templates — those are customer-facing and already
  reviewed under `.claude/rules/dealix-commercial-os.md`; if the same
  pattern exists there, report it as a new finding rather than editing
  inline (customer-facing copy changes should go through `dealix-content`).

## STOP conditions
- If the excerpted lines have already been edited (don't match the excerpt
  above) → STOP, re-run drift check before editing.
- If removing a stated number would require inventing a replacement
  statistic → STOP; use hedged language ("the goal is") instead, never
  substitute one invented number for another.
