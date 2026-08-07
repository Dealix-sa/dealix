"""Optional adapter for PixelRAG-compatible visual evidence retrieval.

This adapter does not import PixelRAG by default. Dealix remains usable in CI,
Railway, and Python 3.11 environments. PixelRAG should run separately as a
private worker or hosted public endpoint.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dealix.visual_rag.contracts import (
    VisualRAGJob,
    VisualRAGMode,
    VisualRAGResult,
    VisualRAGTile,
)
from dealix.visual_rag.policies import evaluate_visual_rag_job


@dataclass(frozen=True)
class VisualRAGAdapterConfig:
    """Runtime configuration for the VisualRAG adapter."""

    hosted_search_url: str | None = None
    private_worker_url: str | None = None
    pixelshot_bin: str = "pixelshot"
    output_root: Path = Path("reports/visual_rag")
    request_timeout_seconds: int = 30

    @classmethod
    def from_env(cls) -> VisualRAGAdapterConfig:
        return cls(
            hosted_search_url=os.getenv("DEALIX_PIXELRAG_HOSTED_SEARCH_URL"),
            private_worker_url=os.getenv("DEALIX_PIXELRAG_PRIVATE_WORKER_URL"),
            pixelshot_bin=os.getenv("DEALIX_PIXELSHOT_BIN", "pixelshot"),
            output_root=Path(os.getenv("DEALIX_VISUAL_RAG_OUTPUT_ROOT", "reports/visual_rag")),
            request_timeout_seconds=int(os.getenv("DEALIX_VISUAL_RAG_TIMEOUT_SECONDS", "30")),
        )


class VisualRAGAdapter:
    """Boundary between Dealix workflows and PixelRAG-compatible backends."""

    def __init__(self, config: VisualRAGAdapterConfig | None = None) -> None:
        self.config = config or VisualRAGAdapterConfig.from_env()

    def run(self, job: VisualRAGJob) -> VisualRAGResult:
        """Run a VisualRAG job or return a safe blocked/disabled result."""

        decision = evaluate_visual_rag_job(job)
        if not decision.allowed:
            return VisualRAGResult(
                job_id=job.job_id,
                status="blocked" if job.mode != VisualRAGMode.DISABLED else "disabled",
                mode=job.mode,
                message=decision.reason,
                warnings=list(decision.warnings),
                next_actions=[
                    "Review docs/commercial/PIXELRAG_VISUAL_EVIDENCE_LAYER.md",
                    "Use screenshot_only for public/manual evidence or private_worker for client documents.",
                ],
            )

        if job.require_human_approval:
            return VisualRAGResult(
                job_id=job.job_id,
                status="pending_approval",
                mode=job.mode,
                message="VisualRAG job passed policy but requires human approval before execution.",
                warnings=list(decision.warnings),
                next_actions=["Approve the visual evidence job, then rerun with require_human_approval=False."],
            )

        if job.mode == VisualRAGMode.SCREENSHOT_ONLY:
            return self._prepare_screenshot_job(job, warnings=list(decision.warnings))

        if job.mode == VisualRAGMode.HOSTED_SEARCH:
            return self._run_search(job, self.config.hosted_search_url, warnings=list(decision.warnings))

        if job.mode == VisualRAGMode.PRIVATE_WORKER:
            return self._run_search(job, self.config.private_worker_url, warnings=list(decision.warnings))

        return VisualRAGResult(
            job_id=job.job_id,
            status="error",
            mode=job.mode,
            message=f"Unsupported VisualRAG mode: {job.mode}",
        )

    def _prepare_screenshot_job(self, job: VisualRAGJob, warnings: list[str]) -> VisualRAGResult:
        """Prepare a screenshot job for an external worker instead of executing locally."""

        return VisualRAGResult(
            job_id=job.job_id,
            status="pending_approval",
            mode=job.mode,
            message="Screenshot capture is prepared for a PixelRAG worker; main Dealix app does not execute local browser tooling.",
            warnings=warnings,
            next_actions=[
                "Run the approved job on the private PixelRAG worker.",
                "Store generated tiles under the configured visual evidence output path.",
                "Attach reviewed tiles through the proof-pack bridge.",
            ],
            metadata={
                "output_root": str(self.config.output_root),
                "pixelshot_bin": self.config.pixelshot_bin,
                "source_count": len(job.sources),
            },
        )

    def _run_search(
        self, job: VisualRAGJob, endpoint_url: str | None, warnings: list[str]
    ) -> VisualRAGResult:
        if not endpoint_url:
            return VisualRAGResult(
                job_id=job.job_id,
                status="error",
                mode=job.mode,
                message="No PixelRAG-compatible search endpoint is configured.",
                warnings=warnings,
                next_actions=[
                    "Set DEALIX_PIXELRAG_HOSTED_SEARCH_URL for public hosted search.",
                    "Set DEALIX_PIXELRAG_PRIVATE_WORKER_URL for private client-document search.",
                ],
            )

        if not job.query:
            return VisualRAGResult(
                job_id=job.job_id,
                status="error",
                mode=job.mode,
                message="Visual search requires a query.",
                warnings=warnings,
            )

        payload: dict[str, Any] = {
            "queries": [{"text": job.query}],
            "n_docs": job.n_docs,
            "metadata": {"dealix_job_id": job.job_id, **job.metadata},
        }
        request = urllib.request.Request(
            endpoint_url.rstrip("/") + "/search",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.config.request_timeout_seconds) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return VisualRAGResult(
                job_id=job.job_id,
                status="error",
                mode=job.mode,
                message=f"Visual search request failed: {exc}",
                warnings=warnings,
            )

        tiles = _normalize_search_tiles(job.job_id, parsed)
        return VisualRAGResult(
            job_id=job.job_id,
            status="ok",
            mode=job.mode,
            message=f"Retrieved {len(tiles)} visual search results.",
            tiles=tiles,
            warnings=warnings,
            next_actions=["Review retrieved evidence before using it in a proof pack or client output."],
            metadata={"raw_result_keys": sorted(parsed.keys()) if isinstance(parsed, dict) else []},
        )


def _normalize_search_tiles(job_id: str, parsed: Any) -> list[VisualRAGTile]:
    """Best-effort normalization for PixelRAG-compatible search responses."""

    items: list[Any]
    if isinstance(parsed, dict):
        if isinstance(parsed.get("results"), list):
            items = parsed["results"]
        elif isinstance(parsed.get("documents"), list):
            items = parsed["documents"]
        elif isinstance(parsed.get("data"), list):
            items = parsed["data"]
        else:
            items = []
    elif isinstance(parsed, list):
        items = parsed
    else:
        items = []

    tiles: list[VisualRAGTile] = []
    numeric_score_types = (int, float)
    for i, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        score = item.get("score")
        tiles.append(
            VisualRAGTile(
                tile_id=str(item.get("tile_id") or item.get("id") or f"{job_id}:search:{i}"),
                source_id=item.get("source_id") or item.get("doc_id") or item.get("url"),
                page=item.get("page") if isinstance(item.get("page"), int) else None,
                score=float(score) if isinstance(score, numeric_score_types) else None,
                image_path=item.get("image_path"),
                image_url=item.get("image_url") or item.get("thumbnail_url"),
                snippet=item.get("snippet") or item.get("text"),
                metadata={key: value for key, value in item.items() if key not in {"embedding"}},
            )
        )
    return tiles
