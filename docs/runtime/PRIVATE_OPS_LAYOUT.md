# Dealix Private Ops Runtime — Layout

This document describes the **runtime-only** filesystem layout that
backs Dealix sales + delivery operations. **No file under
`/opt/dealix-ops-private/` is ever committed to this repository.**
These files are **never committed**.

The runtime is bootstrapped by:

```
python scripts/bootstrap_private_ops_runtime.py
```

If the bootstrap script ever leaks paths into the repo, the verifier
`scripts/verifiers/verify_private_ops_runtime.py` will fail.

## Filesystem layout

```
/opt/dealix-ops-private/
├── README.md                       # founder-only operating notes
├── warm_list/
│   └── warm_list.csv               # contacts, hand-curated by founder
├── proof_packs/
│   └── <engagement_id>/
│       ├── source_passport.json
│       ├── findings.md
│       ├── proof_pack.pdf
│       └── capital_assets/
│           └── *.zip
├── value_ledger/
│   └── events.jsonl
├── audit_log/
│   └── <YYYY-MM-DD>.jsonl
├── approvals/
│   ├── pending/
│   └── decided/
├── secrets/                        # never written by scripts; founder-only
│   └── .env.private
└── backups/
    └── <YYYY-MM-DD>/
```

## File header conventions

- CSVs carry a header row with stable column names.
- JSONL files contain one object per line, sorted by timestamp on read.
- Every directory carries a `.gitignore` containing `*` so any accident
  is caught locally.

## Lifecycle

| Event | Trigger | Action |
|---|---|---|
| New engagement | dealix-delivery agent | `proof_packs/<engagement_id>/` created |
| Capital Asset shipped | dealix-delivery agent | Zip added to `capital_assets/` |
| Approval decision | approval-center-worker | Move file `pending/ -> decided/` |
| Daily audit | governance | Append to `audit_log/<YYYY-MM-DD>.jsonl` |

## Backup

- Daily snapshot copied to `/opt/dealix-ops-private/backups/<YYYY-MM-DD>/`.
- Weekly off-host copy to founder-controlled S3 (requires founder approval).
- Never auto-uploaded to a third party.

## Why this is **never** committed

These files contain:
- Customer PII (names, emails, phone, national-id fragments).
- Pricing + commercial terms per customer.
- Source passports listing approved data sources.
- Capital Assets that are customer-proprietary.

Committing them would violate NN6 (no PII in logs), NN1 (no scraping
without source passport), and the broader trust contract.

The bootstrap script creates the tree on a hardened host
(`/opt/dealix-ops-private/` is owned `root:dealix`, perms `750`).
