"""Read-only views into the private_ops runtime.

Used by Founder Console endpoints to surface CSV/MD state without ever
mutating it. All paths are resolved under $DEALIX_PRIVATE_OPS; reads
outside that root are refused.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Any


def _private_ops_root() -> Path:
    root = os.environ.get("DEALIX_PRIVATE_OPS")
    if not root:
        raise RuntimeError("DEALIX_PRIVATE_OPS is not set")
    return Path(root).resolve()


def _safe_resolve(*parts: str) -> Path:
    root = _private_ops_root()
    p = (root.joinpath(*parts)).resolve()
    # path traversal guard — resolved path must stay under root
    if root not in p.parents and p != root:
        raise PermissionError("refused: path escapes DEALIX_PRIVATE_OPS root")
    return p


def read_csv(*parts: str) -> list[dict[str, str]]:
    p = _safe_resolve(*parts)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_markdown(*parts: str) -> str:
    p = _safe_resolve(*parts)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def list_ledgers(*parts: str) -> list[str]:
    p = _safe_resolve(*parts)
    if not p.exists():
        return []
    return sorted([x.name for x in p.iterdir() if x.is_file()])


def summary() -> dict[str, Any]:
    """Cheap "what's in the private ops runtime?" report for the Founder Console."""
    try:
        root = _private_ops_root()
    except RuntimeError as e:
        return {"ok": False, "error": str(e)}
    out: dict[str, Any] = {"ok": True, "root": str(root), "sections": {}}
    if not root.exists():
        out["ok"] = False
        out["error"] = "DEALIX_PRIVATE_OPS path does not exist"
        return out
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        out["sections"][sub.name] = sorted(x.name for x in sub.iterdir() if x.is_file())
    return out
