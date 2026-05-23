# Campaign Playbook

Each campaign at Dealix is a time-boxed, hypothesis-driven push tied to a specific ICP and a specific revenue outcome.

## Anatomy of a campaign

| Field | Description |
|-------|-------------|
| id | `cmp_YYYYMM_<slug>` |
| hypothesis | One sentence: "If we say X to Y, they will Z." |
| icp | Sector + role |
| channels | Email, LinkedIn, content, webinar — explicit list |
| offer | Pointer into `product/offer_ladder.csv` |
| proof | Pointer into `proof/proof_library.csv` |
| budget | Time + cash |
| success_metric | Quantified, single primary metric |
| start / end | ISO dates |

Campaigns are tracked in `marketing/campaigns.csv`.

## Approval

Any campaign that touches a public surface (LinkedIn ads, webinar invite) requires founder approval.
