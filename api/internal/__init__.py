"""
Internal Dealix API package — founder console + admin-only read endpoints.

These endpoints are gated by the X-Dealix-Internal-Token header and write
only to the private ops CSV root (DEALIX_PRIVATE_OPS_ROOT). They never
trigger external execution.
"""

from __future__ import annotations
