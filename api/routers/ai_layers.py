"""
AI Layers — unified HTTP surface for the Dealix intelligence stack.
طبقات الذكاء الاصطناعي — واجهة HTTP موحّدة لكل طبقات الذكاء في Dealix.

Wraps the ``dealix.intelligence.layers`` package. All endpoints are
read-only / compute-only — no external sends, no charges, no live actions.
Hard rules surfaced via the ``hard_gates`` field per Dealix doctrine.

Endpoints (all under /api/v1/ai-layers):
    GET  /                        layer index + hard gates
    GET  /status                  per-layer availability + backend
    POST /embed                   single + batch embeddings
    POST /vector/upsert           upsert text into in-memory store
    POST /vector/search           cosine search
    POST /chunker                 hierarchical text chunker
    POST /ner                     named entity recognition (AR+EN)
    POST /keyphrase               RAKE-style keyphrase extraction
    POST /relation                S-P-O relation triples
    POST /pii                     PDPL PII detect + redact
    POST /summarize               extractive TextRank summary
    POST /translate               AR↔EN glossary translation
    POST /zeroshot                zero-shot classification
    POST /cluster                 KMeans-lite over caller-supplied texts
    POST /forecast                EWMA / Holt / linreg
    POST /anomaly                 z-score / IQR / EWMA anomaly detection
    POST /safety                  prompt-injection + jailbreak + doctrine
    POST /moderate                toxicity + content categories
    POST /rag/ingest              ingest doc into RAG index
    POST /rag/ask                 retrieve + build a citation-rich prompt
    POST /recommend/by-text       content-based recommendations
    POST /kg/add                  add a triple
    POST /kg/query                S/P/O / SP / PO query
    POST /memory/add              add a conversation turn
    GET  /memory/snapshot         current memory + running summary
    POST /memory/reset            reset memory
    POST /feedback                record a thumbs-up/down feedback row
    GET  /feedback/{layer}        feedback summary for a layer
"""
from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from dealix.intelligence.layers import (
    AnomalyDetector,
    ContentRecommender,
    ConversationMemory,
    EmbeddingModel,
    ExtractiveSummarizer,
    FeedbackStore,
    Forecaster,
    KMeansLite,
    KeyphraseExtractor,
    KnowledgeGraph,
    Moderator,
    NERTagger,
    PIIRedactor,
    RAGEngine,
    RelationExtractor,
    SafetyClassifier,
    SmartChunker,
    Translator,
    VectorStore,
    ZeroShotClassifier,
    embed,
    embed_batch,
)

router = APIRouter(prefix="/api/v1/ai-layers", tags=["AI Layers"])


# ── Shared singletons (in-memory, per-process) ─────────────────────
_EMBED = EmbeddingModel()
_STORE = VectorStore(embedder=_EMBED)
_NER = NERTagger()
_KEYPHRASE = KeyphraseExtractor()
_RELATION = RelationExtractor(ner=_NER)
_PII = PIIRedactor()
_SUMMARIZER = ExtractiveSummarizer()
_TRANSLATOR = Translator()
_CHUNKER = SmartChunker()
_FORECASTER = Forecaster()
_SAFETY = SafetyClassifier()
_MODERATOR = Moderator()
_RAG = RAGEngine(store=_STORE, chunker=_CHUNKER, embedder=_EMBED)
_RECOMMENDER = ContentRecommender(_STORE)
_KG = KnowledgeGraph()
_MEMORY = ConversationMemory(max_turns=24, max_chars=8000)
_FEEDBACK = FeedbackStore()

_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_secrets_in_response": True,
    "in_memory_indices_only": True,
    "graceful_degradation_on_failure": True,
    "approval_required_for_external_actions": True,
}

_LAYER_INDEX = {
    "foundations": ["embeddings", "vector_store", "chunker"],
    "extraction": ["ner", "keyphrase", "relation", "pii"],
    "transformation": ["summarizer", "translator", "zeroshot"],
    "retrieval": ["rag", "recommender"],
    "analytics": ["clustering", "forecasting", "anomaly"],
    "safety": ["safety", "moderation"],
    "gateway": ["llm_gateway", "prompt_cache", "memory"],
    "knowledge": ["knowledge_graph"],
    "learning": ["feedback"],
    "orchestration": ["pipeline"],
}


