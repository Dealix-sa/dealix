"""Policy adapter for the Founder Console.

Loads policies/dealix_control_policy.yaml and exposes helpers to:
  - check if a string contains a forbidden claim,
  - enforce that external action requests are queued for approval,
  - emit policy-violation audit records.
"""
from __future__ import annotations

import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "policies" / "dealix_control_policy.yaml"


def _load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except ImportError:
        return _fallback_parse(path)
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _fallback_parse(path: Path) -> dict:
    # Tiny YAML-subset reader for environments without PyYAML.
    # Only extracts `forbidden_claims:` list of double-quoted strings.
    if not path.exists():
        return {}
    forbidden: list[str] = []
    in_list = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("forbidden_claims:"):
            in_list = True
            continue
        if in_list:
            if not line.startswith((" ", "\t")) and stripped:
                in_list = False
                continue
            if stripped.startswith("- "):
                value = stripped[2:].strip()
                if value.startswith('"') and value.endswith('"'):
                    forbidden.append(value[1:-1])
    return {"forbidden_claims": forbidden}


def forbidden_claims() -> list[str]:
    return list(_load_yaml(POLICY_PATH).get("forbidden_claims") or [])


def contains_forbidden_claim(text: str) -> list[str]:
    lower = text.lower()
    return [phrase for phrase in forbidden_claims() if phrase.lower() in lower]


def audit_record(actor: str, action_id: str, reason: str, decision: str) -> dict:
    return {
        "actor": actor,
        "action_id": action_id,
        "reason": reason,
        "decision": decision,
        "recorded_at": datetime.datetime.utcnow().isoformat(timespec="seconds"),
    }
