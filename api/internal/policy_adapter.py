"""
api.internal.policy_adapter — read-only merged policy view.

Reads policies/dealix_control_policy.yaml + the three canonical sources
it extends and returns a single envelope:

  {
    "data": {
      "invariants": [...],
      "approval_gates": {...},
      "claim_rules": {...},
      "forbidden_actions": [...]
    },
    "source": "api",
    "freshness": iso8601,
    "is_estimate": false
  }
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[2]
_WRAPPER = _REPO / "policies" / "dealix_control_policy.yaml"
_APPROVAL = _REPO / "dealix" / "config" / "approval_policy.yaml"
_CLAIM = _REPO / "dealix" / "config" / "claim_policy.yaml"
_GOV = _REPO / "auto_client_acquisition" / "governance_os" / "policies" / "default_registry.yaml"


def _safe_load(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError:
        return {"_error": "pyyaml_not_installed"}
    if not path.exists():
        return {"_error": "missing", "_path": str(path)}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"_error": "parse_error", "_detail": repr(exc), "_path": str(path)}


def merged_policy_view() -> dict[str, Any]:
    wrapper = _safe_load(_WRAPPER) or {}
    approval = _safe_load(_APPROVAL) or {}
    claim = _safe_load(_CLAIM) or {}
    gov = _safe_load(_GOV) or {}

    return {
        "data": {
            "invariants": list((wrapper.get("invariants") or {}).keys()),
            "approval_gates": approval,
            "claim_rules": claim.get("rules", {}),
            "forbidden_actions": gov.get("forbidden_customer_facing_actions", []),
            "wrapper_kind": wrapper.get("kind"),
            "wrapper_status": wrapper.get("status"),
            "private_ops_root": os.environ.get("PRIVATE_OPS")
                or os.environ.get("DEALIX_PRIVATE_OPS")
                or "/opt/dealix",
        },
        "source": "api",
        "freshness": datetime.now(timezone.utc).isoformat(),
        "is_estimate": False,
    }
