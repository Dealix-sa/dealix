"""
Hermes control plane — the single entry point that composes identity,
comms, MCP, provenance, and audit into a coherent agentic plane.
"""

from __future__ import annotations

from dealix.hermes.control_plane.plane import (
    ControlPlane,
    ControlPlaneDecision,
)

__all__ = ["ControlPlane", "ControlPlaneDecision"]
