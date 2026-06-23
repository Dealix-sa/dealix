#!/usr/bin/env python3
"""Dealix Outreach Kit — generate ready-to-send bilingual emails from a real target list.

Doctrine-safe by design:
  * Never sends anything. It only writes ready-to-paste drafts to reports/outreach/<date>/.
  * Never invents companies or email addresses. It reads a CSV that the founder fills
    with REAL targets (data/outreach/saudi_target_intake.csv).
  * Pains are framed as hypotheses/questions, never as fabricated facts about a company.

Usage:
    # 1) copy the template and fill it with real companies you know/researched:
    cp data/outreach/saudi_target_intake.template.csv data/outreach/saudi_target_intake.csv
    #    (edit it, then:)
    python3 scripts/dealix_outreach_kit.py
    python3 scripts/dealix_outreach_kit.py --intake data/outreach/saudi_target_intake.csv --top 15
    python3 scripts/dealix_outreach_kit.py --dry-run

Output:
    reports/outreach/<YYYY-MM-DD>/<priority>-<company>.md   (one ready email per target)
    reports/outreach/<YYYY-MM-DD>/_DIGEST.md                (founder review digest)
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PITCHES_PATH = REPO_ROOT / "data" / "outreach" / "sector_pitches.json"
DEFAULT_INTAKE = REPO_ROOT / "data" / "outreach" / "saudi_target_intake.csv"
TEMPLATE_INTAKE = REPO_ROOT / "data" / "outreach" / "saudi_target_intake.template.csv"
OUT_ROOT = REPO_ROOT / "reports" / "outreach"


def _slug(text: str) -> str:
    text = re.sub(r"\s+", "-", text.strip())
    return re.sub(r"[^0-9A-Za-z؀-ۿ_-]", "", text) or "target"


def load_pitches() -> dict:
    return json.loads(PITCHES_PATH.read_text(encoding="utf-8"))


def read_targets(intake: Path) -> list[dict]:
    rows: list[dict] = []
    with intake.open(encoding="utf-8") as fh:
        reader = csv.DictReader(r for r in fh if not r.lstrip().startswith("#"))
        for row in reader:
            row = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
            if not row.get("company") or not row.get("sector"):
                continue
            rows.append(row)
    return rows


def render_email(target: dict, pitches: dict, stage: str = "intro") -> tuple[str, str]:
    company = target["company"]
    sector = target["sector"]
    lang = (target.get("language") or "both").lower()
    sec = pitches["sectors"].get(sector)
    co = pitches["company"]
    fu = pitches.get("followups", {})
    if not sec:
        raise ValueError(f"unknown sector '{sector}' for {company} (valid: {', '.join(pitches['sectors'])})")

    greeting_name = target.get("contact_name") or ""
    blocks: list[str] = []

    def sig_ar() -> list[str]:
        return [
            "",
            f"Dealix — {co['oneLiner_ar']}",
            f"تشخيص مجاني: {co['diagnostic']}  |  {co['site']}",
            "",
            "تحياتي،",
            "سامي — Dealix",
        ]

    def sig_en() -> list[str]:
        return [
            "",
            f"Dealix — {co['oneLiner_en']}",
            f"Free diagnostic: {co['diagnostic']}  |  {co['site']}",
            "",
            "Best,",
            "Sami — Dealix",
        ]

    def ar_block() -> str:
        hello = f"السلام عليكم {greeting_name}،".strip() if greeting_name else "السلام عليكم،"
        if stage == "f3":
            body_lines = [hello, "", fu.get("f3_ar", "")]
        elif stage == "f7":
            body_lines = [hello, "", fu.get("f7_ar", "")]
        else:
            body_lines = [hello, "", sec["pain_ar"], "", sec["fix_ar"], "", sec["cta_ar"]]
        return "\n".join(body_lines + sig_ar())

    def en_block() -> str:
        hello = f"Hi {greeting_name}," if greeting_name else "Hello,"
        if stage == "f3":
            body_lines = [hello, "", fu.get("f3_en", "")]
        elif stage == "f7":
            body_lines = [hello, "", fu.get("f7_en", "")]
        else:
            body_lines = [hello, "", sec["pain_en"], "", sec["fix_en"], "", sec["cta_en"]]
        return "\n".join(body_lines + sig_en())

    if lang in ("ar", "both"):
        blocks.append(ar_block())
    if lang in ("en", "both"):
        blocks.append(en_block())

    prefix = {"f3": "متابعة (يوم 3): ", "f7": "متابعة أخيرة (يوم 7): "}.get(stage, "")
    base_subject = sec["subject_ar"].format(company=company) if lang != "en" else sec["subject_en"].format(company=company)
    subject = prefix + base_subject
    body = ("\n\n— — —\n\n").join(blocks)
    return subject, body


def write_target_file(out_dir: Path, target: dict, subject: str, body: str, pitches: dict, stage: str = "intro") -> Path:
    prio = target.get("priority") or "3"
    suffix = {"f3": "-followup3", "f7": "-followup7"}.get(stage, "")
    fname = f"{prio}-{_slug(target['company'])}{suffix}.md"
    path = out_dir / fname
    to = target.get("contact_email") or "[ضع إيميل العميل الحقيقي هنا]"
    signal = target.get("signal_note") or "—"
    offer = pitches.get("recommended_offer", {}).get(target.get("sector"), {})
    offer_line = "—"
    if offer:
        offer_line = f"{offer.get('tier')} · setup {offer.get('setup'):,} SAR · monthly {offer.get('monthly'):,} SAR (لا تعرضه إلا بعد التشخيص)"
    content = "\n".join([
        f"# {target['company']} — {target.get('sector')}",
        "",
        f"**TO:** {to}",
        f"**SUBJECT:** {subject}",
        f"**CITY:** {target.get('city') or '—'}  ·  **PRIORITY:** {prio}  ·  **LANG:** {target.get('language') or 'both'}",
        f"**SIGNAL (سبب الاستهداف):** {signal}",
        f"**العرض الموصى به عند الاهتمام:** {offer_line}",
        "**STATUS:** draft_pending_human_review — راجع وأرسل يدويًا.",
        "",
        "---",
        "",
        body,
        "",
    ])
    path.write_text(content, encoding="utf-8")
    return path


def write_digest(out_dir: Path, targets: list[dict], pitches: dict) -> Path:
    today = date.today().isoformat()
    lines = [
        f"# Dealix · digest الاستهداف اليومي · {today}",
        "",
        f"عدد المستهدفين الجاهزين: **{len(targets)}**  ·  الحالة: كلها مسودات تنتظر مراجعتك.",
        "",
        "| # | الشركة | القطاع | المدينة | أولوية | إيميل |",
        "|---|--------|--------|---------|--------|-------|",
    ]
    for i, t in enumerate(sorted(targets, key=lambda r: r.get("priority") or "3"), 1):
        lines.append(
            f"| {i} | {t['company']} | {t.get('sector')} | {t.get('city') or '—'} "
            f"| {t.get('priority') or '3'} | {t.get('contact_email') or '—'} |"
        )
    lines += [
        "",
        "## الخطوة التالية",
        "1. افتح كل ملف في هذا المجلد، راجع النص، عدّل إذا تبي.",
        "2. تأكد من إيميل العميل (لا ترسل لإيميل غير مؤكد).",
        "3. أرسل من إيميلك يدويًا — Dealix لا يرسل تلقائيًا (سياسة مراجعة بشرية).",
        "",
        f"التشخيص المجاني: {pitches['company']['diagnostic']}",
    ]
    path = out_dir / "_DIGEST.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Dealix outreach kit — ready emails from a real target list")
    ap.add_argument("--intake", type=Path, default=DEFAULT_INTAKE)
    ap.add_argument("--top", type=int, default=0, help="Limit number of targets (0 = all)")
    ap.add_argument("--stage", choices=["intro", "f3", "f7"], default="intro",
                    help="intro = first email; f3 = day-3 follow-up; f7 = day-7 final nudge")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pitches = load_pitches()

    intake = args.intake
    if not intake.exists():
        print(f"لا يوجد ملف مستهدفين: {intake}")
        print(f"انسخ القالب واملأه بشركات حقيقية:\n  cp {TEMPLATE_INTAKE} {DEFAULT_INTAKE}")
        return 1

    targets = read_targets(intake)
    if args.top:
        targets = sorted(targets, key=lambda r: r.get("priority") or "3")[: args.top]
    if not targets:
        print(f"الملف فاضي أو ما فيه صفوف صالحة: {intake}")
        return 1

    if args.dry_run:
        print(f"[dry-run] {len(targets)} مستهدف سيُولّد لهم إيميلات:")
        for t in targets:
            print(f"  - {t['company']} ({t.get('sector')}) → {t.get('contact_email') or 'بدون إيميل'}")
        return 0

    out_dir = OUT_ROOT / date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    errors: list[str] = []
    for t in targets:
        try:
            subject, body = render_email(t, pitches, stage=args.stage)
            written.append(write_target_file(out_dir, t, subject, body, pitches, stage=args.stage))
        except Exception as exc:
            errors.append(f"{t.get('company')}: {exc}")

    digest = write_digest(out_dir, targets, pitches)
    print(f"تم إنشاء {len(written)} إيميل جاهز في: {out_dir}")
    print(f"digest المراجعة: {digest}")
    if errors:
        print("\nأخطاء:")
        for e in errors:
            print(f"  - {e}")
    print("\nكلها مسودات تنتظر مراجعتك. Dealix لا يرسل تلقائيًا.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
