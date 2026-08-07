# Model Provider Matrix

| Provider | Env var | Strengths | Cautions |
| --- | --- | --- | --- |
| MiniMax | `MINIMAX_API_KEY` | Long context, good Arabic | Throttling |
| Kimi | `KIMI_API_KEY` | Strong reasoning | Cost |
| DeepSeek | `DEEPSEEK_API_KEY` | Code + reasoning | Newer ecosystem |
| OpenRouter | `OPENROUTER_API_KEY` | Multi-model fallback | Per-route reliability |
| OpenAI | `OPENAI_API_KEY` | General quality | Cost, regional latency |

Routing rules (when activated):
- AR-heavy outreach → MiniMax or Kimi.
- Proposal sections → OpenAI / Kimi.
- Translation AR↔EN → MiniMax.
- Compliance review preflight → DeepSeek.
- All tasks fall back to deterministic if no provider configured.
