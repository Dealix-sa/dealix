"""Social content queue — today's draft post (no auto-publish)."""

from __future__ import annotations

import re
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.doctrine import SOAEN_CHECKLIST_AR
from dealix.commercial_ops.paths import SOCIAL_QUEUE_YAML

_LEGACY_BODY_START = re.compile(r"^(?P<indent>\s*)body_ar:\s*'(?P<value>.*)$")
_NEXT_FIELD = re.compile(r"^\s*(cta_ar|aeo_slug|status|week|day|pillar|title_ar):")


def _next_nonempty(lines: list[str], start: int) -> str:
    for line in lines[start:]:
        if line.strip():
            return line
    return ""


def _normalize_legacy_body_scalars(text: str) -> str:
    """Convert legacy single-quoted multiline ``body_ar`` values to block scalars.

    The historic queue contains valid content but some generated entries use an
    unterminated-looking single-quoted multiline style that PyYAML rejects. This
    conversion is deliberately narrow: only ``body_ar`` fields are changed and
    a closing quote is accepted only when the following non-empty line is a
    sibling queue field. Other YAML errors are allowed to fail normally.
    """

    lines = text.splitlines()
    output: list[str] = []
    index = 0

    while index < len(lines):
        match = _LEGACY_BODY_START.match(lines[index])
        if match is None:
            output.append(lines[index])
            index += 1
            continue

        indent = match.group("indent")
        content_lines = [match.group("value")]
        cursor = index + 1
        found_close = False

        while cursor < len(lines):
            candidate = lines[cursor]
            if candidate.rstrip().endswith("'"):
                next_line = _next_nonempty(lines, cursor + 1)
                if _NEXT_FIELD.match(next_line):
                    content_lines.append(candidate.rstrip()[:-1])
                    found_close = True
                    cursor += 1
                    break
            content_lines.append(candidate)
            cursor += 1

        if not found_close:
            output.append(lines[index])
            index += 1
            continue

        output.append(f"{indent}body_ar: |-")
        block_indent = indent + "  "
        for content_line in content_lines:
            stripped = content_line.strip()
            output.append(f"{block_indent}{stripped}" if stripped else "")
        index = cursor

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def load_social_queue(path: Path | None = None) -> dict[str, Any]:
    p = path or SOCIAL_QUEUE_YAML
    if not p.is_file():
        return {"posts": []}

    text = p.read_text(encoding="utf-8")
    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError as original_error:
        normalized = _normalize_legacy_body_scalars(text)
        if normalized == text:
            raise original_error
        loaded = yaml.safe_load(normalized)

    data = loaded or {"posts": []}
    if not isinstance(data, dict):
        raise ValueError("social content queue root must be a mapping")
    posts = data.get("posts") or []
    if not isinstance(posts, list):
        raise ValueError("social content queue posts must be a list")
    return data


def get_post_for_date(
    on_date: date | None = None,
    *,
    queue: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Pick post by anchor week + weekday (Sun=0 .. Sat=6)."""
    data = queue if queue is not None else load_social_queue()
    posts: list[dict[str, Any]] = list(data.get("posts") or [])
    if not posts:
        return None

    d = on_date or datetime.now(UTC).date()
    anchor_raw = (data.get("anchor_date") or "2026-05-17").strip()
    try:
        anchor = date.fromisoformat(anchor_raw[:10])
    except ValueError:
        anchor = date(2026, 5, 17)
    num_weeks = max(1, int(data.get("cycle_weeks") or 4))
    week_num = ((d - anchor).days // 7) % num_weeks + 1
    day_index = (d.weekday() + 1) % 7  # Sun=0

    for post in posts:
        if int(post.get("week", 0)) == week_num and int(post.get("day", -1)) == day_index:
            return {
                **post,
                "calendar_date": d.isoformat(),
                "soaen_checklist_ar": SOAEN_CHECKLIST_AR,
            }

    for post in posts:
        if (post.get("status") or "draft") == "draft":
            return {**post, "calendar_date": d.isoformat(), "soaen_checklist_ar": SOAEN_CHECKLIST_AR}
    return {**posts[0], "calendar_date": d.isoformat(), "soaen_checklist_ar": SOAEN_CHECKLIST_AR}


def format_linkedin_draft(post: dict[str, Any]) -> str:
    title = post.get("title_ar") or ""
    body = post.get("body_ar") or ""
    cta = post.get("cta_ar") or post.get("cta") or ""
    lines = [
        title,
        "",
        body,
        "",
        f"➡️ {cta}",
        "",
        "— Dealix · Post-Lead Revenue Ops (مسودة — راجع SOAEN قبل النشر)",
    ]
    return "\n".join(lines)


def mark_post_status(
    *,
    week: int,
    day: int,
    status: str,
    path: Path | None = None,
) -> dict[str, Any]:
    """Update queue YAML status (draft | approved | published). Does not publish externally."""
    allowed = {"draft", "approved", "published"}
    if status not in allowed:
        raise ValueError(f"status must be one of {allowed}")
    p = path or SOCIAL_QUEUE_YAML
    data = load_social_queue(p)
    posts: list[dict[str, Any]] = list(data.get("posts") or [])
    hit = False
    for post in posts:
        if int(post.get("week", 0)) == week and int(post.get("day", -1)) == day:
            post["status"] = status
            hit = True
            break
    if not hit:
        raise KeyError(f"no post for week={week} day={day}")
    data["posts"] = posts
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    return {"week": week, "day": day, "status": status, "updated": True}