# ─────────────────────────────────────────────────────────────────────
# Root + status
# ─────────────────────────────────────────────────────────────────────
@router.get("/")
async def root() -> dict[str, Any]:
    return {
        "service": "ai_layers",
        "version": 1,
        "layers": _LAYER_INDEX,
        "hard_gates": _HARD_GATES,
        "backend": _EMBED.backend,
        "embedding_dim": _EMBED.dim,
    }


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "embeddings": {"backend": _EMBED.backend, "dim": _EMBED.dim},
        "vector_store": _STORE.stats(),
        "rag": _RAG.stats(),
        "knowledge_graph": _KG.stats(),
        "memory": {
            "turns": _MEMORY.snapshot().total_turns,
            "chars": _MEMORY.snapshot().total_chars,
            "pruned": _MEMORY.snapshot().pruned_turns,
        },
        "hard_gates": _HARD_GATES,
    }


# ─────────────────────────────────────────────────────────────────────
# Embeddings
# ─────────────────────────────────────────────────────────────────────
class EmbedRequest(BaseModel):
    text: str | None = None
    texts: list[str] | None = None


@router.post("/embed")
async def embed_endpoint(req: EmbedRequest) -> dict[str, Any]:
    if not req.text and not req.texts:
        raise HTTPException(400, "provide 'text' or 'texts'")
    if req.texts:
        vecs = embed_batch(req.texts)
        return {"count": len(vecs), "dim": len(vecs[0]) if vecs else 0, "vectors": vecs}
    vec = embed(req.text or "")
    return {"count": 1, "dim": len(vec), "vector": vec}


# ─────────────────────────────────────────────────────────────────────
# Vector store
# ─────────────────────────────────────────────────────────────────────
class UpsertRequest(BaseModel):
    id: str
    text: str
    metadata: dict[str, Any] | None = None


@router.post("/vector/upsert")
async def vector_upsert(req: UpsertRequest) -> dict[str, Any]:
    record = _STORE.upsert(req.id, req.text, req.metadata or {})
    return {
        "id": record.id,
        "dim": len(record.vector),
        "store_size": _STORE.size,
    }


class VectorSearchRequest(BaseModel):
    query: str
    top_k: int = Field(5, ge=1, le=50)
    min_score: float = Field(0.0, ge=0.0, le=1.0)
    metadata_filter: dict[str, Any] | None = None


@router.post("/vector/search")
async def vector_search(req: VectorSearchRequest) -> dict[str, Any]:
    hits = _STORE.search(
        req.query,
        top_k=req.top_k,
        min_score=req.min_score,
        metadata_filter=req.metadata_filter,
    )
    return {
        "query": req.query,
        "count": len(hits),
        "results": [
            {"id": r.id, "score": round(s, 4), "text": r.text, "metadata": r.metadata}
            for r, s in hits
        ],
    }


# ─────────────────────────────────────────────────────────────────────
# Chunker
# ─────────────────────────────────────────────────────────────────────
class ChunkerRequest(BaseModel):
    text: str
    max_chars: int = Field(1200, ge=64, le=8000)
    overlap_chars: int = Field(120, ge=0, le=1000)


@router.post("/chunker")
async def chunker_endpoint(req: ChunkerRequest) -> dict[str, Any]:
    chunker = SmartChunker(max_chars=req.max_chars, overlap_chars=req.overlap_chars)
    chunks = chunker.chunk(req.text)
    return {
        "count": len(chunks),
        "chunks": [
            {"index": c.index, "start_char": c.start_char, "end_char": c.end_char, "text": c.text}
            for c in chunks
        ],
    }


# ─────────────────────────────────────────────────────────────────────
# NER / Keyphrase / Relation / PII
# ─────────────────────────────────────────────────────────────────────
class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


@router.post("/ner")
async def ner_endpoint(req: TextRequest) -> dict[str, Any]:
    ents = _NER.tag(req.text)
    grouped = _NER.tag_grouped(req.text)
    return {
        "count": len(ents),
        "entities": [
            {"text": e.text, "label": e.label, "start": e.start, "end": e.end, "score": e.score}
            for e in ents
        ],
        "grouped": grouped,
    }


