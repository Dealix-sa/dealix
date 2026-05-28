# Hermes Secret Rotation Playbook

**Scope:** API keys used by the Hermes orchestrator layer
(`dealix/hermes/`). Covers DeepSeek-direct, OpenRouter, OpenAI fallback.

---

## When to rotate

Rotate immediately when any of the following is true:

- A key was pasted into a chat, ticket, screenshot, screen share, video,
  or any non-secret channel.
- A key appeared in a git diff, CI log, error trace, or Sentry event.
- A laptop or session where the key was loaded was lost / disposed.
- A team member with key access has left the team.
- The provider dashboard shows unexpected usage spikes.
- It has been > 90 days since the last rotation (calendar rotation).

If you are in doubt, rotate. Rotation is cheap; a leaked key is not.

---

## Channels for handing over a rotated key

**Allowed:**
- Pasting directly into Railway / Vercel / Render project secrets UI.
- Pasting directly into `.env.local` on the founder's local machine
  (gitignored — see `.gitignore` lines 4–5, 270–272).
- 1Password / Bitwarden vault entry shared via the vault's native share.

**Forbidden:**
- Claude Code chat messages (transcripts are stored).
- Slack / WhatsApp / Telegram / Email.
- Git commits — even on private branches, even temporarily.
- Screenshots in any tracker.
- Test fixtures, seed data, `.env.example`.

---

## Step-by-step

### 1. DeepSeek (direct)

1. Open <https://platform.deepseek.com/api_keys>.
2. Revoke the old key labelled `dealix-hermes-direct`.
3. Create a new key with the same label and **API quota matching prod usage**.
4. Copy the value (starts with `sk-` followed by 32 hex chars) directly into:
   - Local dev: append to `.env.local` as `DEEPSEEK_API_KEY=sk-…`
   - Prod (Railway): `Project → Variables → DEEPSEEK_API_KEY`
   - CI (GitHub Actions): `Settings → Secrets → DEEPSEEK_API_KEY`
5. Trigger a no-op redeploy on Railway to load the new value.
6. Run `python scripts/hermes_smoke.py --provider direct_deepseek` and
   confirm `provider_resolved: direct_deepseek` and a non-empty completion.

### 2. OpenRouter

1. Open <https://openrouter.ai/keys>.
2. Revoke the old key labelled `dealix-hermes-openrouter`.
3. Create new key with **credit cap** (e.g. $50/mo) so a leak is bounded.
4. Format: `sk-or-v1-` followed by 40+ hex chars.
5. Store under `OPENROUTER_API_KEY` in the same three locations as step 1.4.
6. Run `python scripts/hermes_smoke.py --provider openrouter` and confirm
   the Three-Gear engine resolves gear 1 / 2 / 3 model IDs successfully.

### 3. OpenAI (only if used as fallback)

1. Open <https://platform.openai.com/api-keys>.
2. Revoke the old project key (`sk-proj-…`).
3. Create a new project key scoped to the `dealix-hermes` project.
4. Store under `OPENAI_API_KEY`.

---

## After rotation — required verifications

Run all four:

```bash
# 1. Doctrine guard — no live key in tracked files
pytest tests/test_no_provider_key_in_repo.py -v

# 2. detect-secrets baseline still clean
detect-secrets scan --baseline .secrets.baseline

# 3. Gitleaks pass on working tree
gitleaks detect --no-git -v --config .gitleaks.toml

# 4. Hermes smoke against the active provider
python scripts/hermes_smoke.py
```

If any step fails, **do not deploy** — investigate the leak path first.

---

## Audit trail

Each rotation appends a row to `docs/ledgers/SECRET_ROTATION_LEDGER.md`
with: date, key id (last 4 chars only), reason, performed-by, verification
checklist outcomes. Hermes governance_gate refuses to operate if the most
recent rotation entry is older than 90 days.
