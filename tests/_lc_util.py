"""Shared helpers for launch-control tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def load_script(name: str) -> ModuleType:
    """Load a script module from scripts/<name>.py by file path."""
    path = REPO_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_lc_{name}", path)
    assert spec and spec.loader, f"cannot load {path}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ensure_run() -> None:
    """Generate a fresh commercial run + media calendar into canonical outputs."""
    from launch_os import paths
    from launch_os.drafts import generate_drafts, write_run
    from launch_os.safety import audit_queue
    from launch_os.readiness import readiness_report, daily_metrics
    from launch_os.media_social import generate_calendar, write_calendar
    import json

    paths.ensure_dirs()
    drafts = generate_drafts(target=400)
    summary = write_run(drafts, paths.COMMERCIAL_OUT, paths.COMMERCIAL_LATEST)
    run_dir = summary["run_dir"]
    queue = run_dir / "draft_queue.jsonl"

    safety = audit_queue(queue)
    for d in (run_dir, paths.COMMERCIAL_LATEST):
        (d / "safety_audit.json").write_text(json.dumps(safety, ensure_ascii=False, indent=2), encoding="utf-8")

    report = readiness_report(queue, target=400)
    for d in (run_dir, paths.COMMERCIAL_LATEST):
        (d / "daily_metrics.json").write_text(
            json.dumps(report["metrics"], ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (d / "readiness.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    write_calendar(generate_calendar(), paths.MEDIA_OUT)