@router.post("/keyphrase")
async def keyphrase_endpoint(req: TextRequest) -> dict[str, Any]:
    phrases = _KEYPHRASE.extract(req.text, top_k=15)
    return {
        "count": len(phrases),
        "phrases": [
            {"phrase": p.phrase, "score": p.score, "words": p.word_count, "freq": p.frequency}
            for p in phrases
        ],
    }


@router.post("/relation")
async def relation_endpoint(req: TextRequest) -> dict[str, Any]:
    triples = _RELATION.extract(req.text)
    return {
        "count": len(triples),
        "triples": [
            {
                "subject": t.subject,
                "predicate": t.predicate,
                "object": t.object,
                "confidence": t.confidence,
                "subject_label": t.subject_label,
                "object_label": t.object_label,
                "sentence": t.sentence,
            }
            for t in triples
        ],
    }


class PIIRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    mode: Literal["mask", "hash", "partial"] = "mask"


@router.post("/pii")
async def pii_endpoint(req: PIIRequest) -> dict[str, Any]:
    redacted, matches = _PII.redact(req.text, mode=req.mode)
    return {
        "redacted": redacted,
        "match_count": len(matches),
        "matches": [
            {"category": m.category, "value": "[hidden]", "start": m.start, "end": m.end, "severity": m.severity}
            for m in matches
        ],
        "mode": req.mode,
    }


# ─────────────────────────────────────────────────────────────────────
# Summarizer / Translator / Zero-shot
# ─────────────────────────────────────────────────────────────────────
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=40000)
    top_k: int = Field(3, ge=1, le=15)


@router.post("/summarize")
async def summarize_endpoint(req: SummarizeRequest) -> dict[str, Any]:
    res = _SUMMARIZER.summarize(req.text, top_k=req.top_k)
    return {
        "summary": res.summary,
        "coverage_ratio": res.coverage_ratio,
        "selected_sentences": [
            {"sentence": s.sentence, "score": round(s.score, 4), "original_index": s.original_index}
            for s in res.sentences
        ],
        "backend": res.backend,
    }


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)
    direction: Literal["auto", "ar->en", "en->ar"] = "auto"


@router.post("/translate")
async def translate_endpoint(req: TranslateRequest) -> dict[str, Any]:
    res = _TRANSLATOR.translate(req.text, direction=req.direction)
    return {
        "translation": res.text,
        "source": res.source,
        "target": res.target,
        "backend": res.backend,
        "confidence": res.confidence,
    }


class ZeroShotRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)
    labels: list[str] = Field(..., min_length=1, max_length=50)
    multi_label: bool = False
    threshold: float = Field(0.35, ge=0.0, le=1.0)


@router.post("/zeroshot")
async def zeroshot_endpoint(req: ZeroShotRequest) -> dict[str, Any]:
    clf = ZeroShotClassifier(req.labels, embedder=_EMBED)
    res = clf.classify(req.text, multi_label=req.multi_label, threshold=req.threshold)
    return {
        "label": res.label,
        "score": res.score,
        "multi_label": res.multi_label,
        "ranking": [{"label": lbl, "score": s} for lbl, s in res.ranking],
        "backend": res.backend,
    }


# ─────────────────────────────────────────────────────────────────────
# Clustering / Forecasting / Anomaly
# ─────────────────────────────────────────────────────────────────────
class ClusterRequest(BaseModel):
    texts: list[str] = Field(..., min_length=2, max_length=2000)
    ids: list[str] | None = None
    k: int = Field(3, ge=2, le=64)
    metric: Literal["euclidean", "cosine"] = "cosine"


@router.post("/cluster")
async def cluster_endpoint(req: ClusterRequest) -> dict[str, Any]:
    if req.ids and len(req.ids) != len(req.texts):
        raise HTTPException(400, "ids length must match texts length")
    vectors = embed_batch(req.texts)
    km = KMeansLite(k=req.k, metric=req.metric)
    result = km.fit(vectors, ids=req.ids)
    return {
        "iterations": result.iterations,
        "total_inertia": result.total_inertia,
        "silhouette": result.silhouette,
        "clusters": [
            {
                "id": c.id,
                "size": len(c.member_indices),
                "members": c.member_ids,
                "inertia": c.inertia,
            }
            for c in result.clusters
        ],
    }


class ForecastRequest(BaseModel):
    series: list[float] = Field(..., min_length=2, max_length=2000)
    horizon: int = Field(4, ge=1, le=64)
    method: Literal["ewma", "holt", "linreg"] = "holt"
    alpha: float = Field(0.4, gt=0.0, lt=1.0)
    beta: float = Field(0.2, ge=0.0, lt=1.0)


