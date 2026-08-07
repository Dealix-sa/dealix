# data/distribution/ — examples only

These `*.example.*` files illustrate the `distribution_os` record shapes
(validated against [`../../schemas/`](../../schemas/)). They are **examples**,
not live data.

Live operational data is written by `distribution_os` to `var/*.jsonl`
(git-ignored), or to the path in the matching `DEALIX_*_PATH` env var:

| Store | Env var | Default |
|-------|---------|---------|
| prospects | `DEALIX_PROSPECTS_PATH` | `var/prospects.jsonl` |
| drafts | `DEALIX_DRAFTS_PATH` | `var/drafts.jsonl` |
| follow-ups | `DEALIX_FOLLOWUPS_PATH` | `var/followups.jsonl` |
| proposals | `DEALIX_PROPOSALS_PATH` | `var/proposals.jsonl` |
| proof packs | `DEALIX_PROOF_PACKS_PATH` | `var/proof_packs.jsonl` |
| payment handoffs | `DEALIX_PAYMENT_HANDOFFS_PATH` | `var/payment_handoffs.jsonl` |
| delivery handoffs | `DEALIX_DELIVERY_HANDOFFS_PATH` | `var/delivery_handoffs.jsonl` |
| win/loss | `DEALIX_WIN_LOSS_PATH` | `var/win_loss.jsonl` |

No customer PII belongs in committed example files.
