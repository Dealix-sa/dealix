"""Check if an action requires human approval per 06_APPROVAL_GATES.yml."""
from __future__ import annotations

from dataclasses import dataclass

from .config_loader import load_approval_gates


@dataclass
class GateCheckResult:
    action: str
    requires_approval: bool
    gate_id: str | None
    reason: str


def check_action(action_key: str) -> GateCheckResult:
    """Return GateCheckResult for *action_key*. Reads gates from YAML.

    Matching logic: the normalised action_key is compared against gate
    trigger strings (case-insensitive substring match). Gates that have
    ``requires_human_approval: true`` are checked first; free-action gates
    (``requires_human_approval: false``) serve as explicit allow-list entries.
    """
    gates: dict = load_approval_gates().get("gates", {})

    normalised = action_key.lower().replace("-", "_").replace(" ", "_")

    # First pass: check restricted gates (requires_human_approval: true)
    for gate_id, gate in gates.items():
        if not gate.get("requires_human_approval", False):
            continue
        triggers: list[str] = gate.get("triggers", [gate_id])
        if not triggers:
            triggers = [gate_id]
        if any(normalised in t.lower().replace("-", "_").replace(" ", "_") for t in triggers):
            return GateCheckResult(
                action=action_key,
                requires_approval=True,
                gate_id=gate.get("id", gate_id),
                reason=gate.get("reason", "Human approval required"),
            )

    # Second pass: exact gate_id match (handles gate keys like "send_first_email")
    for gate_id, gate in gates.items():
        key_normalised = gate_id.lower().replace("-", "_")
        if normalised == key_normalised:
            requires = gate.get("requires_human_approval", False)
            if requires:
                return GateCheckResult(
                    action=action_key,
                    requires_approval=True,
                    gate_id=gate.get("id", gate_id),
                    reason=gate.get("reason", "Human approval required"),
                )
            else:
                return GateCheckResult(
                    action=action_key,
                    requires_approval=False,
                    gate_id=gate.get("id", gate_id),
                    reason=gate.get("reason", "Action is permitted without approval"),
                )

    return GateCheckResult(
        action=action_key,
        requires_approval=False,
        gate_id=None,
        reason="Action is permitted without approval",
    )
