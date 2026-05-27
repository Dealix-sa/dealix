# Hermes Server Runbook

This runbook explains how to operate Hermes safely as a review-first founder operating layer.

## Prerequisites

- Repository available on the server.
- Python 3.11 or newer.
- Local `.env` kept outside Git.
- Optional local AI gateway configured from `.ai/litellm_config.example.yaml`.

## Safe check sequence

```bash
git status
python scripts/verify_hermes_layer.py
python scripts/hermes_review_runner.py --out-dir data/hermes
```

Expected outputs:

```text
HERMES_LAYER_OK
HERMES_REVIEW_RUNNER_OK
```

Expected local artifacts:

```text
data/hermes/review_records.jsonl
data/hermes/founder_digest.md
```

The repository already ignores `data/*`, so generated founder artifacts should remain local.

## Suggested local rhythm

Start with artifact generation only:

```text
08:00 daily: run hermes_review_runner.py and review founder_digest.md
Every 6 hours: run verify_hermes_layer.py and review any errors
On PR changes: review Hermes workflow results
Weekly: review HERMES_EXECUTION_BACKLOG.md and choose next small PR
```

## Operating procedure

1. Run `python scripts/verify_hermes_layer.py` after every Hermes change.
2. Run the review runner to generate artifacts.
3. Read `data/hermes/founder_digest.md`.
4. Convert useful recommendations into GitHub issues, PRs, or manual founder actions.
5. Keep generated customer and founder state outside Git.

## Rollback

Hermes foundation changes are isolated to docs, scripts, and `hermes/` files.

1. Pause any local scheduler that calls the runner.
2. Stop running the review runner.
3. Remove local generated artifacts under `data/hermes/` if they are no longer needed.
4. Revert the PR or specific Hermes commits if necessary.

## Expansion path

Add capabilities in this order:

1. Read-only local artifacts.
2. Read-only GitHub and CI summaries.
3. Read-only provider usage summaries.
4. Founder review records.
5. Approval registry.
6. Narrow approved workflows after review records are reliable.

## Safety notes

- Do not store real provider keys in the repo.
- Do not commit generated artifacts from `data/hermes/`.
- Do not connect writable integrations until the approval registry exists.
- Do not mix framework experiments with production changes in the same PR.
