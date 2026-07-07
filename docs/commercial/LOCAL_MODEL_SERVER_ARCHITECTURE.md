# Dealix Local Model Server Architecture

## Purpose

Dealix may use local or private model workers for low-cost classification, summarization, and draft support. The primary production service should remain the API/orchestration layer; model serving should be isolated.

## Recommended layout

```text
Dealix API / Railway service
  - public web/API surface
  - healthcheck /healthz
  - admin endpoints protected by keys
  - approval center

Private AI worker
  - Ollama for simple local tasks
  - vLLM later for GPU serving
  - private network only
  - queue-based jobs
  - rate limits and logs

Fallback providers
  - OpenRouter/Groq/etc. only for tasks that need external model quality
  - never send secrets or sensitive data to an untrusted route
```

## Security rules

- Do not expose local model ports publicly.
- Put the worker behind VPN/Tailscale/private networking or an authenticated gateway.
- Keep API keys in environment variables or secret stores only.
- Do not put secrets in prompts, logs, reports, or git.
- Use a task queue rather than direct user-triggered model calls for heavy jobs.
- Keep external model routes optional and policy-controlled.

## Routing policy

- Classification, scoring, and short summaries: local small model.
- Draft support: local or low-cost fallback, always reviewed.
- Code changes and high-stakes analysis: coding agent or stronger model with review.
- Public/client-facing text: proof-backed and founder-approved.

## First production posture

Do not run a large LLM inside the main `dealix` Railway service. Keep the main service small and reliable. Add a private worker only after the daily internal loop is stable.
