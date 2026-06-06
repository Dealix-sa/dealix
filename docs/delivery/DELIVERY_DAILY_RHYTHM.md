# Delivery Daily Rhythm — الإيقاع اليومي للتسليم

The repeatable cadence that keeps every active engagement moving without the
founder having to remember state. One pass, every working day.

## Morning (15 min)

1. Run `python scripts/founder_daily_command.py`.
2. Read `reports/founder/daily_command.md` — note the single recommended action.
3. For each active customer in `customers/`, open `07_next_action_board.md` and
   confirm today's one move.

## Midday (per active engagement)

- Do the one move. Update the relevant workspace file.
- Append a one-line entry to `09_delivery_log.md` (what changed, what's next).
- If anything needs to leave the building → **draft only**, queue it in
  `06_approval_register.md`. Never send (non-negotiable #8).

## End of day (10 min)

- Update `data/revenue/pipeline.jsonl` with any stage changes.
- If a Proof Pack reached score ≥ 70, register the Capital Asset in
  `data/revenue/proof_assets.jsonl`.
- Re-run `python scripts/founder_daily_command.py` so tomorrow starts clean.

## Guardrails

- No engagement sits > 24h without a delivery-log entry.
- No paid engagement closes without a Proof Pack + Capital Asset.
- No external send without approval.

## Weekly roll-up

The week's rhythm feeds the [Weekly CEO Review](../founder/WEEKLY_CEO_REVIEW.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
