"""Shared helpers for Commercial Growth OS step scripts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DATA_DIR = REPO_ROOT / "data" / "commercial"
REPORT_DIR = REPO_ROOT / "reports" / "commercial" / "growth_os"


def load_json(path, key=None, default=None):
    p = Path(path)
    if not p.exists():
        return default if default is not None else ([] if key else {})
    data = json.loads(p.read_text(encoding="utf-8"))
    if key and isinstance(data, dict):
        return data.get(key, default if default is not None else [])
    return data


def dump(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
