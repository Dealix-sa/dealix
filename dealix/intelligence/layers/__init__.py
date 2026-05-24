"""
Dealix Intelligence Layers — comprehensive AI stack.
طبقات الذكاء الاصطناعي الشاملة لـ Dealix.

Each layer is a self-contained, dependency-free module that gracefully
upgrades when optional libraries (sentence-transformers, scikit-learn,
numpy, etc.) are installed.

Layer index:
    Foundations       embeddings, vector_store, chunker
    Extraction        ner, keyphrase, relation, pii
    Transformation    summarizer, translator, zeroshot
    Retrieval         rag, recommender
    Analytics         clustering, forecasting, anomaly
    Safety            safety, moderation
    Gateway           llm_gateway, prompt_cache, memory
    Knowledge         knowledge_graph
    Learning          feedback
    Orchestration     pipeline
"""

from dealix.intelligence.layers.anomaly import AnomalyDetector, AnomalyResult
from dealix.intelligence.layers.chunker import Chunk, SmartChunker
from dealix.intelligence.layers.clustering import KMeansLite, Cluster
from dealix.intelligence.layers.embeddings import EmbeddingModel, embed, embed_batch
from dealix.intelligence.layers.feedback import FeedbackStore, Feedback
from dealix.intelligence.layers.forecasting import Forecaster, ForecastResult
from dealix.intelligence.layers.keyphrase import KeyphraseExtractor, Keyphrase
from dealix.intelligence.layers.knowledge_graph import KnowledgeGraph, Triple
from dealix.intelligence.layers.llm_gateway import LLMGateway, GatewayResponse
from dealix.intelligence.layers.memory import ConversationMemory, Turn
from dealix.intelligence.layers.moderation import Moderator, ModerationResult
from dealix.intelligence.layers.ner import NERTagger, Entity
from dealix.intelligence.layers.pii import PIIRedactor, PIIMatch
from dealix.intelligence.layers.pipeline import Pipeline, PipelineStep
from dealix.intelligence.layers.prompt_cache import PromptCache
from dealix.intelligence.layers.rag import RAGEngine, RAGResult
from dealix.intelligence.layers.recommender import ContentRecommender, Recommendation
from dealix.intelligence.layers.relation import RelationExtractor
from dealix.intelligence.layers.safety import SafetyClassifier, SafetyResult
from dealix.intelligence.layers.summarizer import ExtractiveSummarizer
from dealix.intelligence.layers.translator import Translator
from dealix.intelligence.layers.vector_store import VectorStore, VectorRecord
from dealix.intelligence.layers.zeroshot import ZeroShotClassifier, ZeroShotResult

__all__ = [
    "AnomalyDetector",
    "AnomalyResult",
    "Chunk",
    "Cluster",
    "ContentRecommender",
    "ConversationMemory",
    "EmbeddingModel",
    "Entity",
    "ExtractiveSummarizer",
    "Feedback",
    "FeedbackStore",
    "ForecastResult",
    "Forecaster",
    "GatewayResponse",
    "KMeansLite",
    "Keyphrase",
    "KeyphraseExtractor",
    "KnowledgeGraph",
    "LLMGateway",
    "ModerationResult",
    "Moderator",
    "NERTagger",
    "PIIMatch",
    "PIIRedactor",
    "Pipeline",
    "PipelineStep",
    "PromptCache",
    "RAGEngine",
    "RAGResult",
    "Recommendation",
    "RelationExtractor",
    "SafetyClassifier",
    "SafetyResult",
    "SmartChunker",
    "Translator",
    "Triple",
    "Turn",
    "VectorRecord",
    "VectorStore",
    "ZeroShotClassifier",
    "ZeroShotResult",
    "embed",
    "embed_batch",
]
