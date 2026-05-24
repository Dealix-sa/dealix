#!/usr/bin/env python3
"""Verify Policy-as-Code: policies/dealix_control_policy.yaml is well-formed
and lists all 11 non-negotiables with required fields."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, report  # noqa: E402

LAYER = "Policy-as-Code"
REQUIRED_NN = [f"NN{i}_" for i in range(1, 12)]
REQUIRED_TOP_KEYS = ("non_negotiables", "approval_thresholds", "critical_actions",
                     "proof_pack", "bilingual_disclaimer", "audit")


def main() -> None:
    reasons: list[str] = []
    path = REPO_ROOT / "policies" / "dealix_control_policy.yaml"
    if not path.exists():
        report(LAYER, False, ["missing: policies/dealix_control_policy.yaml"])

    text = path.read_text(encoding="utf-8")
    for k in REQUIRED_TOP_KEYS:
        if f"{k}:" not in text:
            reasons.append(f"missing top key: {k}")
    for nn in REQUIRED_NN:
        if nn not in text:
            reasons.append(f"missing non-negotiable id token: {nn}")

    # PyYAML check (best-effort)
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            reasons.append("yaml root must be a mapping")
        else:
            nns = data.get("non_negotiables") or []
            if len(nns) < 11:
                reasons.append(f"non_negotiables count {len(nns)} < 11")
            for entry in nns:
                for f in ("id", "description", "severity"):
                    if f not in entry:
                        reasons.append(f"non-negotiable missing field: {f}")
                        break
    except ImportError:
        pass  # yaml not installed in some CI shards; token check still valid
    except Exception as exc:  # noqa: BLE001
        reasons.append(f"yaml parse error: {exc!s}")

    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
