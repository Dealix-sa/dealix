"""Shared helpers for V5 commercial tests (no network, no external sends)."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
_CHAIN_DONE = False


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(ROOT / "scripts" / script), *args],
                          cwd=ROOT, capture_output=True, text=True)


def ensure_chain() -> Path:
    """Generate the daily commercial artifacts once per test session."""
    global _CHAIN_DONE
    if not _CHAIN_DONE:
        assert run("commercial_generate_400_drafts.py", "--target", "400").returncode == 0
        assert run("commercial_score_drafts.py").returncode == 0
        assert run("commercial_safety_audit.py").returncode == 0
        assert run("commercial_founder_review_report.py").returncode == 0
        _CHAIN_DONE = True
    import datetime as dt
    return ROOT / "outputs" / "commercial_launch" / dt.date.today().isoformat()


def load_drafts() -> list[dict]:
    d = ensure_chain()
    return [json.loads(l) for l in (d / "draft_queue.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
