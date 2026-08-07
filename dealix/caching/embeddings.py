"""Local Arabic-friendly embeddings with a zero-dependency fallback.

When ``sentence-transformers`` is installed, Dealix uses the multilingual
MiniLM model.  The production API intentionally does not install that large
optional model; in that environment a deterministic Unicode token/character
hash vector keeps the semantic cache functional without pulling NumPy into
every Vercel Function bundle.
"""

from __future__ import annotations

import hashlib
import math
import re
import threading
from collections.abc import Sequence

_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
_EMBED_DIM = 384


class LocalEmbedder:
    """Thread-safe lazy-loaded local embedder.

    The underlying sentence-transformers model is heavy (~118 MB) so we load it
    on first use and keep it as a class-level singleton.
    """

    _lock = threading.Lock()
    _model = None  # type: ignore[assignment]
    _model_unavailable = False

    @classmethod
    def _get_model(cls):  # pragma: no cover — external dep
        if cls._model is None and not cls._model_unavailable:
            with cls._lock:
                if cls._model is None and not cls._model_unavailable:
                    try:
                        from sentence_transformers import SentenceTransformer  # type: ignore
                    except ImportError:
                        cls._model_unavailable = True
                        return None
                    cls._model = SentenceTransformer(_MODEL_NAME)
        return cls._model

    @staticmethod
    def fingerprint(text: str) -> str:
        """Deterministic short hash — used as Redis sub-key."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def embed(cls, text: str) -> list[float]:
        """Return a deterministic, L2-normalized 384-dimensional vector."""
        model = cls._get_model()
        if model is None:
            return cls._fallback_embed(text)

        encoded = model.encode(text, convert_to_numpy=False, normalize_embeddings=True)
        values = encoded.tolist() if hasattr(encoded, "tolist") else list(encoded)
        if values and isinstance(values[0], list):
            values = values[0]
        return [float(value) for value in values]

    @staticmethod
    def _fallback_embed(text: str) -> list[float]:
        """Create a compact lexical vector that works for Arabic and English.

        Tokens and Unicode character trigrams are feature-hashed into a fixed
        vector.  This is deliberately deterministic across processes and does
        not claim model-level semantic understanding.
        """
        normalized = " ".join(text.casefold().split())
        tokens = re.findall(r"[^\W_]+", normalized, flags=re.UNICODE)
        features = [f"token:{token}" for token in tokens]
        compact = normalized.replace(" ", "_")
        features.extend(
            f"tri:{compact[index:index + 3]}"
            for index in range(max(0, len(compact) - 2))
        )

        vector = [0.0] * _EMBED_DIM
        for feature in features:
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
            index = int.from_bytes(digest[:4], "big") % _EMBED_DIM
            sign = 1.0 if digest[4] & 1 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            return [value / norm for value in vector]
        return vector

    @staticmethod
    def similarity(a: Sequence[float], b: Sequence[float]) -> float:
        """Cosine similarity without requiring a numeric runtime package."""
        if len(a) != len(b) or not a:
            return 0.0
        dot = sum(left * right for left, right in zip(a, b, strict=True))
        left_norm = math.sqrt(sum(value * value for value in a))
        right_norm = math.sqrt(sum(value * value for value in b))
        denominator = left_norm * right_norm
        return dot / denominator if denominator else 0.0


DIM = _EMBED_DIM
