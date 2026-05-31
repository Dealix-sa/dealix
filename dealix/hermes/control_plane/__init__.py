"""
control_plane — the runtime that wraps every agent / tool / workflow call.

A call is legitimate if and only if it passes, in order:

    request_context -> actor_identity -> policy_enforcement
        -> sovereignty_gate -> trust_gate -> data_gate -> tool_gate
        -> approval_gate -> (execute) -> audit_gate -> outcome_gate

At any point, ``kill_switch`` can short-circuit execution for an agent,
tool, or workflow.

The package ``__init__`` is intentionally minimal so that ``identity``
modules can pull lightweight pieces (``sovereignty_gate``,
``runtime_modes``) without triggering the full runtime chain. The
heavier ``runtime`` symbols are lazy-loaded through ``__getattr__``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from dealix.hermes.control_plane.runtime_modes import RuntimeMode

if TYPE_CHECKING:
    from dealix.hermes.control_plane.runtime import (
        ControlPlaneDecision,
        ControlPlaneRuntime,
        RuntimeOutcome,
    )

_LAZY = {
    "ControlPlaneRuntime": ("dealix.hermes.control_plane.runtime", "ControlPlaneRuntime"),
    "ControlPlaneDecision": ("dealix.hermes.control_plane.runtime", "ControlPlaneDecision"),
    "RuntimeOutcome": ("dealix.hermes.control_plane.runtime", "RuntimeOutcome"),
}


def __getattr__(name: str):
    if name in _LAZY:
        import importlib

        module_name, attr = _LAZY[name]
        return getattr(importlib.import_module(module_name), attr)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["ControlPlaneDecision", "ControlPlaneRuntime", "RuntimeMode", "RuntimeOutcome"]
