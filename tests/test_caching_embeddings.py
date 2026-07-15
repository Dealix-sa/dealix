from __future__ import annotations

import math

from dealix.caching.embeddings import DIM, LocalEmbedder


def test_fallback_embedding_is_deterministic_and_normalized(monkeypatch) -> None:
    monkeypatch.setattr(LocalEmbedder, "_model", None)
    monkeypatch.setattr(LocalEmbedder, "_model_unavailable", True)

    first = LocalEmbedder.embed("فرص قطاع التقنية في الرياض")
    second = LocalEmbedder.embed("فرص قطاع التقنية في الرياض")

    assert first == second
    assert len(first) == DIM
    assert math.isclose(sum(value * value for value in first), 1.0, rel_tol=1e-9)


def test_fallback_similarity_prefers_related_text(monkeypatch) -> None:
    monkeypatch.setattr(LocalEmbedder, "_model", None)
    monkeypatch.setattr(LocalEmbedder, "_model_unavailable", True)

    query = LocalEmbedder.embed("شركة تقنية سعودية في الرياض")
    related = LocalEmbedder.embed("شركة تقنية في الرياض")
    unrelated = LocalEmbedder.embed("توريد معدات بحرية في جدة")

    assert LocalEmbedder.similarity(query, related) > LocalEmbedder.similarity(query, unrelated)


def test_similarity_rejects_mismatched_or_zero_vectors() -> None:
    assert LocalEmbedder.similarity([1.0], [1.0, 0.0]) == 0.0
    assert LocalEmbedder.similarity([0.0, 0.0], [1.0, 0.0]) == 0.0
