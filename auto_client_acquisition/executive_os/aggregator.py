"""Convene all 7 role briefs — degrade per-role, never crash.

Wraps ``role_command_os.build_role_brief`` for every role. A role that
fails to compose yields ``None`` and is reported via
``aggregator_degraded_roles`` rather than aborting the tick.
"""

from __future__ import annotations

from auto_client_acquisition.role_command_os import (
    RoleBrief,
    RoleName,
    build_role_brief,
)


def build_all_role_briefs() -> dict[str, RoleBrief | None]:
    """Build every role brief; failed roles map to ``None``."""
    out: dict[str, RoleBrief | None] = {}
    for role in RoleName:
        try:
            out[role.value] = build_role_brief(role)
        except Exception:
            out[role.value] = None
    return out


def aggregator_degraded_roles(briefs: dict[str, RoleBrief | None]) -> list[str]:
    """Return the role names that failed to compose."""
    return [role for role, brief in briefs.items() if brief is None]


__all__ = ["aggregator_degraded_roles", "build_all_role_briefs"]
