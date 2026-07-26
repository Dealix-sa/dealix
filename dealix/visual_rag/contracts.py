"""Contracts for Dealix VisualRAG jobs and results.

These models are dependency-light on purpose. They do not import PixelRAG,
Playwright, Torch, FAISS, or any remote SDK. The actual renderer/search backend
is selected by the adapter at runtime.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, TypeAdapter, model_validator

_URL_ADAPTER = TypeAdapter(HttpUrl)


class VisualRAGMode(StrEnum):
    """Execution mode for a visual retrieval job."""

    DISABLED = "disabled"
    SCREENSHOT_ONLY = "screenshot_only"
    HOSTED_SEARCH = "hosted_search"
    PRIVATE_WORKER = "private_worker"


class VisualRAGSensitivity(StrEnum):
    """Sensitivity classification for rendered or indexed material."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CLIENT_CONFIDENTIAL = "client_confidential"
    REGULATED = "regulated"


class VisualRAGSource(BaseModel):
    """A visual source to render or search."""

    kind: Literal["url", "local_file", "uploaded_file", "text_note"]
    uri: str = Field(..., min_length=1)
    title: str | None = None
    source_id: str | None = None

    @model_validator(mode="after")
    def validate_url_shape(self) -> VisualRAGSource:
        if self.kind == "url":
            # Validate shape without coercing the stored value.
            _URL_ADAPTER.validate_python(self.uri)
        return self


class VisualRAGJob(BaseModel):
    """A request to render, search, or attach visual evidence."""

    job_id: str = Field(..., min_length=3)
    mode: VisualRAGMode = VisualRAGMode.DISABLED
    sources: list[VisualRAGSource] = Field(default_factory=list)
    query: str | None = None
    n_docs: int = Field(default=5, ge=1, le=20)
    sensitivity: VisualRAGSensitivity = VisualRAGSensitivity.INTERNAL
    allow_external_processing: bool = False
    require_human_approval: bool = True
    proof_pack_id: str | None = None
    retention_days: int = Field(default=30, ge=0, le=3650)
    metadata: dict[str, Any] = Field(default_factory=dict)


class VisualRAGTile(BaseModel):
    """Reference to a screenshot tile or visual evidence artifact."""

    tile_id: str
    source_id: str | None = None
    page: int | None = None
    score: float | None = None
    image_path: str | None = None
    image_url: str | None = None
    snippet: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class VisualRAGResult(BaseModel):
    """Normalized result returned by any VisualRAG backend."""

    job_id: str
    status: Literal["disabled", "blocked", "pending_approval", "ok", "error"]
    mode: VisualRAGMode
    message: str
    tiles: list[VisualRAGTile] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
