"""
Embeddings layer — bilingual sentence/text embeddings.
طبقة التضمينات — توليد متجهات دلالية للنصوص.

Strategy
--------
1. If ``sentence-transformers`` is installed, use a small multilingual model
   ("paraphrase-multilingual-MiniLM-L12-v2") and cache it module-level.
2. Otherwise, fall back to a deterministic hashed bag-of-character-trigrams
   embedding (dim=256) — small, fast, language-agnostic, and good enough for
   cosine similarity ranking inside Dealix's RAG / clustering / recommender.

The fallback is intentionally pure Python so unit tests and ephemeral
containers do not need to download model weights.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import threading
from dataclasses import dataclass
from typing import Iterable, Sequence

from dealix.intelligence.arabic_nlp import normalize_arabic

DEFAULT_DIM = 256
_MIN_DIM = 32
_MAX_DIM = 4096

_TRIGRAM_RE = re.compile(r"\s+")
_NON_WORD_RE = re.compile(r"[^\w؀-ۿ]+")

_MODEL_LOCK = threading.Lock()
_MODEL: object | None = None
_MODEL_DIM: int = 0
_MODEL_NAME = os.getenv(
    "DEALIX_EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


@dataclass(frozen=True)
class EmbeddingVector:
    """Container so callers can read both vector + backend used."""

    vector: tuple[float, ...]
    backend: str
    dim: int


def _try_load_sentence_transformer() -> tuple[object | None, int]:
    """Best-effort lazy load of sentence-transformers (cached module-wide)."""
    global _MODEL, _MODEL_DIM
    if _MODEL is not None:
        return _MODEL, _MODEL_DIM
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore

        with _MODEL_LOCK:
            if _MODEL is None:
                model = SentenceTransformer(_MODEL_NAME)
                _MODEL = model
                _MODEL_DIM = int(model.get_sentence_embedding_dimension())
    except Exception:  # pragma: no cover — env-dependent
        _MODEL = None
        _MODEL_DIM = 0
    return _MODEL, _MODEL_DIM


def _hashed_trigram_vector(text: str, dim: int) -> list[float]:
    """Deterministic hashed embedding — language-agnostic, no deps."""
    if not text:
        return [0.0] * dim
    norm = normalize_arabic(text.lower())
    norm = _NON_WORD_RE.sub(" ", norm)
    tokens = [t for t in _TRIGRAM_RE.split(norm) if t]
    vec = [0.0] * dim
    if not tokens:
        return vec
    for tok in tokens:
        # Character trigrams capture morphology in AR + EN.
        padded = f"  {tok}  "
        for i in range(len(padded) - 2):
            trigram = padded[i : i + 3]
            h = hashlib.blake2b(trigram.encode("utf-8"), digest_size=8).digest()
            idx = int.from_bytes(h[:4], "big") % dim
            # Sign hash — reduces collision bias (feature hashing trick).
            sign = 1.0 if (h[4] & 1) else -1.0
            vec[idx] += sign
    # L2 normalize so cosine similarity == dot product.
    norm_factor = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm_factor for v in vec]


class EmbeddingModel:
    """High-level embedding interface used by RAG, clustering, recommender."""

    def __init__(self, dim: int = DEFAULT_DIM, prefer_local: bool | None = None) -> None:
        self._fallback_dim = max(_MIN_DIM, min(int(dim), _MAX_DIM))
        if prefer_local is None:
            prefer_local = os.getenv("DEALIX_EMBED_PREFER_LOCAL", "1") == "1"
        self._prefer_local = bool(prefer_local)
        self._backend = "hashed-trigram"
        if self._prefer_local:
            model, mdim = _try_load_sentence_transformer()
            if model is not None and mdim > 0:
                self._fallback_dim = mdim
                self._backend = f"sentence-transformers:{_MODEL_NAME}"

    @property
    def backend(self) -> str:
        return self._backend

    @property
    def dim(self) -> int:
        return self._fallback_dim

    def embed(self, text: str) -> EmbeddingVector:
        vec = self._raw(text)
        return EmbeddingVector(tuple(vec), self._backend, len(vec))

    def embed_many(self, texts: Sequence[str]) -> list[EmbeddingVector]:
        return [self.embed(t) for t in texts]

    def _raw(self, text: str) -> list[float]:
        if self._backend.startswith("sentence-transformers"):
            try:
                arr = _MODEL.encode([text], normalize_embeddings=True)  # type: ignore[union-attr]
                return [float(x) for x in arr[0]]
            except Exception:  # pragma: no cover
                pass
        return _hashed_trigram_vector(text, self._fallback_dim)


# ── Module-level convenience helpers (singleton model) ──────────────
_DEFAULT_MODEL: EmbeddingModel | None = None


def _default() -> EmbeddingModel:
    global _DEFAULT_MODEL
    if _DEFAULT_MODEL is None:
        _DEFAULT_MODEL = EmbeddingModel()
    return _DEFAULT_MODEL


def embed(text: str) -> list[float]:
    return list(_default().embed(text).vector)


def embed_batch(texts: Iterable[str]) -> list[list[float]]:
    model = _default()
    return [list(model.embed(t).vector) for t in texts]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)
