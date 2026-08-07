# RAG Architecture Plan

## V14 (today)
- Deterministic local index. No embeddings.
- Substring + keyword match on titles + first 500 chars.
- Good enough for ~1,000 source files.

## V15+ (future)
- Embedding-backed vector store (provider TBD).
- Per-tenant collections.
- Reranking with a small reranker.
- Hybrid retrieval (BM25 + dense).

## Quality gates before flipping to vector RAG
- Embedding provider contracted with data-residency clause.
- Per-tenant isolation tested.
- Eval set: at least 50 Q/A pairs with reference answers.
- Cost ceiling per query enforced.
- Caching to reduce embedding calls.

## Non-goals
- Open-internet retrieval inside Dealix. The knowledge base stays internal.
- Agentic web browsing.
