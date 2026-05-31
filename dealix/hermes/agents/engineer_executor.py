"""dealix-engineer executor — produces a code-change envelope."""

from __future__ import annotations

from typing import Any

from ..router import Route
from ._envelope import build_envelope


_ENGINEER_CONSTRAINTS: list[str] = [
    "Honor all 11 non-negotiables; pass tests/test_no_* before commit.",
    "Reuse canonical modules: data_os, governance_os, proof_os, value_os, capital_os, adoption_os, friction_log, client_os, sales_os.",
    "Type hints required. No emojis in code. No model identifiers in code comments or commit messages.",
    "Never push to main; work on the configured feature branch.",
    "Every new data flow has a passing pytest under tests/.",
]


def engineer_executor(task: Any, route: Route) -> dict[str, Any]:
    return build_envelope(
        task=task,
        route=route,
        role="engineer",
        system_constraints=_ENGINEER_CONSTRAINTS,
        deliverable=(
            "Patch set: list of file paths to modify, the diff per file, the test(s) "
            "added/modified, and the verification command to run."
        ),
    )
