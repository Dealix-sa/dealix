#!/usr/bin/env python3
"""Render the 10-panel Dealix CEO master dashboard.

Calls the supporting CEO scripts (business score, finance snapshot,
stage) and reads optional private operating files. Pure stdlib.
Bilingual. Always exits 0 unless an internal error occurs.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
PRIVATE = REPO_ROOT / "dealix-ops-private"

PANEL_WIDTH = 72


def _run_json(script: Path) -> dict | None:
    """Run a sibling script with --json. Return parsed dict or None."""
    if not script.exists():
        return None
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        return None


def _read_first_lines(path: Path, n: int = 6) -> str:
    if not path.exists():
        return f"N/A — fill {path.relative_to(REPO_ROOT)}"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return f"N/A — unreadable {path.relative_to(REPO_ROOT)}"
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return f"N/A — empty {path.relative_to(REPO_ROOT)}"
    return "\n".join(lines[:n])


def _count_dir(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    return sum(
        1
        for p in path.iterdir()
        if p.is_file() and not p.name.startswith(".") and p.name != ".gitkeep"
    )


def panel(title_en: str, title_ar: str, body: str) -> str:
    header = f" {title_en} / {title_ar} ".center(PANEL_WIDTH, "─")
    body_lines = body.splitlines() if body else ["(no data)"]
    rendered = "\n".join(f"  {ln}" for ln in body_lines)
    footer = "─" * PANEL_WIDTH
    return f"{header}\n{rendered}\n{footer}"


def panel_founder_focus() -> str:
    body = _read_first_lines(PRIVATE / "founder" / "ceo_command.md")
    return panel("Founder Focus", "تركيز المؤسس", body)


def panel_revenue_score(score: dict | None) -> str:
    if not score:
        body = "N/A — run scripts/ceo_business_score.py"
    else:
        overall = score.get("overall")
        head = f"Overall / الإجمالي: {overall if overall is not None else 'N/A'}/100"
        rows = []
        for d in score.get("dimensions", []):
            s = d.get("score")
            rows.append(
                f"  {d.get('dimension_en'):<18} {'N/A' if s is None else f'{s}/100'}"
            )
        body = head + "\n" + "\n".join(rows)
    return panel("Revenue Score", "درجة الإيراد", body)


def panel_pipeline(snap: dict | None) -> str:
    if not snap:
        body = "N/A — run scripts/ceo_finance_snapshot.py"
    else:
        pv = snap.get("pipeline_weighted")
        body = f"Weighted pipeline / الأنبوب المرجَّح: {pv}"
    return panel("Pipeline", "الأنبوب", body)


def panel_cash_mrr_runway(snap: dict | None) -> str:
    if not snap:
        body = "N/A — run scripts/ceo_finance_snapshot.py"
    else:
        body = (
            f"Cash total / إجمالي النقد   : {snap.get('cash_collected_total')}\n"
            f"Cash 30d   / نقد 30 يومًا  : {snap.get('cash_collected_30d')}\n"
            f"MRR        / إيراد متكرر   : {snap.get('mrr')}\n"
            f"Burn       / الحرق الشهري  : {snap.get('monthly_burn')}\n"
            f"Runway     / المهلة (شهور) : {snap.get('runway_months')}"
        )
    return panel("Cash / MRR / Runway", "النقد / الإيراد / المهلة", body)


def panel_delivery_readiness() -> str:
    count = _count_dir(PRIVATE / "delivery" / "qa")
    if count == 0 and not (PRIVATE / "delivery" / "qa").exists():
        body = "N/A — fill dealix-ops-private/delivery/qa/"
    else:
        body = f"QA artifacts on disk / مخرجات الجودة: {count}"
    return panel("Delivery Readiness", "جاهزية التسليم", body)


def panel_trust_risks() -> str:
    risk = PRIVATE / "founder" / "risk_log.md"
    if not risk.exists():
        body = f"N/A — fill {risk.relative_to(REPO_ROOT)}"
    else:
        try:
            text = risk.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        open_risks = sum(1 for ln in text.splitlines() if ln.strip().startswith("- ") and "open" in ln.lower())
        body = f"Open risks / المخاطر المفتوحة: {open_risks}"
    return panel("Trust Risks", "مخاطر الثقة", body)


def panel_stage(stage: dict | None) -> str:
    if not stage:
        body = "N/A — run scripts/ceo_stage.py"
    else:
        body = (
            f"Stage / المرحلة : {stage.get('stage_number')} — "
            f"{stage.get('name_en')} / {stage.get('name_ar')}\n"
            f"Window / النافذة : {stage.get('window')}\n"
            f"Next / التالي    : {stage.get('next_action_en')}"
        )
    return panel("Stage Readiness", "جاهزية المرحلة", body)


def panel_learning_decision() -> str:
    body = _read_first_lines(PRIVATE / "learning" / "experiment_log.md", n=5)
    return panel("Learning Decision", "قرار التعلم", body)


def panel_productization() -> str:
    body = _read_first_lines(PRIVATE / "learning" / "productization_candidates.md", n=5)
    return panel("Productization Candidates", "مرشحات التحويل لمنتج", body)


def panel_kill_defer() -> str:
    body = _read_first_lines(REPO_ROOT / "docs" / "founder" / "KILL_LIST.md", n=6)
    return panel("Kill / Defer List", "قائمة الإيقاف / التأجيل", body)


def render() -> str:
    score = _run_json(SCRIPTS / "ceo_business_score.py")
    snap = _run_json(SCRIPTS / "ceo_finance_snapshot.py")
    stage = _run_json(SCRIPTS / "ceo_stage.py")

    panels = [
        panel_founder_focus(),
        panel_revenue_score(score),
        panel_pipeline(snap),
        panel_cash_mrr_runway(snap),
        panel_delivery_readiness(),
        panel_trust_risks(),
        panel_stage(stage),
        panel_learning_decision(),
        panel_productization(),
        panel_kill_defer(),
    ]
    header = "Dealix CEO Master Dashboard / لوحة قيادة المؤسس الرئيسية"
    return header + "\n" + "=" * PANEL_WIDTH + "\n" + "\n".join(panels)


def main(argv: list[str] | None = None) -> int:
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main())