@router.post("/forecast")
async def forecast_endpoint(req: ForecastRequest) -> dict[str, Any]:
    f = Forecaster(alpha=req.alpha, beta=req.beta)
    res = f.forecast(req.series, horizon=req.horizon, method=req.method)
    return {
        "method": res.method,
        "next_value": round(res.next_value, 4),
        "horizon": [round(x, 4) for x in res.horizon],
        "lower_ci": [round(x, 4) for x in res.lower_ci],
        "upper_ci": [round(x, 4) for x in res.upper_ci],
        "trend_slope": res.trend_slope,
        "residual_std": res.residual_std,
    }


class AnomalyRequest(BaseModel):
    series: list[float] = Field(..., min_length=2, max_length=5000)
    method: Literal["zscore", "iqr", "ewma"] = "zscore"
    threshold: float | None = None


@router.post("/anomaly")
async def anomaly_endpoint(req: AnomalyRequest) -> dict[str, Any]:
    det = AnomalyDetector(method=req.method, threshold=req.threshold)
    res = det.detect(req.series)
    return {
        "method": res.method,
        "threshold": res.threshold,
        "series_mean": res.series_mean,
        "series_std": res.series_std,
        "anomaly_count": len(res.anomalies),
        "anomalies": [
            {"index": a.index, "value": a.value, "score": a.score, "severity": a.severity, "reason": a.reason}
            for a in res.anomalies
        ],
    }


# ─────────────────────────────────────────────────────────────────────
# Safety / Moderation
# ─────────────────────────────────────────────────────────────────────
@router.post("/safety")
async def safety_endpoint(req: TextRequest) -> dict[str, Any]:
    res = _SAFETY.evaluate(req.text)
    return {
        "score": res.score,
        "severity": res.severity,
        "recommended_action": res.recommended_action,
        "findings": [
            {"category": f.category, "cue": f.cue, "severity": f.severity}
            for f in res.findings
        ],
        "redacted_input_preview": (res.redacted_input[:240] + "…") if len(res.redacted_input) > 240 else res.redacted_input,
    }


@router.post("/moderate")
async def moderate_endpoint(req: TextRequest) -> dict[str, Any]:
    res = _MODERATOR.evaluate(req.text)
    return {
        "flagged": res.flagged,
        "highest_category": res.highest_category,
        "highest_score": res.highest_score,
        "categories": res.categories,
        "matched_terms": list(res.matched_terms),
    }


# ─────────────────────────────────────────────────────────────────────
# RAG
# ─────────────────────────────────────────────────────────────────────
class RAGIngestRequest(BaseModel):
    document_id: str
    text: str = Field(..., min_length=1)
    metadata: dict[str, Any] | None = None


@router.post("/rag/ingest")
async def rag_ingest(req: RAGIngestRequest) -> dict[str, Any]:
    report = _RAG.ingest(req.document_id, req.text, metadata=req.metadata)
    return {
        "document_id": report.document_id,
        "chunks_indexed": report.chunks_indexed,
        "total_chars": report.total_chars,
        "skipped": report.skipped,
        "reason": report.reason,
        "store_size": _STORE.size,
    }


class RAGAskRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(4, ge=1, le=20)
    min_score: float = Field(0.05, ge=0.0, le=1.0)
    metadata_filter: dict[str, Any] | None = None


@router.post("/rag/ask")
async def rag_ask(req: RAGAskRequest) -> dict[str, Any]:
    res = _RAG.ask(
        req.query,
        top_k=req.top_k,
        min_score=req.min_score,
        metadata_filter=req.metadata_filter,
    )
    return {
        "query": res.query,
        "documents_searched": res.documents_searched,
        "citations": [
            {
                "document_id": c.document_id,
                "chunk_id": c.chunk_id,
                "chunk_index": c.chunk_index,
                "score": c.score,
                "snippet": c.snippet,
                "metadata": c.metadata,
            }
            for c in res.citations
        ],
        "context": res.context,
        "prompt": res.prompt,
        "backend": res.backend,
    }


# ─────────────────────────────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────────────────────────────
class RecommendRequest(BaseModel):
    text: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=50)
    diversify: bool = True
    metadata_filter: dict[str, Any] | None = None


