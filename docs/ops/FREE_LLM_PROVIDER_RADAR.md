# Free LLM Provider Radar — Dealix Daily Operating Layer

Dealix uses `cheahjs/free-llm-api-resources` as a living reference for legitimate free and trial LLM API providers. This is an operating radar, not an instruction to send sensitive Dealix or customer data to free tiers.

## Source adopted

- Reference repository: `cheahjs/free-llm-api-resources`
- Purpose: list services that provide free access or credits for API-based LLM usage.
- Important upstream posture: do not abuse free services, and exclude non-legitimate reverse-engineered chatbot services.
- Dealix posture: approval-first, PDPL-aware, no secrets in git, no sensitive data to free tiers by default.

## Why this matters for Dealix

This radar reduces daily AI operating cost while keeping founder velocity high. It should be used for non-sensitive work such as:

- repo coding assistance and refactor planning;
- test generation and failure explanation;
- draft-only outreach, proposal, and content variants;
- lead enrichment prompts that do not include private customer data;
- Arabic/Saudi wording experiments;
- speech/transcription experiments where the input is non-confidential.

It must not be used by default for:

- customer PII;
- legal/compliance final advice;
- confidential financials or contracts;
- credentials, secrets, webhook payloads, or private production logs;
- any outbound action that bypasses Dealix approval gates.

## Daily provider ladder

1. **Sensitive / customer / legal / production data**
   - Use approved paid/private provider or local model.
   - Keep audit trail and approval gate.

2. **Repo coding and agent work**
   - First choices: OpenRouter free models, Cerebras, Groq, GitHub Models, Cloudflare Workers AI.
   - Use for planning, code review, unit tests, documentation, and non-secret logs.

3. **Arabic and Saudi output drafting**
   - First choices: Groq Arabic models where available, Cohere Arabic-capable models, Gemini/Gemma, Cloudflare hosted Arabic-capable open models.
   - Human review required before client-facing Arabic.

4. **Batch daily Dealix work**
   - Use Groq/Cerebras/Cloudflare/OpenRouter for draft-only daily generation.
   - Split large work into small batches and respect provider rate limits.

5. **Temporary trial credits**
   - Treat as burst capacity only.
   - Do not build critical production dependency on expiring credits.

## Morning routine

Run:

```bash
make ai-provider-radar
```

Then decide:

- Which free provider handles coding today?
- Which provider handles Arabic/content drafts?
- Which provider is safe enough for non-sensitive lead research?
- Which tasks must stay on paid/private/local models?

## Environment keys

All keys are optional. Keep them in `.env` or the deployment secret manager only.

```bash
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=qwen/qwen3-coder:free

GROQ_API_KEY=
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=qwen/qwen3-32b

CEREBRAS_API_KEY=
CEREBRAS_BASE_URL=https://api.cerebras.ai/v1
CEREBRAS_MODEL=gpt-oss-120b

GOOGLE_API_KEY=
GEMINI_MODEL=gemma-3-27b-it

MISTRAL_API_KEY=
MISTRAL_BASE_URL=https://api.mistral.ai/v1
MISTRAL_MODEL=codestral-latest

COHERE_API_KEY=
COHERE_MODEL=command-r7b-arabic-02-2025

CLOUDFLARE_ACCOUNT_ID=
CLOUDFLARE_API_TOKEN=
CLOUDFLARE_AI_MODEL=@cf/qwen/qwen3-30b-a3b-fp8

GITHUB_MODELS_TOKEN=
GITHUB_MODELS_BASE_URL=https://models.github.ai/inference
GITHUB_MODELS_MODEL=openai/gpt-4.1-mini
```

## Safety rules

- Never commit API keys.
- Never paste `.env`, customer records, legal files, health records, or private logs into free providers.
- Use free providers for speed and experimentation, not as the final trust boundary.
- Keep all external send paths `draft_only` unless explicitly approved.
- If a provider changes policy, remove or downgrade it from `data/ai/free_llm_provider_registry.json`.

## Weekly maintenance

Every week:

1. Open `cheahjs/free-llm-api-resources`.
2. Check changed providers, limits, and trial credits.
3. Update `data/ai/free_llm_provider_registry.json`.
4. Run `make ai-provider-radar-json`.
5. Commit only non-secret provider metadata.

## Acceptance standard

This radar is considered operational when:

- `make ai-provider-radar` works without network access;
- provider entries clearly mark `free`, `trial`, `openai_compatible`, and `sensitive_data_allowed`;
- Dealix operators can pick a provider by task in under 60 seconds;
- sensitive work defaults away from free tiers;
- the daily operator can reference the radar before generating AI-assisted artifacts.
