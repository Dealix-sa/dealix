"""
Risk Controls library (Section 55).

Categories aligned with the AI risk mitigation taxonomy:
    - GOV  : Governance & Oversight
    - SEC  : Technical & Security
    - OPS  : Operational Process
    - TRANS: Transparency & Accountability
    - COM  : Commercial

كل control عبارة عن دالة `(ctx: dict) -> ControlVerdict` تُستدعى من
runtime/gates أو من workspace audits.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ControlSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ControlVerdict:
    control_id: str
    passed: bool
    severity: ControlSeverity
    detail: str
    metadata: dict[str, Any] = field(default_factory=dict)


ControlFn = Callable[[dict[str, Any]], ControlVerdict]


@dataclass(frozen=True)
class Control:
    control_id: str
    name: str
    category: str  # "GOV" | "SEC" | "OPS" | "TRANS" | "COM"
    description: str
    default_severity: ControlSeverity
    fn: ControlFn


# ────────────────────────────────────────────────────────────────
# Control implementations
# ────────────────────────────────────────────────────────────────


def _ctrl_gov_001(ctx: dict[str, Any]) -> ControlVerdict:
    agent_owner = ctx.get("agent_owner")
    passed = bool(agent_owner)
    return ControlVerdict(
        control_id="CTRL-GOV-001",
        passed=passed,
        severity=ControlSeverity.HIGH,
        detail="agent must have a human owner" if not passed else "ok",
    )


def _ctrl_gov_002(ctx: dict[str, Any]) -> ControlVerdict:
    tool_owner = ctx.get("tool_owner")
    passed = bool(tool_owner)
    return ControlVerdict(
        control_id="CTRL-GOV-002",
        passed=passed,
        severity=ControlSeverity.HIGH,
        detail="tool must have a human owner" if not passed else "ok",
    )


def _ctrl_gov_003(ctx: dict[str, Any]) -> ControlVerdict:
    if not ctx.get("is_external_action"):
        return ControlVerdict(
            control_id="CTRL-GOV-003",
            passed=True,
            severity=ControlSeverity.INFO,
            detail="not an external action",
        )
    passed = bool(ctx.get("approval_ticket_id"))
    return ControlVerdict(
        control_id="CTRL-GOV-003",
        passed=passed,
        severity=ControlSeverity.HIGH,
        detail="external action requires approval ticket" if not passed else "ok",
    )


def _ctrl_sec_001(ctx: dict[str, Any]) -> ControlVerdict:
    sensitive = bool(ctx.get("contains_sensitive_data"))
    if not sensitive:
        return ControlVerdict(
            control_id="CTRL-SEC-001",
            passed=True,
            severity=ControlSeverity.INFO,
            detail="no sensitive data flagged",
        )
    passed = not bool(ctx.get("leaving_workspace"))
    return ControlVerdict(
        control_id="CTRL-SEC-001",
        passed=passed,
        severity=ControlSeverity.CRITICAL,
        detail=(
            "sensitive data cannot leave its workspace"
            if not passed
            else "ok"
        ),
    )


def _ctrl_sec_002(ctx: dict[str, Any]) -> ControlVerdict:
    if not ctx.get("mcp_server_id"):
        return ControlVerdict(
            control_id="CTRL-SEC-002",
            passed=True,
            severity=ControlSeverity.INFO,
            detail="no MCP server in scope",
        )
    passed = bool(ctx.get("mcp_review_signed_off"))
    return ControlVerdict(
        control_id="CTRL-SEC-002",
        passed=passed,
        severity=ControlSeverity.HIGH,
        detail="MCP server requires signed-off review" if not passed else "ok",
    )


def _ctrl_ops_001(ctx: dict[str, Any]) -> ControlVerdict:
    if not ctx.get("execution_id"):
        return ControlVerdict(
            control_id="CTRL-OPS-001",
            passed=True,
            severity=ControlSeverity.INFO,
            detail="no execution in scope",
        )
    passed = bool(ctx.get("outcome_recorded"))
    return ControlVerdict(
        control_id="CTRL-OPS-001",
        passed=passed,
        severity=ControlSeverity.MEDIUM,
        detail="every execution requires an outcome" if not passed else "ok",
    )


def _ctrl_ops_002(ctx: dict[str, Any]) -> ControlVerdict:
    if not ctx.get("incident_id"):
        return ControlVerdict(
            control_id="CTRL-OPS-002",
            passed=True,
            severity=ControlSeverity.INFO,
            detail="no incident in scope",
        )
    passed = bool(ctx.get("remediation_recorded"))
    return ControlVerdict(
        control_id="CTRL-OPS-002",
        passed=passed,
        severity=ControlSeverity.HIGH,
        detail="incident requires remediation" if not passed else "ok",
    )


def _ctrl_trans_001(ctx: dict[str, Any]) -> ControlVerdict:
    if not ctx.get("contains_external_claim"):
        return ControlVerdict(
            control_id="CTRL-TRANS-001",
            passed=True,
            severity=ControlSeverity.INFO,
            detail="no external claim",
        )
    passed = bool(ctx.get("evidence_pack_id") or ctx.get("citation_url"))
    return ControlVerdict(
        control_id="CTRL-TRANS-001",
        passed=passed,
        severity=ControlSeverity.HIGH,
        detail="external claim requires evidence" if not passed else "ok",
    )


def _ctrl_com_001(ctx: dict[str, Any]) -> ControlVerdict:
    if not ctx.get("enterprise_pricing"):
        return ControlVerdict(
            control_id="CTRL-COM-001",
            passed=True,
            severity=ControlSeverity.INFO,
            detail="not enterprise pricing",
        )
    passed = bool(ctx.get("founder_approved"))
    return ControlVerdict(
        control_id="CTRL-COM-001",
        passed=passed,
        severity=ControlSeverity.HIGH,
        detail="enterprise pricing requires founder approval" if not passed else "ok",
    )


_DEFAULT_CONTROLS: tuple[Control, ...] = (
    Control(
        "CTRL-GOV-001",
        "Agent must have owner",
        "GOV",
        "Every agent registered in the system must have a human owner.",
        ControlSeverity.HIGH,
        _ctrl_gov_001,
    ),
    Control(
        "CTRL-GOV-002",
        "Tool must have owner",
        "GOV",
        "Every tool registered must have a human owner.",
        ControlSeverity.HIGH,
        _ctrl_gov_002,
    ),
    Control(
        "CTRL-GOV-003",
        "External action requires approval",
        "GOV",
        "Any external-facing action requires an approval ticket id.",
        ControlSeverity.HIGH,
        _ctrl_gov_003,
    ),
    Control(
        "CTRL-SEC-001",
        "Sensitive data cannot leave workspace",
        "SEC",
        "Sensitive data outputs must not cross workspace boundaries.",
        ControlSeverity.CRITICAL,
        _ctrl_sec_001,
    ),
    Control(
        "CTRL-SEC-002",
        "MCP server requires review",
        "SEC",
        "MCP servers must be reviewed and signed off before use.",
        ControlSeverity.HIGH,
        _ctrl_sec_002,
    ),
    Control(
        "CTRL-OPS-001",
        "Every execution requires outcome",
        "OPS",
        "Every execution must produce an outcome record.",
        ControlSeverity.MEDIUM,
        _ctrl_ops_001,
    ),
    Control(
        "CTRL-OPS-002",
        "Incident requires remediation",
        "OPS",
        "Every incident must record a remediation step.",
        ControlSeverity.HIGH,
        _ctrl_ops_002,
    ),
    Control(
        "CTRL-TRANS-001",
        "External claim requires evidence",
        "TRANS",
        "Any external-facing claim must reference an evidence pack or citation.",
        ControlSeverity.HIGH,
        _ctrl_trans_001,
    ),
    Control(
        "CTRL-COM-001",
        "Enterprise pricing requires approval",
        "COM",
        "Enterprise-level pricing requires founder approval.",
        ControlSeverity.HIGH,
        _ctrl_com_001,
    ),
)


class ControlLibrary:
    def __init__(self) -> None:
        self._controls: dict[str, Control] = {}
        self._lock = threading.Lock()

    def register(self, control: Control) -> None:
        with self._lock:
            if control.control_id in self._controls:
                raise ValueError(f"control `{control.control_id}` already registered")
            self._controls[control.control_id] = control

    def all(self) -> list[Control]:
        with self._lock:
            return list(self._controls.values())

    def evaluate_all(self, ctx: dict[str, Any]) -> list[ControlVerdict]:
        with self._lock:
            controls = list(self._controls.values())
        return [c.fn(ctx) for c in controls]

    def failures(self, ctx: dict[str, Any]) -> list[ControlVerdict]:
        return [v for v in self.evaluate_all(ctx) if not v.passed]


def default_library() -> ControlLibrary:
    lib = ControlLibrary()
    for c in _DEFAULT_CONTROLS:
        lib.register(c)
    return lib


__all__ = [
    "Control",
    "ControlFn",
    "ControlLibrary",
    "ControlSeverity",
    "ControlVerdict",
    "default_library",
]
