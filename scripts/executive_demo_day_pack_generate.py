#!/usr/bin/env python3
"""Generate an Executive Demo Day pack (drafts, for founder review).

Writes outputs/executive_demo_day/YYYY-MM-DD/ with the demo script, asset
checklist, executive follow-up draft, and conversion plan. No guaranteed ROI,
no fabricated proof. Never sends anything externally.

Run: python scripts/executive_demo_day_pack_generate.py
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

NON_NEGOTIABLE = (
    "AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. "
    "المؤسس يراجع ويعتمد ويرسل يدويًا. النظام لا يرسل خارجيًا أبدًا."
)
DRAFT = "DRAFT — review only. لا ROI مضمون. لا proof مختلق."


def _doc(title: str, sections: list[tuple[str, list[str]]]) -> str:
    lines = [f"# {title}", "", f"> {DRAFT}", "", f"> {NON_NEGOTIABLE}", ""]
    for h, bullets in sections:
        lines.append(f"## {h}")
        lines.append("")
        for b in bullets:
            lines.append(f"- {b}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_pack() -> dict[str, str]:
    return {
        "demo_day_script.md": _doc(
            "Demo Day Script",
            [
                ("الافتتاح", ["[المشكلة في جملة]"]),
                ("المنهج", ["كيف يعمل Dealix: AI يجهّز، المؤسس/العميل يعتمد."]),
                ("البرهان", ["حالة برهان معتمدة قابلة للمراجعة — لا أرقام بدون evidence."]),
                ("الخطوة التالية", ["pilot محدود بمعايير نجاح."]),
            ],
        ),
        "demo_assets_checklist.md": _doc(
            "Demo Assets Checklist",
            [
                ("الأصول", ["شرائح موجزة", "حالة برهان معتمدة", "عرض تنفيذي", "close plan"]),
                ("الجاهزية", ["[تحقق من توفر كل أصل قبل العرض]"]),
            ],
        ),
        "executive_followup.md": _doc(
            "Executive Follow-up (Draft)",
            [
                (
                    "المتابعة",
                    [
                        "رسالة متابعة draft — تُعتمد وتُرسل يدويًا من المؤسس.",
                        "تلخّص القيمة والخطوة التالية بدون وعود مضمونة.",
                    ],
                ),
            ],
        ),
        "conversion_plan.md": _doc(
            "Demo → Deal Conversion Plan",
            [
                (
                    "التحويل",
                    [
                        "خطوة تالية محددة بموعد ومالك.",
                        "ربط بـ close plan.",
                        "متابعة يعتمدها المؤسس.",
                    ],
                ),
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--out-root", type=Path, default=REPO / "outputs" / "executive_demo_day")
    args = p.parse_args(argv)

    out_dir = args.out_root / args.date
    out_dir.mkdir(parents=True, exist_ok=True)
    pack = build_pack()
    for fname, content in pack.items():
        (out_dir / fname).write_text(content, encoding="utf-8")
    print(f"executive_demo_day_pack_generate: wrote {len(pack)} drafts to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