@router.post("/recommend/by-text")
async def recommend_by_text(req: RecommendRequest) -> dict[str, Any]:
    items = _RECOMMENDER.by_text(
        req.text,
        top_k=req.top_k,
        diversify=req.diversify,
        metadata_filter=req.metadata_filter,
    )
    return {
        "count": len(items),
        "items": [
            {"id": r.id, "score": r.score, "text": r.text, "metadata": r.metadata}
            for r in items
        ],
    }


# ─────────────────────────────────────────────────────────────────────
# Knowledge Graph
# ─────────────────────────────────────────────────────────────────────
class KGTripleRequest(BaseModel):
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    source: str = ""


@router.post("/kg/add")
async def kg_add(req: KGTripleRequest) -> dict[str, Any]:
    t = _KG.add(
        req.subject, req.predicate, req.object,
        confidence=req.confidence, source=req.source,
    )
    return {"added": True, "stats": _KG.stats(), "triple": {"s": t.subject, "p": t.predicate, "o": t.object}}


class KGQueryRequest(BaseModel):
    subject: str | None = None
    predicate: str | None = None
    object: str | None = None


@router.post("/kg/query")
async def kg_query(req: KGQueryRequest) -> dict[str, Any]:
    triples = _KG.query(req.subject, req.predicate, req.object)
    return {
        "count": len(triples),
        "triples": [
            {"subject": t.subject, "predicate": t.predicate, "object": t.object, "confidence": t.confidence}
            for t in triples
        ],
    }


# ─────────────────────────────────────────────────────────────────────
# Conversation memory
# ─────────────────────────────────────────────────────────────────────
class MemoryAddRequest(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str = Field(..., min_length=1)
    metadata: dict[str, Any] | None = None


@router.post("/memory/add")
async def memory_add(req: MemoryAddRequest) -> dict[str, Any]:
    t = _MEMORY.add(req.role, req.content, metadata=req.metadata or {})
    snap = _MEMORY.snapshot()
    return {
        "added": True,
        "turn": {"role": t.role, "chars": len(t.content)},
        "snapshot": {"total_turns": snap.total_turns, "pruned": snap.pruned_turns},
    }


@router.get("/memory/snapshot")
async def memory_snapshot() -> dict[str, Any]:
    snap = _MEMORY.snapshot()
    return {
        "running_summary": snap.running_summary,
        "total_turns": snap.total_turns,
        "total_chars": snap.total_chars,
        "pruned_turns": snap.pruned_turns,
        "recent_turns": [
            {"role": t.role, "content": t.content[:240], "ts": t.timestamp}
            for t in snap.recent_turns[-10:]
        ],
    }


@router.post("/memory/reset")
async def memory_reset() -> dict[str, Any]:
    _MEMORY.reset()
    return {"reset": True}


# ─────────────────────────────────────────────────────────────────────
# Feedback / Active learning
# ─────────────────────────────────────────────────────────────────────
class FeedbackRequest(BaseModel):
    item_id: str
    layer: str
    prediction: Any
    verdict: Literal["positive", "negative", "neutral"]
    reason: str = ""
    actor: str = "anonymous"
    score: float | None = None
    metadata: dict[str, Any] | None = None


@router.post("/feedback")
async def feedback_endpoint(req: FeedbackRequest) -> dict[str, Any]:
    fb = _FEEDBACK.add(
        req.item_id, req.layer, req.prediction, req.verdict,
        reason=req.reason, actor=req.actor, score=req.score, metadata=req.metadata or {},
    )
    return {"recorded": True, "summary": _summary_to_dict(_FEEDBACK.summary(fb.layer))}


@router.get("/feedback/{layer}")
async def feedback_summary(layer: str) -> dict[str, Any]:
    return _summary_to_dict(_FEEDBACK.summary(layer))


def _summary_to_dict(s) -> dict[str, Any]:
    return {
        "layer": s.layer,
        "total": s.total,
        "positives": s.positives,
        "negatives": s.negatives,
        "neutrals": s.neutrals,
        "accuracy": s.accuracy,
        "avg_score": s.avg_score,
        "recent_negatives": [
            {"item_id": f.item_id, "reason": f.reason, "actor": f.actor}
            for f in s.recent_negatives
        ],
    }
