# Outbound Draft Machine

| Field | Value |
|---|---|
| Purpose | Produce personalised outbound email drafts per scored account |
| Inputs | `growth/account_scores.csv`, `growth/buyer_personas.csv`, trigger events, suppression list |
| Outputs | `outreach_queue.csv` (draft rows), audit events |
| Source | First-party signal preferred; fallback datasets carry `source=fallback` |
| Approval class | External send — founder approval required |
| Trust gate | Brand check, suppression check, bilingual symmetry check |
| Owner | Distribution Operator agent |
| Worker | `worker_outbound_draft` (scheduled, see Worker Orchestrator) |
| KPI | Reply quality, cash-per-send, brand-pass rate |
| Failure mode | Brand check fails → draft returned to agent with diff |
| Recovery | Eval Guardian re-runs voice eval; founder is notified on second failure |

## Draft contract

```yaml
queue: outreach_queue
fields:
  - draft_id
  - account_id
  - persona_id
  - sector_id
  - subject_en
  - subject_ar
  - body_en
  - body_ar
  - personalisation_evidence  # citations to triggers / signals
  - suppression_check         # pass / fail / unknown
  - brand_check               # pass / fail / unknown
  - trust_check               # pass / fail / unknown
  - status                    # draft | approved | declined | deferred | sent
  - created_at
  - source
```

## Forbidden in drafts

- Any guaranteed-result language.
- Any claim without an evidence citation.
- Any image attachment.
- Any non-Dealix-domain link.
- Any personalisation token unresolved.

## Send

Sending is a separate operator action, performed manually after `/approvals` approval. The Outbound Draft Machine itself never opens a network socket to any external SMTP or email provider.
