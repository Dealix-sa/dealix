# Gmail Drafts Runbook

## Safety first

- **AI drafts only.** No automatic external send.
- **Human review required** before any draft becomes an email.
- **Opt-out line** included in every generated message.
- **Env vars only** for secrets; no credentials in code.

## Required environment variables

```bash
export GMAIL_CLIENT_ID="..."
export GMAIL_CLIENT_SECRET="..."
export GMAIL_REFRESH_TOKEN="..."
export GMAIL_SENDER_EMAIL="sami@dealix.me"
export GMAIL_LIST_UNSUBSCRIBE="unsubscribe@dealix.me"
```

Scope needed: `https://www.googleapis.com/auth/gmail.compose`

## Commands

```bash
# Preview drafts without creating anything (default)
make gmail-drafts-dry-run

# Actually create Gmail drafts after review
make gmail-drafts
```

## Manual steps

1. Run `make revenue-daily` to generate outbox drafts.
2. Open each draft in `outbox/YYYY-MM-DD/` and review.
3. Run `make gmail-drafts-dry-run` to confirm recipient list.
4. Set `GMAIL_*` env vars.
5. Run `make gmail-drafts` (creates drafts, does not send).
6. In Gmail, review drafts and send manually.

## What is blocked by design

- No `send()` call from this script.
- `--force` is required to leave dry-run mode.
- Missing env vars returns a clear error, not a silent skip.
