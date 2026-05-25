"""
workflows — declarative workflow loader.

Workflows are defined in YAML under ``workflows/configs/`` and loaded
into typed objects at import time. The runner enforces gates and
outcome recording before marking a workflow complete.
"""

from dealix.hermes.workflows.loader import (
    WORKFLOW_REGISTRY,
    WorkflowDefinition,
    load_all,
)

__all__ = ["WORKFLOW_REGISTRY", "WorkflowDefinition", "load_all"]
