"""Governed data-intelligence primitives for the Commercial Universe.

This module does not fetch, scrape, send, or persist external data. It defines the
contract every connector must satisfy before an observation can become a signal,
opportunity, action, or KPI contribution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from