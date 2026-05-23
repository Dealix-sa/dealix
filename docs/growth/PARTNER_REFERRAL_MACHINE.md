# Partner Referral Machine

## purpose
Turn approved partners into a structured referral stream — with
attribution, drafts, and a transparent reward record.

## inputs
- `data/private_ops_seed/growth/partners.csv` (named partners with consent).
- `growth/account_scores.csv` (warm-intro candidates).

## outputs
`distribution/partner_referrals.csv`:
```
referral_id,partner_id,account_id,intro_draft,
expected_value_band,status,attribution,created_at
```

## source
- Partner-provided account names + customer consent.
- Never scraped.

## approval_class
per-referral.

## trust_gate
- Partner is informed in advance and consents to the program.
- Each intro draft is approved by the founder before it goes to the
  partner.
- Reward record is tracked in `governance/partner_rewards.csv`
  (not in this repo; in the private ops volume).

## owner
growth_strategist → founder.

## worker
`distribution_partner_referral_worker`.

## KPI
- Referrals per partner per quarter.
- Convert rate from referral → meeting.
- Partner satisfaction signal (qualitative ledger).

## failure_mode
- Partner over-asked.
- Off-segment intro suggested.

## recovery_path
- Density throttle per partner.
- Segment filter on candidates.

## kill_switch
`make growth-kill-partner-referral`.

## audit
`audit/distribution_partner_referral_runs.jsonl`.
