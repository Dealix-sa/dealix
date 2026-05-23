# Private Ops Runtime Contract

The private ops tree lives at `$DEALIX_PRIVATE_OPS`
(default `/opt/dealix-ops-private`). It is **never committed** to the
public repo. The shape is enforced by
`scripts/bootstrap_private_ops_runtime.py` and read by
`api/internal/runtime_reader.py`.

## Directories

```
intelligence/lead_intelligence_base.csv
outreach/outreach_queue.csv
outreach/conversation_log.csv
outreach/suppression_list.csv
approvals/approval_queue.csv
trust/approval_decisions.csv
trust/trust_flags.csv
trust/agent_toggles.csv
sales/proposal_queue.csv
finance/payment_capture_queue.csv
finance/cash_collected.csv
runtime/worker_state.csv
distribution/channel_scorecard.csv
distribution/sector_scorecard.csv
delivery/delivery_queue.csv
retention/retention_queue.csv
proof/proof_library.csv
evals/eval_status.csv
product/productization_candidates.csv
security/security_status.csv
founder/operating_scorecard.md
```

Missing files return safe empty structures with `source: "fallback"`.
