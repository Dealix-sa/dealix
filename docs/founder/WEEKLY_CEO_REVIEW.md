# Weekly CEO Review — Template

> Run every Sunday before bed. Cannot be skipped two weeks in a row.
> Output: one updated scorecard set, one decision row, one focus refresh.

## Format

```markdown
# Weekly CEO Review — Week ending YYYY-MM-DD

## Revenue
- Cash collected this week:   SAR _____
- New customers:              _____
- MRR delta:                  +/- SAR _____
- Pipeline value:             SAR _____
- Close rate:                 _____%

## GTM
- Best channel this week:     _____
- Best sector this week:      _____
- Best message this week:     _____ (link)
- Biggest objection:          _____
- Cost per booked call:       SAR _____

## Delivery
- Reports delivered:          _____
- Average delivery time:      _____ days
- QA failures:                _____
- Client feedback (avg /10):  _____
- Rework count:               _____

## Product
- Features shipped:           _____
- Bugs fixed:                 _____
- Features deferred:          _____ (with revisit date)
- Customer-requested:         _____
- Build-Defer-Kill ratio:     ___ / ___ / ___

## Trust
- Approval escalations:       _____
- Opt-outs:                   _____
- Incidents:                  _____ (target: 0)
- Claims reviewed:            _____
- Public safety pass:         ✅ / ❌
- A3-blocked actions:         _____

## Learning
- What worked:                _____
- What failed:                _____
- What to double down on:     _____
- What to stop:               _____

## Scorecards (out of 100)
- Founder OS:                 _____
- Strategy OS:                _____
- Revenue OS:                 _____
- Acquisition OS:             _____
- Delivery OS:                _____
- Product OS:                 _____
- Trust OS:                   _____
- Finance OS:                 _____
- Client Success OS:          _____
- Content OS:                 _____
- People OS:                  _____
- Learning OS:                _____

## CEO Decision This Week
- BUILD:  _____ (passes Strategy Filter test #__)
- FIX:    _____
- KILL:   _____ (one-line reason)
- DEFER:  _____ (revisit by YYYY-MM-DD)

## Next Week's One Focus
> Singular. Measurable. Reversible if wrong.

[__________________________________]
```

## Rules

- Fill every field. If a number is unknown, write `unknown — fix source by [date]`.
- No section may be marked "n/a" two weeks in a row.
- The KILL row cannot be empty. If you killed nothing this week, you are over-committed.
- The Next Week's One Focus must connect to the One Focus from last week (either continue, complete, or explicitly pivot).

## Storage

- Each completed review goes to `weekly_reviews/YYYY-MM-DD.md` in the **private repo**.
- Aggregate scorecard trends go to `docs/learning/MONTHLY_STRATEGY_UPDATE.md` (public, sanitized).
- Decisions get appended to `DEALIX_EXECUTION_LEDGER.md` and `founder/decision_log.md`.

## When To Skip

Never. The review takes 45 minutes. Skipping it costs more than running it.

If you genuinely cannot complete it, fill in:
- The three numbers you do know
- Mark all unknowns with `BLOCKED: <why>`
- Schedule the unblock in next week's One Focus.
