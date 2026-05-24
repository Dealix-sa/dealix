# Dealix Intelligence Layers — Comprehensive AI Stack

> 22 طبقة ذكاء اصطناعي بدون اعتمادات خارجية — كل طبقة قابلة للترقية تلقائيًا عند تثبيت مكتبات اختيارية.

## Layer Index

| Tier | Module | What it does |
|------|--------|--------------|
| Foundations | `embeddings.py` | Sentence/text embeddings (sentence-transformers when available, hashed-trigram fallback) |
| Foundations | `vector_store.py` | In-memory cosine-similarity store with optional JSON persistence |
| Foundations | `chunker.py` | Paragraph + sentence-aware bilingual chunker |
| Extraction | `ner.py` | Bilingual NER (PERSON / ORG / LOCATION / MONEY / PHONE / EMAIL / URL / DATE / PERCENT / SECTOR / CR / VAT) |
| Extraction | `keyphrase.py` | RAKE-style keyphrase extraction (AR + EN) |
| Extraction | `relation.py` | Subject-predicate-object triple extractor |
| Extraction | `pii.py` | PDPL-aligned PII detect + redact (mask / hash / partial) |
| Transformation | `summarizer.py` | TextRank-lite extractive summarization |
| Transformation | `translator.py` | AR↔EN glossary translator with optional LLM upgrade |
| Transformation | `zeroshot.py` | Zero-shot classification via label-embedding cosine |
| Retrieval | `rag.py` | End-to-end RAG (chunk → embed → retrieve → pack with citations) |
| Retrieval | `recommender.py` | Content-based recommender with optional MMR diversification |
| Analytics | `clustering.py` | KMeans-lite (k-means++ seed, silhouette score) |
| Analytics | `forecasting.py` | EWMA / Holt linear / linear regression with 95 % CI |
| Analytics | `anomaly.py` | z-score / IQR / EWMA anomaly detection |
| Safety | `safety.py` | Prompt-injection / jailbreak / doctrine-breach / secret-exfil heuristics |
| Safety | `moderation.py` | Toxicity + content-category lexicon classifier |
| Gateway | `llm_gateway.py` | Provider-agnostic gateway with cache, retries, fallback |
| Gateway | `prompt_cache.py` | LRU + TTL cache, optional disk persistence |
| Gateway | `memory.py` | Rolling conversation memory with auto-summary |
| Knowledge | `knowledge_graph.py` | In-memory triple store with SPO indices + BFS traversal |
| Learning | `feedback.py` | Active-learning feedback store with summary + relabel queue |
| Orchestration | `pipeline.py` | Async-capable pipeline of named steps |

## HTTP surface

All layers are exposed under **`/api/v1/ai-layers/*`** (see `api/routers/ai_layers.py`).
Root endpoint returns layer index + hard gates:

```
GET /api/v1/ai-layers/
GET /api/v1/ai-layers/status
POST /api/v1/ai-layers/embed
POST /api/v1/ai-layers/vector/{upsert,search}
POST /api/v1/ai-layers/chunker
POST /api/v1/ai-layers/{ner,keyphrase,relation,pii}
POST /api/v1/ai-layers/{summarize,translate,zeroshot}
POST /api/v1/ai-layers/{cluster,forecast,anomaly}
POST /api/v1/ai-layers/{safety,moderate}
POST /api/v1/ai-layers/rag/{ingest,ask}
POST /api/v1/ai-layers/recommend/by-text
POST /api/v1/ai-layers/kg/{add,query}
POST /api/v1/ai-layers/memory/{add,reset}
GET  /api/v1/ai-layers/memory/snapshot
POST /api/v1/ai-layers/feedback
GET  /api/v1/ai-layers/feedback/{layer}
```

## Hard gates (Dealix doctrine, surfaced in every response)

- `no_live_send` — never sends real outbound messages
- `no_live_charge` — never charges customers
- `no_secrets_in_response` — never leaks API keys / prompts
- `in_memory_indices_only` — vector store / KG / memory are process-local; persist explicitly
- `graceful_degradation_on_failure` — layers degrade rather than raise
- `approval_required_for_external_actions` — layers are compute-only

## Quick start (Python)

```python
from dealix.intelligence import (
    RAGEngine, NERTagger, PIIRedactor, ZeroShotClassifier,
    SafetyClassifier, Forecaster, AnomalyDetector, KnowledgeGraph,
)

rag = RAGEngine()
rag.ingest("doc-1", "Dealix offers a 7-day free diagnostic. Pricing starts at 499 SAR.")
print(rag.ask("How long is the diagnostic?").citations)

# PDPL redaction before logging customer text
safe, _ = PIIRedactor().redact("Reach me at u@x.co or +966501234567")

# Safety gate before any LLM call
verdict = SafetyClassifier().evaluate(user_input)
if verdict.recommended_action == "block":
    return "blocked"

# Forecast next 4 weeks of revenue
Forecaster().forecast([100, 120, 140, 165, 190], horizon=4, method="holt")

# Detect anomalies in a daily latency series
AnomalyDetector(method="zscore").detect([0.4, 0.41, 0.39, 0.42, 5.2])
```

## Tests

```bash
APP_ENV=test pytest tests/intelligence/ -q --no-cov
```

85 tests cover every layer + every HTTP endpoint.
