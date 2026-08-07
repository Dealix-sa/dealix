"""Social content queue — today's draft post (no auto-publish)."""

from __future__ import annotations

import os
import tempfile
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.doctrine import SOAEN_CHECKLIST_AR
from dealix.commercial_ops.paths import SOCIAL_QUEUE_YAML


def load_social_queue(path: Path | None = None) -> dict[str, Any]:
    p = path or SOCIAL_QUEUE_YAML
    if not p.is_file():
        return {"posts": []}
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {"posts": []}
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


def _atomic_dump_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write YAML atomically so parallel readers never observe a partial file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = Path(handle.name)

        with temp_path.open(encoding="utf-8") as handle:
            validated = yaml.safe_load(handle)
        if not isinstance(validated, dict) or not isinstance(validated.get("posts"), list):
            raise ValueError("refusing to replace social queue with invalid YAML")

        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def mark_post_status(
    *,
    week: int,
    day: int,
    status: str,
    path: Path | None = None,
) -> dict[str, Any]:
    """Update queue status atomically. This never publishes externally."""
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
    _atomic_dump_yaml(p, data)
    return {"week": week, "day": day, "status": status, "updated": True}
