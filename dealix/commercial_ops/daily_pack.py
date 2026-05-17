"""Write founder daily pack index — links today's governed outputs."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.paths import (
    FOUNDER_BRIEFS_DIR,
    REPO_ROOT,
    WAR_ROOM_TODAY_JSON,
)


def write_daily_pack_index(
    *,
    date_str: str | None = None,
    digest_path: Path | None = None,
    out_dir: Path | None = None,
) -> Path:
    """Create data/founder_briefs/DAILY_PACK_{date}.md checklist for founder review."""
    day = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    d = out_dir or FOUNDER_BRIEFS_DIR
    d.mkdir(parents=True, exist_ok=True)
    brief = d / f"brief_{day}.md"
    commercial = digest_path or (d / f"commercial_{day}.md")
    war_room = WAR_ROOM_TODAY_JSON

    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            return str(p)

    lines = [
        f"# Founder Daily Pack · {day}",
        "",
        "راجع بالترتيب (لا إرسال خارجي بدون موافقة):",
        "",
        f"- [ ] موجز المؤسس: `{_rel(brief)}`"
        + (" _(موجود)_" if brief.is_file() else " _(شغّل run_founder_commercial_day)_"),
        f"- [ ] Commercial digest: `{_rel(commercial)}`"
        + (" _(موجود)_" if commercial.is_file() else " _(مفقود)_"),
        f"- [ ] War Room JSON: `{_rel(war_room)}`"
        + (" _(موجود)_" if war_room.is_file() else " _(مفقود)_"),
        "- [ ] سجّل صفاً في `docs/commercial/operations/evidence_events_tracker.csv`",
        "- [ ] راجع مسودة LinkedIn من digest أو `scripts/social_queue_today.py`",
        "- [ ] مركز الموافقات قبل Gmail/LinkedIn",
        "",
        "## CI (GitHub Secrets)",
        "",
        "| Secret | الغرض |",
        "|--------|--------|",
        "| `DEALIX_API_BASE` | revenue-machine يومي |",
        "| `DEALIX_API_KEY` | Bearer للـ API |",
        "| `DEALIX_ADMIN_API_KEY` | War Room + evidence sync (اختياري) |",
        "| `DEALIX_SYNC_EVIDENCE` | `1` لمزامنة CSV → API |",
        "",
        "## تغذية المرشحين",
        "",
        "```bash",
        "python scripts/seed_revenue_machine_candidates.py",
        "# أو: python scripts/import_gtm_revenue_seed.py --dry-run",
        "```",
        "",
        "_Governed autopilot — لا واتساب بارد._",
    ]
    path = d / f"DAILY_PACK_{day}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    _write_index_json(day, path, commercial, war_room, brief)
    return path


def _write_index_json(
    day: str,
    pack_md: Path,
    commercial: Path,
    war_room: Path,
    brief: Path,
) -> Path:
    """Machine-readable index for founder UI and CI artifacts."""
    d = pack_md.parent

    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            return str(p)

    payload = {
        "date": day,
        "pack_md": _rel(pack_md),
        "brief_md": _rel(brief),
        "commercial_md": _rel(commercial),
        "war_room_json": _rel(war_room) if war_room.is_file() else None,
        "brief_exists": brief.is_file(),
        "commercial_exists": commercial.is_file(),
        "war_room_exists": war_room.is_file(),
    }
    index_path = d / "index.json"
    index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index_path


def pack_status(date_str: str | None = None) -> dict[str, Any]:
    day = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    d = FOUNDER_BRIEFS_DIR
    return {
        "date": day,
        "brief_exists": (d / f"brief_{day}.md").is_file(),
        "commercial_exists": (d / f"commercial_{day}.md").is_file(),
        "war_room_exists": WAR_ROOM_TODAY_JSON.is_file(),
        "pack_index": str((d / f"DAILY_PACK_{day}.md").relative_to(REPO_ROOT)),
    }
