# Dealix AI Development Workflow

This guide turns Dealix development into a local, provider-agnostic workflow that does not depend on one IDE subscription limit.

## Goal

Use one local OpenAI-compatible gateway for:

- Aider CLI for large code changes.
- Continue.dev in VS Code for focused edits and code review.
- OpenAI, DeepSeek, and MiniMax API keys with automatic fallback.
- Small, auditable Git branches and pull requests.

## Architecture

```text
VS Code / Continue.dev
        │
Aider CLI
        │
        ▼
LiteLLM Proxy on localhost:4000
        │
        ├── dealix-code  → DeepSeek
        ├── dealix-smart → OpenAI
        └── dealix-fast  → MiniMax
```

## Files added by this workflow

| File | Purpose |
| --- | --- |
| `.ai/litellm_config.example.yaml` | Provider aliases and fallback routing. |
| `docker-compose.ai.yml` | Runs LiteLLM locally without touching production services. |
| `.ai/aider.env.example` | Shell profile notes for Aider through LiteLLM. |
| `scripts/verify_ai_gateway.py` | Dependency-free gateway smoke test. |
| `docs/AI_STRATEGIC_OPPORTUNITIES.md` | Strategic build roadmap for Dealix. |

## Setup

1. Copy the example gateway config:

```bash
mkdir -p .ai
cp .ai/litellm_config.example.yaml .ai/litellm_config.yaml
```

2. Add local-only secrets to `.env`:

```env
LITELLM_MASTER_KEY=replace_with_local_gateway_token

OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
DEALIX_OPENAI_MODEL=gpt-4.1-mini

DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

MINIMAX_API_KEY=
MINIMAX_BASE_URL=
DEALIX_MINIMAX_MODEL=
```

3. Start the local gateway:

```bash
docker compose -f docker-compose.ai.yml up -d
```

4. Verify:

```bash
python scripts/verify_ai_gateway.py \
  --base-url http://localhost:4000/v1 \
  --token "$LITELLM_MASTER_KEY"
```

## Aider usage

```bash
export OPENAI_API_BASE="http://localhost:4000/v1"
export OPENAI_API_KEY="$LITELLM_MASTER_KEY"
aider --model openai/dealix-code
```

Recommended first prompt:

```text
Inspect the repository structure only. Do not edit files. Summarize the architecture, risk areas, and a five-step implementation plan.
```

Then execute in small commits:

```text
Implement step 1 only. Before editing, list the files you will touch. After editing, summarize the diff and tests.
```

## Continue.dev usage

Create local Continue models that point to `http://localhost:4000/v1` and use the same local gateway token. Do not commit personal Continue config files or real provider keys.

Use:

- `Dealix Code` for implementation.
- `Dealix Smart` for architecture, code review, and debugging.
- `Dealix Fast` for boilerplate, quick explanations, and autocomplete.

## Daily safe workflow

```bash
git checkout main
git pull
git checkout -b feat/small-focused-change

docker compose -f docker-compose.ai.yml up -d
python scripts/verify_ai_gateway.py --skip-chat

aider --model openai/dealix-code

make env-check
make security-smoke
pytest -q --no-cov

git diff
git add .
git commit -m "feat: implement focused Dealix improvement"
git push -u origin HEAD
```

## Guardrails

- Do not ask an agent to “build everything”.
- Keep one branch per business outcome.
- Keep prompts bound to specific files.
- Run `make env-check` before editing environment variables.
- Never commit `.env` or provider keys.
- Prefer docs/config/tooling PRs separate from production behavior PRs.
