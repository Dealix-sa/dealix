# Private Ops Runtime Contract

The Founder Console requires a private ops tree on disk. Default root
is `/opt/dealix-ops-private`, overridable via `DEALIX_PRIVATE_OPS`.

## Bootstrap

```
make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private
# or
python scripts/bootstrap_private_ops_runtime.py --private-ops /opt/dealix-ops-private
```

## File tree

```
${DEALIX_PRIVATE_OPS}/
  intelligence/lead_intelligence_base.csv
  outreach/outreach_queue.csv
  outreach/conversation_log.csv
  outreach/suppression_list.csv
  approvals/approval_queue.csv
  trust/approval_decisions.csv      # APPEND-ONLY AUDIT
  trust/trust_flags.csv
  sales/proposal_queue.csv
  finance/payment_capture_queue.csv
  finance/cash_collected.csv
  runtime/worker_state.csv
  distribution/channel_scorecard.csv
  distribution/sector_scorecard.csv
  evals/eval_status.csv
  product/productization_candidates.csv
  security/security_status.csv
  founder/operating_scorecard.md    # generated
```

## Header contract

Header sets are codified in
`api.internal.runtime_reader.RUNTIME_FILES` and in
`scripts/bootstrap_private_ops_runtime.py`. Both must stay in sync.

## Append-only rule

`trust/approval_decisions.csv` is append-only. Workers and the internal
API must use `runtime_reader.append_runtime("approval_decisions", ...)`
and never overwrite existing rows.
