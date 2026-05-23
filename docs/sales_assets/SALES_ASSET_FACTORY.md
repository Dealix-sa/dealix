# Sales Asset Factory

> Where sector one-pagers, samples, proposal templates, and objection
> responses are produced under proof-safe rules.

## Directory layout

```
assets/sales/
├── one_pagers/        # sector-specific one-pagers
├── proposals/         # proposal templates (no signed contracts here)
├── samples/           # proof-safe sample artifacts
├── objections/        # objection response sheets
└── proof_safe/        # the curated proof index (links to proof-pack registry)
```

## CSV (source of truth)

`<PRIVATE_OPS>/sales_assets/sales_asset_registry.csv`

```
asset_id,type,sector,offer,title,status,approval_status,
proof_status,risk_level,file_path,next_action
```

- `type` ∈ {`one_pager`, `proposal`, `sample`, `objection`,
  `proof_safe`, `case_study_outline`}.
- `status` ∈ {`draft`, `review`, `approved`, `champion`, `retired`}.
- `risk_level` ∈ {`low`, `medium`, `high`, `governance_review`}.

## Verifier

`scripts/verify_sales_asset_system.py` checks:

- All listed `file_path` values exist (or the row is marked `draft`).
- No asset includes any of the banned phrases (we never promise
  outcomes, see `PROOF_SAFE_ASSET_POLICY.md` for the full list) in
  title or first 500 bytes of file content.
- Every `approved` asset has `proof_status != evidence_required`.
- Directory layout exists.

## Run

```bash
make sales-assets
```
