#!/usr/bin/env python3
"""Generate a monthly Board Packet (draft, for founder review).

Writes outputs/board_packets/YYYY-MM/BOARD_PACKET.md with all mandatory
sections. Figures are placeholders/assumptions to be filled by the founder —
this script never fabricates traction and never sends anything externally.

Run: python scripts/board_packet_generate.py [--month YYYY-MM]
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

NON_NEGOTIABLE = (
    "AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. "
    "المؤسس يراجع ويعتمد ويوقّع. النظام لا يرسل خارجيًا أبدًا."
)

SECTIONS = [
    ("Executive Summary — الملخّص التنفيذي", ["[ملخّص الشهر — يكمله المؤسس]"]),
    (
        "Revenue Activity — نشاط الإيراد",
        ["[نشاط إيراد فعلي — assumption حتى التأكيد. لا أرقام مختلقة.]"],
    ),
    (
        "Pipeline Quality — جودة خط الأنابيب",
        ["[عدد الفرص المؤهَّلة، المرحلة، القيمة المقدّرة (assumption)]"],
    ),
    ("Delivery Status — حالة التسليم", ["[التسليمات الجارية، نسبة القبول، المخاطر]"]),
    ("Product Progress — تقدّم المنتج", ["[modules/templates مضافة، productization]"]),
    ("Site / Media Progress — الموقع والمحتوى", ["[محتوى منشور يدويًا باعتماد، حالة الموقع]"]),
    ("Risks — المخاطر", ["[أهم المخاطر المفتوحة + المعالجة]"]),
    ("Cash Assumptions — افتراضات النقد", ["[افتراضات نقدية — موسومة assumption صراحةً]"]),
    ("Hiring Triggers — محفّزات التوظيف", ["[هل تجاوز pipeline الطاقة؟ هل يبرّر التكرار دورًا؟]"]),
    ("Decisions Required — القرارات المطلوبة", ["[قرارات هذا الشهر بترتيب الأولوية]"]),
    (
        "Evidence Links — روابط البرهان",
        [
            "outputs/v10_verification/V10_MASTER_VERIFICATION.md",
            "outputs/ceo_cockpit/latest/CEO_COCKPIT.md",
            "outputs/profitability/PROFITABILITY_SUMMARY.md",
            "outputs/moat_metrics/MOAT_METRICS_SUMMARY.md",
        ],
    ),
]

NO_FAKE_TRACTION = (
    "سياسة لا traction مزيّفة: كل رقم في هذه الحزمة إمّا مدعوم بـ evidence "
    "أو موسوم صراحةً كافتراض (assumption). لا أرقام نتائج بدون مصدر."
)


def build_packet(month: str) -> str:
    lines = [f"# Board Packet — {month} (Draft for Founder Review)", ""]
    lines += [f"> {NON_NEGOTIABLE}", "", f"> {NO_FAKE_TRACTION}", ""]
    for title, bullets in SECTIONS:
        lines.append(f"## {title}")
        lines.append("")
        for b in bullets:
            lines.append(f"- {b}")
        lines.append("")
    lines += [
        "## No Fake Traction Policy — سياسة عدم تضخيم النتائج",
        "",
        f"- {NO_FAKE_TRACTION}",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--month", default=date.today().strftime("%Y-%m"))
    p.add_argument("--out-root", type=Path, default=REPO / "outputs" / "board_packets")
    args = p.parse_args(argv)

    out_dir = args.out_root / args.month
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "BOARD_PACKET.md"
    out.write_text(build_packet(args.month), encoding="utf-8")
    print(f"board_packet_generate: wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
