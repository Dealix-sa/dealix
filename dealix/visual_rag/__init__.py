"""Optional visual retrieval layer for Dealix.

This package intentionally keeps PixelRAG behind an adapter boundary. Dealix can
run without PixelRAG installed, which protects CI and production while allowing a
separate Python 3.12 worker or CLI tool to provide visual evidence retrieval.
"""

from dealix.visual_rag.adapter import VisualRAGAdapter
from dealix.visual_rag.contracts import (
    VisualRAGJob,
    VisualRAGMode,
    VisualRAGResult,
    VisualRAGSource,
    VisualRAGSensitivity,
)

__all__ = [
    "VisualRAGAdapter",
    "VisualRAGJob",
    "VisualRAGMode",
    "VisualRAGResult",
    "VisualRAGSource",
    "VisualRAGSensitivity",
]
