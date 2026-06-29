#!/usr/bin/env python3
"""Dealix one-command daily activation — make the company operate today.

``make activate`` → this script. It chains the EXISTING founder tooling into a
single offline run (no secrets, no DB, no network) and writes one human index:
``data/founder_briefs/ACTIVATION_{date}.md`` linking everything the founder
needs this morning:

  1. Founder daily brief        (dealix_founder_daily_brief.py)
  2. Prioritized real leads     (Saudi Lead Graph → dealix_daily_lead_prep)
  3. Per-lead call sheet         (who to contact + what to say + which offer)
  4. Warm-list drafts            (warm_list_outreach.py — if a warm list exists)
  5. War-room touch drafts       (generate_war_room_touch_drafts.py)
  6. Daily scorecard             (founder_daily_scorecard.py)
  7. A rendered proposal          (render_diagnostic_proposal.py, top lead)
  8. The ACTIVATION index         (this script)

This is GLUE ONLY — every step reuses an existing script. Each step is wrapped
so one failure degrades gracefully and never crashes the run (mirrors
``scripts/run_dealix_daily_ops.py``).

Leads are surfaced by the founder-curated ``fit_score`` (the best "who to
contact for revenue" signal); the daily-prep engine then adds the bilingual
"why now", governance gating, and ``action_mode`` for each one.

Doctrine (Article 4 — IMMUTABLE)
--------------------------------
- DRAFT-ONLY: nothing here sends, charges, scrapes, or auto-contacts anyone.
- The call sheet PREPARES outreach (channel + angle + offer) for the founder to
  review and send MANUALLY. Approval is always human.
- Outputs live under ``data/founder_briefs/`` and ``data/wave12/`` — both
  gitignored — so no lead names or PII are ever committed.

Usage:
    make activate
    python3 scripts/dealix_activate_day.py [--date YYYY-MM-DD] [--top-n 15]
        [--candidates <csv>]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import UTC, date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
for _p in (str(Path(__file__).resolve().parent), str(REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dealix_daily_lead_prep import (  # noqa: E402
    DailyLeadBoard,
    DailyLeadEntry,
    run_daily_prep,
    write_board,
)
from dealix_lead_graph_adapter import DEFAULT_LEAD_GRAPH, load_lead_graph_candidates  # noqa: E402

DEFAULT_BRIEFS_DIR = REPO_ROOT / "data" / "founder_briefs"
DEFAULT_LEAD_DIR = REPO_ROOT / "data" / "wave12" / "daily_lead_prep"


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────


def _fit_score(rich_map: dict[str, dict[str, str]], name: str) -> int:
    raw = (rich_map.get(name, {}).get("fit_score") or "").strip()
    return int(raw) if raw.isdigit() else 0


def _by_fit(
    entries: tuple[DailyLeadEntry, ...], rich_map: dict[str, dict[str, str]]
) -> list[DailyLeadEntry]:
    """Order scored entries by the founder-curated fit_score (desc), stable."""
    return sorted(entries, key=lambda e: _fit_score(rich_map, e.candidate.name), reverse=True)


def _run_script(rel_script: str, args: list[str]) -> int:
    """Run an existing script offline; return its exit code (or 9x if missing/broken)."""
    script = REPO_ROOT / rel_script
    if not script.is_file():
        print(f"  skip: {rel_script} not found")
        return 99
    try:
        proc = subprocess.run(
            [sys.executable, str(script), *args],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
        )
        tail = (proc.stdout or proc.stderr or "").strip().splitlines()
        if tail:
            print(f"  {rel_script}: {tail[-1][:160]}")
        return proc.returncode
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"  {rel_script}: SKIP ({exc})")
        return 98


# ─────────────────────────────────────────────────────────────────────
# Call sheet (pure) — who to contact + what to say
# ─────────────────────────────────────────────────────────────────────


def build_call_sheet(
    board: DailyLeadBoard,
    rich_map: dict[str, dict[str, str]],
    *,
    total_candidates: int | None = None,
) -> str:
    """Render today's prepare-only outreach call sheet (DRAFT-ONLY)."""
    total = total_candidates if total_candidates is not None else board.candidates_count
    lines: list[str] = []
    lines.append(f"# Dealix — Call Sheet · لوحة التواصل — {board.on_date}")
    lines.append("")
    lines.append(
        "> ⚠️ **DRAFT-ONLY / مسودة فقط.** هذه اللوحة تُجهّز التواصل فقط — "
        "**لا إرسال ولا اتصال تلقائي**. المؤسس يراجع ويرسل/يتصل يدوياً بعد الموافقة."
    )
    lines.append("")
    lines.append(
        f"**اليوم / Today:** أقوى {board.leads_returned} جهة من {total} في Lead Graph "
        f"(مرتّبة حسب fit_score). الموسم: {board.season_context.get('season', '—')}."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    if not board.top_leads:
        lines.append("_لا توجد جهات اليوم — أضف leads عبر CSV._")
        return "\n".join(lines)

    for rank, e in enumerate(_by_fit(board.top_leads, rich_map), start=1):
        r = rich_map.get(e.candidate.name, {})
        channel = r.get("suggested_channel") or "—"
        angle = r.get("first_message_angle") or "—"
        offer = r.get("offer_recommended") or "—"
        objection = r.get("objection_prediction") or "—"
        opp = r.get("opportunity_type") or "—"
        fit = r.get("fit_score") or "—"
        intent = r.get("intent_score") or "—"
        lines.append(f"## {rank}. {e.candidate.name} — `{e.priority}` · `{e.action_mode}`")
        lines.append("")
        lines.append(f"- **الملاءمة / Fit:** {fit}  ·  **النية / Intent:** {intent}")
        lines.append(
            f"- **القطاع / Sector:** {e.candidate.sector or '—'}  ·  **Web:** {e.candidate.domain or '—'}"
        )
        lines.append(f"- **صاحب القرار / Decision role:** {e.candidate.contact_title or '—'}")
        lines.append(f"- **نوع الفرصة / Opportunity:** {opp}")
        lines.append(f"- **القناة المقترحة / Channel:** `{channel}`  (يدوي / manual)")
        lines.append(f"- **زاوية الرسالة الأولى / First-message angle (AR):** {angle}")
        lines.append(f"- **العرض المقترح / Recommended offer:** {offer}")
        lines.append(f"- **الاعتراض المتوقع / Likely objection:** {objection}")
        lines.append(f"- **ليش الآن / Why now:** {e.why_now_ar}")
        lines.append(f"- **الإجراء / Action:** {e.recommended_action_ar}")
        if e.blockers:
            lines.append(f"- **⚠️ Blockers:** {', '.join(e.blockers)}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "_كل تواصل يبقى مسودة حتى موافقتك. لا واتساب بارد · لا أتمتة LinkedIn · "
        "لا scraping · لا إرسال خارجي بدون موافقة. (دستور Dealix — Article 4)_"
    )
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Activation index (the single front door)
# ─────────────────────────────────────────────────────────────────────


def _rel(target: Path, start: Path) -> str:
    try:
        return os.path.relpath(target, start)
    except ValueError:
        return target.name


def build_index(
    *,
    board: DailyLeadBoard,
    date_str: str,
    briefs_dir: Path,
    artifacts: list[dict[str, object]],
    rich_map: dict[str, dict[str, str]],
    total_candidates: int,
) -> str:
    """Render ACTIVATION_{date}.md — links every artifact + bring-up commands."""
    lines: list[str] = []
    lines.append(f"# 🟢 Dealix — تفعيل اليوم / Daily Activation — {date_str}")
    lines.append("")
    lines.append(f"_Generated: {datetime.now(UTC).isoformat()}_")
    lines.append("")
    lines.append(
        "> Dealix شركة تشتغل اليوم: بريف + عملاء حقيقيون + مسودات + عرض — "
        "كلها **مسودة بموافقتك**، بدون أي إرسال تلقائي."
    )
    lines.append("")
    lines.append(
        f"**العملاء المحتملون / Lead pool:** {total_candidates} شركة سعودية في Lead Graph · "
        f"معروض اليوم: أقوى {board.leads_returned} حسب fit_score."
    )
    lines.append("")
    lines.append("## 📦 حزمة اليوم / Today's pack")
    lines.append("")
    lines.append("| # | المُخرَج / Artifact | الحالة / Status | الملف / File |")
    lines.append("|---|---|---|---|")
    for i, a in enumerate(artifacts, start=1):
        label = str(a.get("label", ""))
        status = str(a.get("status", ""))
        path_obj = a.get("path")
        if isinstance(path_obj, Path):
            link = f"[`{_rel(path_obj, briefs_dir)}`]({_rel(path_obj, briefs_dir)})"
        else:
            link = "—"
        lines.append(f"| {i} | {label} | {status} | {link} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🎯 أقوى إجراء اليوم / Top action")
    lines.append("")
    lines.append(f"> {board.next_founder_action or '—'}")
    lines.append("")
    if board.top_leads:
        lines.append("## ☎️ من تتواصل معه اليوم / Contact today (top by fit)")
        lines.append("")
        for e in _by_fit(board.top_leads, rich_map)[:5]:
            fit = rich_map.get(e.candidate.name, {}).get("fit_score") or "—"
            lines.append(
                f"- **{e.candidate.name}** (fit {fit}) — `{e.priority}` · "
                f"{e.candidate.contact_title or '—'} · {e.recommended_action_ar}"
            )
        lines.append("")
        lines.append("→ التفاصيل الكاملة (القناة + زاوية الرسالة + العرض) في **Call sheet** أعلاه.")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🔒 ثوابت الحوكمة / Governance invariants (immutable)")
    lines.append("")
    for inv in board.article_4_invariants:
        lines.append(f"- ✅ `{inv}`")
    lines.append("")
    lines.append(
        "_لا إرسال · لا شحن · لا scraping · لا تواصل تلقائي. كل تواصل = مسودة + "
        "موافقة المؤسس. (DEALIX_CONSTITUTION — Article 4)_"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🚀 تشغيل الموقع والـ API / Bring up the site & API")
    lines.append("")
    lines.append("```bash")
    lines.append("# الموقع الأساسي (Next.js على Railway / dealix.me):")
    lines.append("cd frontend && npm install && npm run build && npm start")
    lines.append("# أو: ادفع على main لمسارات frontend/** ليطلق railway_deploy_frontend.yml")
    lines.append("")
    lines.append("# الموقع الثابت الاحتياطي (GitHub Pages): ادفع على landing/**")
    lines.append("")
    lines.append("# الـ API (لازم لعرض الـleads/المسودات حيّة + التشخيص):")
    lines.append("make run   # uvicorn api.main:app  → http://localhost:8000/docs")
    lines.append("```")
    lines.append("")
    lines.append("_Re-run anytime: `make activate`_")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────────────────────────────────


def run_activation(
    *,
    on_date: date | None = None,
    top_n: int = 15,
    candidates_path: Path = DEFAULT_LEAD_GRAPH,
    briefs_dir: Path = DEFAULT_BRIEFS_DIR,
    lead_out_dir: Path = DEFAULT_LEAD_DIR,
    run_subprocess_steps: bool = True,
) -> int:
    """Produce the full daily activation pack offline. Returns 0 (degrades)."""
    today = on_date or datetime.now(UTC).date()
    date_str = today.isoformat()
    briefs_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, object]] = []

    # 1) Founder daily brief
    print("== 1/8 Founder daily brief ==")
    brief_path = briefs_dir / f"brief_{date_str}.md"
    if run_subprocess_steps:
        rc = _run_script("scripts/dealix_founder_daily_brief.py", ["--out", str(brief_path)])
        artifacts.append(
            {
                "label": "بريف المؤسس / Founder brief",
                "path": brief_path if brief_path.is_file() else None,
                "status": "ok" if rc == 0 and brief_path.is_file() else "skipped (deps?)",
            }
        )
    else:
        artifacts.append(
            {"label": "بريف المؤسس / Founder brief", "path": None, "status": "skipped"}
        )

    # 2) Prioritized real leads (Saudi Lead Graph → daily prep), surfaced by fit_score
    print("== 2/8 Lead board (Saudi Lead Graph) ==")
    rich_map: dict[str, dict[str, str]] = {}
    total_candidates = 0
    board: DailyLeadBoard
    try:
        candidates, rich_map = load_lead_graph_candidates(candidates_path, exclude_held=True)
        total_candidates = len(candidates)
        # Surface the founder's strongest-fit leads first; the engine then scores them.
        candidates.sort(key=lambda c: _fit_score(rich_map, c.name), reverse=True)
        selected = candidates[: max(1, top_n)] if candidates else []
        board = run_daily_prep(candidates=selected, on_date=today, top_n=top_n)
        _, md_path = write_board(board, out_dir=lead_out_dir)
        print(f"  leads: {board.leads_returned} of {total_candidates} candidates")
        artifacts.append(
            {
                "label": f"بورد العملاء / Lead board (top {board.leads_returned} of {total_candidates})",
                "path": md_path,
                "status": "ok",
            }
        )
    except Exception as exc:
        print(f"  lead board FAILED: {exc}")
        board = run_daily_prep(candidates=[], on_date=today, top_n=top_n)
        artifacts.append({"label": "بورد العملاء / Lead board", "path": None, "status": "failed"})

    # 3) Per-lead call sheet (who to contact + what to say)
    print("== 3/8 Call sheet ==")
    call_sheet_path = briefs_dir / f"call_sheet_{date_str}.md"
    try:
        call_sheet_path.write_text(
            build_call_sheet(board, rich_map, total_candidates=total_candidates),
            encoding="utf-8",
        )
        artifacts.append(
            {"label": "لوحة التواصل / Call sheet", "path": call_sheet_path, "status": "ok"}
        )
    except OSError as exc:
        print(f"  call sheet FAILED: {exc}")
        artifacts.append({"label": "لوحة التواصل / Call sheet", "path": None, "status": "failed"})

    if run_subprocess_steps:
        # 4) Warm-list drafts (no-ops gracefully if no warm list)
        print("== 4/8 Warm-list drafts ==")
        rc = _run_script("scripts/warm_list_outreach.py", [])
        warm_path = REPO_ROOT / "data" / "outreach" / "warm_list_drafts.md"
        artifacts.append(
            {
                "label": "مسودات القائمة الدافئة / Warm-list drafts",
                "path": warm_path if warm_path.is_file() else None,
                "status": "ok" if rc == 0 else "no warm list (skipped)",
            }
        )

        # 5) War-room touch drafts (no-ops if store empty)
        print("== 5/8 War-room touch drafts ==")
        rc = _run_script("scripts/generate_war_room_touch_drafts.py", ["--top-n", "10"])
        artifacts.append(
            {
                "label": "مسودات War Room / War-room drafts",
                "path": None,
                "status": "ok" if rc == 0 else "empty store (skipped)",
            }
        )

        # 6) Daily scorecard (exit 1 = warnings, non-fatal)
        print("== 6/8 Daily scorecard ==")
        rc = _run_script("scripts/founder_daily_scorecard.py", ["--date", date_str])
        artifacts.append(
            {
                "label": "سكوركارد اليوم / Daily scorecard",
                "path": None,
                "status": "ok" if rc in (0, 1) else "skipped",
            }
        )

        # 7) Rendered proposal for the top-fit lead
        print("== 7/8 Proposal (top lead) ==")
        ordered = _by_fit(board.top_leads, rich_map)
        top_company = ordered[0].candidate.name if ordered else ""
        if top_company:
            rc = _run_script("scripts/render_diagnostic_proposal.py", ["--company", top_company])
            matches = sorted(briefs_dir.glob(f"proposal_*_{date_str}.md"))
            artifacts.append(
                {
                    "label": f"عرض جاهز / Proposal — {top_company}",
                    "path": matches[-1] if matches else None,
                    "status": "ok" if rc == 0 and matches else "skipped",
                }
            )
        else:
            artifacts.append(
                {"label": "عرض جاهز / Proposal", "path": None, "status": "skipped (no lead)"}
            )

    # 8) Activation index
    print("== 8/8 Activation index ==")
    index_path = briefs_dir / f"ACTIVATION_{date_str}.md"
    index_path.write_text(
        build_index(
            board=board,
            date_str=date_str,
            briefs_dir=briefs_dir,
            artifacts=artifacts,
            rich_map=rich_map,
            total_candidates=total_candidates,
        ),
        encoding="utf-8",
    )
    print(f"\n✅ WROTE {index_path}")
    print("DEALIX_ACTIVATION_VERDICT=READY")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--date", help="ISO date YYYY-MM-DD (default: today UTC)")
    p.add_argument("--top-n", type=int, default=15, help="Leads to surface (default: 15)")
    p.add_argument(
        "--candidates",
        type=Path,
        default=DEFAULT_LEAD_GRAPH,
        help="Lead Graph CSV (default: SAUDI_LEAD_GRAPH_MASTER.csv)",
    )
    args = p.parse_args()

    on_date: date | None = None
    if args.date:
        try:
            on_date = datetime.fromisoformat(args.date).date()
        except ValueError:
            print(f"ERROR: --date must be YYYY-MM-DD; got {args.date!r}", file=sys.stderr)
            return 2

    if not args.candidates.is_file():
        print(
            f"WARNING: candidates CSV not found ({args.candidates}); "
            "producing brief + empty board.",
            file=sys.stderr,
        )

    return run_activation(on_date=on_date, top_n=args.top_n, candidates_path=args.candidates)


if __name__ == "__main__":
    raise SystemExit(main())
