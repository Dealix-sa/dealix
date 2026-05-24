"""Execution Intelligence — scoring helpers + RAG pipeline for the AI Stack.

This module exposes two layers:

* **Pure scoring helpers** (capability index, strategy decision, venture
  readiness, …). These are deterministic, side-effect-free, no LLM.
* **Retrieval-augmented generation primitives** (embedder, vector store,
  semantic search, RAG pipeline). These are used by the AI Stack (L3) to
  ground agent decisions in tenant-scoped memory.
"""

from auto_client_acquisition.intelligence_os.capability_index import (
    CapabilityScores,
    compute_dci,
)
from auto_client_acquisition.intelligence_os.capital_allocator import (
    PriorityBand,
    capital_priority_band,
    compute_capital_priority_score,
)
from auto_client_acquisition.intelligence_os.embedder import (
    DEFAULT_DIMENSION,
    Embedder,
    EmbeddingResult,
    chunk_text,
    cosine_similarity,
    deterministic_embed,
    embed_chunks,
)
from auto_client_acquisition.intelligence_os.rag_pipeline import (
    RAGPipeline,
    RetrievedContext,
)
from auto_client_acquisition.intelligence_os.semantic_search import (
    HybridHit,
    hits_as_search_hits,
    hybrid_search,
)
from auto_client_acquisition.intelligence_os.strategy_decision import (
    StrategyDecisionBand,
    StrategySignalInputs,
    compute_strategy_decision_score,
    strategy_decision_band,
)
from auto_client_acquisition.intelligence_os.transformation_gap import (
    SprintOpportunity,
    classify_sprint_opportunity,
    transformation_gap,
)
from auto_client_acquisition.intelligence_os.vector_store import (
    InMemoryVectorStore,
    SearchHit,
    VectorRecord,
    get_default_store,
    reset_default_store,
)
from auto_client_acquisition.intelligence_os.venture_signal import (
    VentureReadinessBand,
    classify_venture_readiness,
    compute_venture_readiness_score,
)

__all__ = [
    "CapabilityScores",
    "DEFAULT_DIMENSION",
    "Embedder",
    "EmbeddingResult",
    "HybridHit",
    "InMemoryVectorStore",
    "PriorityBand",
    "RAGPipeline",
    "RetrievedContext",
    "SearchHit",
    "SprintOpportunity",
    "StrategyDecisionBand",
    "StrategySignalInputs",
    "VectorRecord",
    "VentureReadinessBand",
    "capital_priority_band",
    "chunk_text",
    "classify_sprint_opportunity",
    "classify_venture_readiness",
    "compute_capital_priority_score",
    "compute_dci",
    "compute_strategy_decision_score",
    "compute_venture_readiness_score",
    "cosine_similarity",
    "deterministic_embed",
    "embed_chunks",
    "get_default_store",
    "hits_as_search_hits",
    "hybrid_search",
    "reset_default_store",
    "strategy_decision_band",
    "transformation_gap",
]
