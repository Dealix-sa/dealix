from __future__ import annotations

"""Tiny markdown frontmatter helpers shared across ops_runtime writers."""

from pathlib import Path
from typing import Any


def write_markdown(path: Path, frontmatter: dict[str, Any], body: str) -> Path:
    """Write a Markdown file with YAML-ish frontmatter.

    Creates parent directories as needed. Returns the path written.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = ["---"]
    for k, v in frontmatter.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            # quote to keep things parser-friendly
            lines.append(f'{k}: "{v}"')
    lines.append("---")
    lines.append("")
    text = "\n".join(lines) + body
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")
    return path


def read_markdown_frontmatter(path: Path) -> dict[str, Any] | None:
    """Return the frontmatter dict, or None when absent / malformed."""
    path = Path(path)
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    out: dict[str, Any] = {}
    for raw in lines[1:]:
        if raw.strip() == "---":
            break
        if ":" not in raw:
            continue
        k, _, v = raw.partition(":")
        v = v.strip().strip('"').strip("'")
        out[k.strip()] = v
    return out
