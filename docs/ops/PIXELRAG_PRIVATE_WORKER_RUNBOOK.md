# PixelRAG Private Worker Runbook

## Purpose

Run PixelRAG outside the main Dealix Railway service as a private visual evidence worker. This keeps the production API light while still giving Dealix screenshot-based document retrieval.

## Why separate worker

Dealix main app targets Python 3.11+. PixelRAG targets Python 3.12 and may use heavier index and model packages. Keep the main Dealix service light and call the worker only through the `dealix.visual_rag` adapter.

## Approved modes

| Mode | Use |
|---|---|
| disabled | default CI and production safety |
| screenshot_only | render visual tiles for review |
| hosted_search | public source search only |
| private_worker | private internal document search |

## Minimal worker shape

```txt
Private worker
  Python 3.12
  pixelrag[serve,index]
  private network
  access control
  short retention for generated tiles
```

## Dealix environment variables

```bash
DEALIX_PIXELRAG_PRIVATE_WORKER_URL=http://pixelrag-worker.internal:30001
DEALIX_PIXELRAG_HOSTED_SEARCH_URL=https://api.pixelrag.ai
DEALIX_PIXELSHOT_BIN=pixelshot
DEALIX_VISUAL_RAG_OUTPUT_ROOT=reports/visual_rag
DEALIX_VISUAL_RAG_TIMEOUT_SECONDS=30
```

## Local worker prototype

```bash
python3.12 -m venv .venv-pixelrag
. .venv-pixelrag/bin/activate
pip install 'pixelrag[serve,index]'

cat > pixelrag.yaml << 'EOF'
source:
  type: local
  path: ./docs_to_index
embed:
  model: Qwen/Qwen3-VL-Embedding-2B
  device: auto
output: ./visual_index
EOF

pixelrag index build
pixelrag serve --index-dir ./visual_index --port 30001
```

## Dealix verification

```bash
python scripts/commercial/verify_pixelrag_visual_rag.py
python scripts/commercial/run_pixelrag_visual_rag_demo.py --mode disabled
```

For private worker testing:

```bash
DEALIX_PIXELRAG_PRIVATE_WORKER_URL=http://localhost:30001 \
python scripts/commercial/run_pixelrag_visual_rag_demo.py \
  --mode private_worker \
  --sensitivity internal \
  --source https://example.com \
  --query 'pricing table' \
  --approve
```

## Security rules

- Keep the worker on a private network.
- Do not expose PixelRAG or model-serving endpoints publicly without access control.
- Use hosted search only for public sources.
- Keep retention short for generated visual tiles.
- Review visual evidence before using it in client-facing deliverables.
- Keep screenshots out of git unless they are sanitized fixtures.

## Production milestone order

1. Merge VisualRAG adapter and policy gate.
2. Use screenshot-only for public proof-pack evidence.
3. Deploy private worker in staging.
4. Add proof-pack visual appendix review flow.
5. Add dashboard review UI.
6. Add indexing only after retention and access controls are verified.
