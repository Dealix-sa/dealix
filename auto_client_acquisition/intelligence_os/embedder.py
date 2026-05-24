"""Embedding layer — provider-agnostic text → vector with a deterministic fallback.

The embedder hides the choice of provider behind a single :class:`Embedder`
class. Production deployments inject a callable that wraps the chosen LLM
provider (OpenAI ``text-embedding-3-small``, Cohere ``embed-v3``, …);
in tests and during development we fall back to a deterministic, low-cost
hash-bucket embedder that is good enough for similarity smoke checks and
never makes a network call.

The fallback is **strictly local and deterministic**: the same input always
produces the same vector. It is not a real embedding — callers MUST inject a
production provider before relying on the vector for semantic retrieval.
"""

from __future__ import annotations

import hashlib
import math
import re
import threading
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass

# Default dimension of the deterministic local fallback embedder. Production
# providers (OpenAI text-embedding-3-small is 1536) override this via
# ``Embedder(dimension=...)``.
DEFAULT_DIMENSION: int = 256

_WORD_RE = re.compile(r"[\w؀-ۿ]+", re.UNICODE)


def _hash_bucket(token: str, *, dimension: int) -> int:
    """Map a token to a stable bucket in ``[0, dimension)``."""
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    # Use the first 8 bytes for plenty of entropy without huge ints.
    return int.from_bytes(digest[:8], "big") % dimension


def _l2_normalize(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm <= 0.0:
        return vec
    return [v / norm for v in vec]


def deterministic_embed(text: str, *, dimension: int = DEFAULT_DIMENSION) -> list[float]:
    """Local, deterministic, no-network embedding for tests + dev.

    Bag-of-hashed-tokens with TF weighting + L2 normalization. Tokens are
    matched against unicode word characters (covers Arabic + Latin).
    """
    if dimension <= 0:
        raise ValueError("dimension must be positive")
    if not text or not text.strip():
        return [0.0] * dimension
    tokens = [t.lower() for t in _WORD_RE.findall(text)]
    if not tokens:
        return [0.0] * dimension
    vec = [0.0] * dimension
    for token in tokens:
        vec[_hash_bucket(token, dimension=dimension)] += 1.0
    return _l2_normalize(vec)


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Cosine similarity in ``[-1, 1]``. Returns 0 for zero vectors."""
    if len(a) != len(b):
        raise ValueError(f"dimension mismatch: {len(a)} vs {len(b)}")
    num = sum(x * y for x, y in zip(a, b, strict=True))
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(y * y for y in b))
    if da <= 0.0 or db <= 0.0:
        return 0.0
    return num / (da * db)


@dataclass(slots=True)
class EmbeddingResult:
    """One embedding result with its source text and provider tag."""

    text: str
    vector: list[float]
    provider: str
    model: str
    dimension: int


# Provider callable signature: ``(texts) → list[list[float]]``.
EmbedderCallable = Callable[[Sequence[str]], list[list[float]]]


class Embedder:
    """Provider-agnostic embedder with a deterministic local fallback.

    Inject ``provider`` to swap in OpenAI / Cohere / Anthropic / etc.
    The provider receives a list of texts and must return a list of vectors
    of equal length and equal ``dimension``. If the provider raises or
    returns the wrong shape, the embedder transparently falls back to the
    deterministic local embedding for resilience (the fallback is logged
    via ``fallback_uses`` for observability).
    """

    __slots__ = ("_fallback_uses", "_lock", "dimension", "model", "provider", "provider_name")

    def __init__(
        self,
        *,
        dimension: int = DEFAULT_DIMENSION,
        provider: EmbedderCallable | None = None,
        provider_name: str = "local-deterministic",
        model: str = "hash-bucket-v1",
    ) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        self.dimension = dimension
        self.provider = provider
        self.provider_name = provider_name
        self.model = model
        self._lock = threading.Lock()
        self._fallback_uses = 0

    @property
    def fallback_uses(self) -> int:
        with self._lock:
            return self._fallback_uses

    def embed(self, text: str) -> EmbeddingResult:
        vec = self.embed_batch([text])[0]
        return EmbeddingResult(
            text=text,
            vector=vec,
            provider=self.provider_name,
            model=self.model,
            dimension=self.dimension,
        )

    def embed_batch(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        if self.provider is None:
            return [deterministic_embed(t, dimension=self.dimension) for t in texts]
        try:
            vectors = self.provider(list(texts))
        except Exception:
            with self._lock:
                self._fallback_uses += 1
            return [deterministic_embed(t, dimension=self.dimension) for t in texts]
        if (
            not isinstance(vectors, list)
            or len(vectors) != len(texts)
            or any(len(v) != self.dimension for v in vectors)
        ):
            with self._lock:
                self._fallback_uses += 1
            return [deterministic_embed(t, dimension=self.dimension) for t in texts]
        return [list(v) for v in vectors]

    def similarity(self, a: str, b: str) -> float:
        va, vb = self.embed_batch([a, b])
        return cosine_similarity(va, vb)


def chunk_text(
    text: str,
    *,
    chunk_chars: int = 800,
    overlap: int = 100,
) -> list[str]:
    """Naive char-window chunker for embedding pipelines.

    The chunker preserves order, applies overlap to avoid losing boundary
    sentences, and skips whitespace-only fragments.
    """
    if chunk_chars <= 0:
        raise ValueError("chunk_chars must be positive")
    if overlap < 0 or overlap >= chunk_chars:
        raise ValueError("overlap must satisfy 0 <= overlap < chunk_chars")
    if not text or not text.strip():
        return []
    chunks: list[str] = []
    start = 0
    step = chunk_chars - overlap
    while start < len(text):
        end = min(len(text), start + chunk_chars)
        fragment = text[start:end].strip()
        if fragment:
            chunks.append(fragment)
        if end >= len(text):
            break
        start += step
    return chunks


def embed_chunks(
    embedder: Embedder,
    chunks: Iterable[str],
) -> list[EmbeddingResult]:
    """Embed an iterable of text chunks in a single batch call."""
    items = list(chunks)
    vectors = embedder.embed_batch(items)
    return [
        EmbeddingResult(
            text=text,
            vector=vec,
            provider=embedder.provider_name,
            model=embedder.model,
            dimension=embedder.dimension,
        )
        for text, vec in zip(items, vectors, strict=True)
    ]


__all__ = [
    "DEFAULT_DIMENSION",
    "Embedder",
    "EmbedderCallable",
    "EmbeddingResult",
    "chunk_text",
    "cosine_similarity",
    "deterministic_embed",
    "embed_chunks",
]
