# Strategic Account Attack Plan

> Companion to `STRATEGIC_ACCOUNT_LIST_SYSTEM.md`. Defines *how* the
> Strategic Account List gets attacked, not just maintained.

## Tiers

| Tier | Definition                                                          | Cadence                       |
| ---- | ------------------------------------------------------------------- | ----------------------------- |
| T0   | Trigger fired (funding, hiring, RFP, new exec, regulation)          | act within 7 days             |
| T1   | High-fit, warm path exists                                          | 1 touchpoint / 2 weeks        |
| T2   | High-fit, no warm path                                              | nurture via authority content |
| T3   | Watchlist                                                           | quarterly check               |

## Attack rules

1. Every T0/T1 account has a named `relationship_path` — partner,
   referrer, event, or warm intro. If empty, the account is demoted to T2.
2. Every touchpoint produces a row in `outreach/conversation_log.csv`
   with `approval_status = approved` before sending.
3. After 3 touchpoints with no positive reply, the account moves to
   `nurture` and we stop pushing.
4. After a positive reply, the account moves to the `sales` workflow
   (proposal → sample → close).
5. No T0/T1 account proceeds to "proposal" without an approved
   `proof_safe` asset attached.

## Inputs and outputs

- Generator reads (when present): `growth/account_scores.csv`,
  `growth/lead_intelligence.csv`, `growth/sector_targets.csv`,
  `outreach/conversation_log.csv`.
- Writes `<PRIVATE_OPS>/market_attack/strategic_account_attack_plan.md`
  (this is produced by `scripts/generate_strategic_account_list.py`).
- Source of truth: `<PRIVATE_OPS>/market_attack/strategic_accounts.csv`.
