# Local Model / AI Worker Architecture

## Principles
- Do **not** run a large LLM inside the Railway production API.
- Keep the Dealix production API separate from any AI worker.
- Ollama is fine for local testing and simple private tasks.
- vLLM can serve GPU production later, on a **private** network only.
- A provider fallback (e.g. OpenRouter) may be used only if configured safely.
- **No** model endpoint is public without auth, firewall, rate limits, and
  private networking. **No** provider keys are committed or printed.

## Layout
- **Main app:** Railway / API / Website / Approval Center.
- **Execution:** GitHub Actions daily · strategy registry · action queue ·
  approval queue · proof log.
- **AI worker:** local machine or private VPS · Ollama or vLLM · private network ·
  API key · rate limit · no secrets in prompts.
