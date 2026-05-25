from __future__ import annotations

"""Read and write the current stage marker file.

Stage state lives in `<private_ops>/stage/current_stage.md` with a YAML
frontmatter block. We do not depend on PyYAML; we parse the small subset of
frontmatter we own (`key: value` lines).
"""

from datetime import date
from pathlib import Path
from typing import Any

CURRENT_STAGE_RELPATH = "stage/current_stage.md"

_DEFAULT_STAGE: dict[str, Any] = {
    "stage": 0,
    "started_at": "",
    "target_exit_date": "",
    "status": "not_started",
    "note": "private ops directory not initialised; defaulting to Stage 0",
}


def _parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse a `---` delimited YAML-ish frontmatter block.

    Only supports flat `key: value` lines — enough for stage state.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, Any] = {}
    for raw in lines[1:]:
        if raw.strip() == "---":
            break
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key.isidentifier() or key.replace("_", "").isalnum():
            out[key] = _coerce(value)
    return out


def _coerce(value: str) -> Any:
    if value == "":
        return ""
    if value.isdigit():
        return int(value)
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    return value


def _emit_frontmatter(data: dict[str, Any]) -> str:
    body = ["---"]
    for k, v in data.items():
        if isinstance(v, bool):
            body.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            body.append(f"{k}: {v}")
        else:
            body.append(f'{k}: "{v}"')
    body.append("---")
    body.append("")
    return "\n".join(body)


def read_current_stage(private_ops_path: Path) -> dict[str, Any]:
    """Return current stage data; falls back to Stage 0 if missing."""
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / CURRENT_STAGE_RELPATH
    if not target.exists():
        return dict(_DEFAULT_STAGE)
    try:
        text = target.read_text(encoding="utf-8")
    except OSError:
        return dict(_DEFAULT_STAGE)
    parsed = _parse_frontmatter(text)
    if not parsed:
        return dict(_DEFAULT_STAGE)
    return {
        "stage": parsed.get("stage", 0),
        "started_at": parsed.get("started_at", ""),
        "target_exit_date": parsed.get("target_exit_date", ""),
        "status": parsed.get("status", "in_progress"),
    }


def write_current_stage(private_ops_path: Path, stage_data: dict[str, Any]) -> None:
    """Write the stage marker file, creating parent dirs as needed."""
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / CURRENT_STAGE_RELPATH
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "stage": stage_data.get("stage", 0),
        "started_at": stage_data.get("started_at", date.today().isoformat()),
        "target_exit_date": stage_data.get("target_exit_date", ""),
        "status": stage_data.get("status", "in_progress"),
    }
    body = _emit_frontmatter(payload)
    body += f"\n# Stage {payload['stage']}\n\nStatus: {payload['status']}\n"
    target.write_text(body, encoding="utf-8")
