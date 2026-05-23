# private_ops — Local Operating Templates

This directory holds the operational templates Dealix uses to actually run client
engagements. It mirrors the structure of the separate `dealix-ops-private`
repository so the same paths work in both places.

## Why It Lives Here
The public Revenue Sprint Kit (under `docs/offers/revenue_sprint/`) describes
the system and the rules. The actual day-to-day artifacts — founder DMs,
sample packs, proposals, intake forms, delivery reports — live here as
templates so contributors can run the playbook without leaving the repo.

## Rules
- **Never** commit real client data here. These are templates only.
- Per-client copies (filled-out intakes, real lead tables, signed proposals)
  belong in the private operations repository, not in this directory.
- Any addition or change here must keep the file shape compatible with the
  private repo so the playbooks stay portable.

## Layout
```
private_ops/
├── README.md
├── verify_revenue_sprint_kit.py
└── offers/
    └── revenue_sprint/
        ├── founder_dm_pack.md
        ├── sample_pack_template.md
        ├── proposal_fast_template.md
        ├── payment_followup_templates.md
        ├── client_intake.md
        ├── delivery_report_template.md
        ├── qa_checklist.md
        ├── handoff_template.md
        ├── feedback_request.md
        └── retainer_ask.md
```

## Verifier
Run:
```
python private_ops/verify_revenue_sprint_kit.py
```
Exits non-zero if any kit file is missing or trivially short.
