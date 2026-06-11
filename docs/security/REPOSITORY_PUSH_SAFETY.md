# Repository Push Safety

## Before Every Push
1. Run `scripts/check_no_secrets.py`
2. Review diff for accidental credentials
3. Ensure no `.env` or `secrets.json` added
4. Confirm tests pass in demo mode

## Branch Protection
- Push to `feature/*` branches only
- PR required for `main`
- CI must pass before merge

## If Secrets Leaked
1. Rotate immediately
2. Revoke old keys
3. Force-push removal only if no forks exist
4. Document incident
