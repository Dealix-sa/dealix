# Campaign Factory

> A single discipline for turning a sector + offer + channel into a
> measurable campaign with explicit approval, assets, queue, and
> results.

## CSV schemas

### `<PRIVATE_OPS>/campaigns/campaign_registry.csv`

```
campaign_id,name,sector,offer,channel,goal,approval_class,owner,
status,start_date,end_date,next_action
```

- `approval_class` ∈ {`founder_only`, `founder_review`, `governance`,
  `partner_and_founder`}.
- `status` ∈ {`draft`, `pending_approval`, `live`, `paused`,
  `complete`, `killed`}.

### `<PRIVATE_OPS>/campaigns/campaign_assets.csv`

```
asset_id,campaign_id,type,title,status,approval_status,proof_status,
risk_level,next_action
```

- `type` ∈ {`post`, `one_pager`, `sample`, `proposal_template`,
  `webinar_deck`, `event_card`, `email_template`, `report`}.
- `proof_status` ∈ {`n_a`, `evidence_required`, `evidence_attached`,
  `proof_pack_signed`}.

### `<PRIVATE_OPS>/campaigns/campaign_queue.csv`

```
queue_id,campaign_id,channel,target_segment,message_or_asset,
approval_status,send_status,next_action
```

- `send_status` ∈ {`queued`, `approved`, `sent`, `held`, `rejected`}.
- Nothing leaves `queued` without an explicit founder approval row.

### `<PRIVATE_OPS>/campaigns/campaign_results.csv`

```
date,campaign_id,channel,impressions,clicks,replies,positive_replies,
samples,proposals,payments,learning,next_action
```

## Generator

`scripts/generate_campaign_command_report.py` reads the four CSVs
above and writes `<PRIVATE_OPS>/campaigns/campaign_command_report.md`.

## Approval flow (campaigns)

1. Founder drafts a campaign → row in `campaign_registry.csv`,
   `status=draft`.
2. Assets created → `campaign_assets.csv`, `status=draft`,
   `approval_status=pending`.
3. Assets reviewed → `approval_status=approved`, `proof_status` set.
4. Queue rows added → `campaign_queue.csv`, `send_status=queued`.
5. Founder approves a batch → `send_status=approved`.
6. Sending happens (manual or through an approved channel).
7. Results captured nightly into `campaign_results.csv`.
