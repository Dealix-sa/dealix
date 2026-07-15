"""
Clustering layer — KMeans-lite for vector segmentation.
طبقة التجميع — KMeans مختصر لتقسيم العملاء أو المحادثات.

Pure-Python implementation: deterministic seeding (k-means++), Lloyd's
algorithm, silhouette score for k-quality.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Sequence

from dealix.intelligence.layers.embeddings import cosine_similarity


def _euclidean(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _centroid(points: list[Sequence[float]]) -> list[float]:
    if not points:
        return []
    dim = len(points[0])
    out = [0.0] * dim
    for p in points:
        for i in range(dim):
            out[i] += p[i]
    return [v / len(points) for v in out]


@dataclass
class Cluster:
    id: int
    centroid: list[float]
    member_indices: list[int] = field(default_factory=list)
    member_ids: list[str] = field(default_factory=list)
    inertia: float = 0.0


@dataclass(frozen=True)
class ClusteringResult:
    clusters: tuple[Cluster, ...]
    iterations: int
    total_inertia: float
    silhouette: float


class KMeansLite:
    """Cosine + Euclidean KMeans (Lloyd) with k-means++ seeding."""

    def __init__(
        self,
        k: int,
        *,
        max_iter: int = 50,
        tol: float = 1e-4,
        random_state: int = 42,
        metric: str = "euclidean",  # "euclidean" or "cosine"
    ) -> None:
        if k < 1:
            raise ValueError("k must be >= 1")
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        if metric not in ("euclidean", "cosine"):
            raise ValueError("metric must be euclidean or cosine")
        self.metric = metric

    def fit(
        self,
        vectors: Sequence[Sequence[float]],
        *,
        ids: Sequence[str] | None = None,
    ) -> ClusteringResult:
        n = len(vectors)
        if n == 0:
            return ClusteringResult(tuple(), 0, 0.0, 0.0)
        ids = list(ids) if ids else [str(i) for i in range(n)]
        k = min(self.k, n)
        rng = random.Random(self.random_state)
        centroids = self._kmeans_plus_plus_seed(vectors, k, rng)
        assignments = [0] * n
        prev_inertia = float("inf")
        iters = 0
        for it in range(self.max_iter):
            iters = it + 1
            # Assign
            new_assignments = [
                self._nearest_centroid(vectors[i], centroids) for i in range(n)
            ]
            # Update centroids
            groups: list[list[Sequence[float]]] = [[] for _ in range(k)]
            for i, c in enumerate(new_assignments):
                groups[c].append(vectors[i])
            new_centroids: list[list[float]] = []
            for j in range(k):
                if groups[j]:
                    new_centroids.append(_centroid(groups[j]))
                else:
                    # Reseed empty cluster from a random point.
                    new_centroids.append(list(vectors[rng.randrange(n)]))
            inertia = 0.0
            for i in range(n):
                inertia += self._dist(vectors[i], new_centroids[new_assignments[i]]) ** 2
            if abs(prev_inertia - inertia) < self.tol:
                centroids = new_centroids
                assignments = new_assignments
                break
            centroids = new_centroids
            assignments = new_assignments
            prev_inertia = inertia
        # Build clusters
        clusters: list[Cluster] = []
        for j in range(k):
            mem_idx = [i for i, c in enumerate(assignments) if c == j]
            mem_ids = [ids[i] for i in mem_idx]
            cluster_inertia = 0.0
            for i in mem_idx:
                cluster_inertia += self._dist(vectors[i], centroids[j]) ** 2
            clusters.append(
                Cluster(
                    id=j,
                    centroid=list(centroids[j]),
                    member_indices=mem_idx,
                    member_ids=mem_ids,
                    inertia=round(cluster_inertia, 4),
                )
            )
        total_inertia = sum(c.inertia for c in clusters)
        sil = self._silhouette(vectors, assignments, centroids) if k > 1 else 0.0
        return ClusteringResult(
            clusters=tuple(clusters),
            iterations=iters,
            total_inertia=round(total_inertia, 4),
            silhouette=round(sil, 4),
        )

    # ── Internals ─────────────────────────────────────────────────
    def _dist(self, a: Sequence[float], b: Sequence[float]) -> float:
        if self.metric == "cosine":
            return 1.0 - cosine_similarity(a, b)
        return _euclidean(a, b)

    def _nearest_centroid(
        self, point: Sequence[float], centroids: Sequence[Sequence[float]]
    ) -> int:
        best_idx = 0
        best_dist = float("inf")
        for j, c in enumerate(centroids):
            d = self._dist(point, c)
            if d < best_dist:
                best_dist = d
                best_idx = j
        return best_idx

    def _kmeans_plus_plus_seed(
        self, vectors: Sequence[Sequence[float]], k: int, rng: random.Random
    ) -> list[list[float]]:
        n = len(vectors)
        centroids: list[list[float]] = [list(vectors[rng.randrange(n)])]
        for _ in range(k - 1):
            d2 = [
                min(self._dist(v, c) ** 2 for c in centroids)
                for v in vectors
            ]
            total = sum(d2) or 1.0
            r = rng.random() * total
            cum = 0.0
            chosen = len(vectors) - 1
            for i, w in enumerate(d2):
                cum += w
                if cum >= r:
                    chosen = i
                    break
            centroids.append(list(vectors[chosen]))
        return centroids

    def _silhouette(
        self,
        vectors: Sequence[Sequence[float]],
        assignments: list[int],
        centroids: list[list[float]],
    ) -> float:
        n = len(vectors)
        if n < 2:
            return 0.0
        sample_n = min(n, 64)
        idxs = list(range(n))
        # Build per-cluster member lists
        members: dict[int, list[int]] = {}
        for i, c in enumerate(assignments):
            members.setdefault(c, []).append(i)
        scores: list[float] = []
        for i in idxs[:sample_n]:
            own = assignments[i]
            if len(members.get(own, [])) < 2:
                continue
            a = sum(self._dist(vectors[i], vectors[j]) for j in members[own] if j != i) / max(
                1, len(members[own]) - 1
            )
            b = float("inf")
            for c, ms in members.items():
                if c == own or not ms:
                    continue
                d = sum(self._dist(vectors[i], vectors[j]) for j in ms) / len(ms)
                if d < b:
                    b = d
            if b == float("inf"):
                continue
            if max(a, b) > 0:
                scores.append((b - a) / max(a, b))
        return sum(scores) / max(1, len(scores))
