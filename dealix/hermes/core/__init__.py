"""Hermes kernel — the seven-stage pipeline.

Stages:
    Signal → Opportunity → Decision → Execution → Outcome → Asset → Scale

Each stage is a pure module with explicit schemas. The orchestrator binds
them together; nothing else may bypass a stage.
"""

from __future__ import annotations
