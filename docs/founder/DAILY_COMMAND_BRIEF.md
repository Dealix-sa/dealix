# Daily Command Brief — Template

> Generated nightly by the Founder Brief Agent. Read first thing in the morning.
> Never edit the historical briefs — only the template here.

## Format

```markdown
# Daily Founder Brief — YYYY-MM-DD

## 1. Money
- Cash collected today: SAR _____
- Cash collected MTD:   SAR _____
- Proposals pending:    _____ (value SAR _____)
- Payments overdue:     _____ (oldest _____ days)
- MRR:                  SAR _____
- Runway:               _____ months

## 2. Pipeline
- New leads added:        _____
- Contacted today:        _____
- Replies received:       _____ (rate _____%)
- Calls booked:           _____
- Proposals sent:         _____
- Stage transitions:      _____ → _____

## 3. Delivery
- Active clients:         _____
- Reports due today:      _____
- Risks flagged:          _____
- Waiting on founder:     _____ items

## 4. Trust
- Opt-outs received:      _____
- Risk flags raised:      _____
- Claims needing approval:_____
- Data incidents:         _____ (target: 0)
- A3-blocked actions:     _____ (expected: 0 unless test)

## 5. CEO Decisions (queue)
- Approve: ___ (link to draft)
- Reject:  ___ (with reason template)
- Build:   ___ (passes Strategy Filter?)
- Defer:   ___ (revisit date required)
- Kill:    ___ (one-line reason required)

## 6. One Focus Today
> The single highest-leverage action. Not three. One.

[__________________________________]
```

## Generation Rules

The brief is assembled by `scripts/generate_founder_brief.py` (when present) from:

| Section | Source |
|---|---|
| Money | `revenue/mrr_tracker.csv`, `revenue/cash_collected.csv` (private repo) |
| Pipeline | `pipeline/pipeline_tracker.csv` (private repo) |
| Delivery | `delivery/active_sprints/*.md` (private repo) |
| Trust | `trust/approval_log.csv`, `trust/data_incidents.md` (private repo) |
| Decisions | Open PRs + agent approval queue |
| Focus | Founder-set, pulled from `FOCUS_POLICY.md` |

If a source is missing, the brief includes a `MISSING:` flag instead of guessing.

## Reading Discipline

- Read top-to-bottom, in order, once.
- Do not jump to "what's interesting" — money first, always.
- If section 6 (One Focus) is empty, **fill it before doing anything else**.
- The brief is read-only. Capture decisions in `decision_log.md`, not here.

## When The Brief Lies

If the numbers feel wrong:
1. Check the source CSV directly
2. Don't "correct" the brief — fix the source
3. Log a `learning_os` ledger entry: "brief generator drifted, fixed source"
