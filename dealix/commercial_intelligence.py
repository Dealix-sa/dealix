"""Governed source intelligence for the Dealix Commercial Universe.

Pure domain logic only: no scraping, sending, persistence, or connector calls.
Every observation is tenant-scoped, purpose-limited, expiring, and evidence-backed.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class SourceKind(StrEnum):
    OWNED = "owned"
    CRM = "crm"
    EMAIL = "email"
   