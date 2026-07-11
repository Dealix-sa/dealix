"""Canonical domain contracts for Dealix's multi-department Commercial Universe.

The contracts are intentionally deterministic and side-effect free. They model
strategy, approvals, meetings, and relationship memory without sending messages,
booking calendars, charging customers, or mutating external systems.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum