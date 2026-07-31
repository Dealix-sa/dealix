"""Contract for the approved public Dealix commercial path."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "landing" / "pricing.html"


class _VisibleTextParser(HTMLParser):
    """Collect browser-visible text while ignoring script and style content."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._suppressed = 0
        self.parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del attrs
        if tag.casefold() in {"script", "style"}:
            self._suppressed += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in {"script", "style"} and self._suppressed:
            self._suppressed -= 1

    def handle_data(self, data: str) -> None:
        if not self._suppressed:
            self.parts.append(data)


def _visible_text() -> str:
    parser = _VisibleTextParser()
    parser.feed(PRICING.read_text(encoding="utf-8"))
    parser.close()
    return " ".join(parser.parts)


def test_public_pricing_exposes_only_the_approved_launch_motion() -> None:
    visible = _visible_text()
    required = (
        "التشخيص المجاني المختصر",
        "تجربة مركز قيادة الإيرادات",
        "30 يومًا",
        "عرض مخصص",
        "لا يوجد سعر عام ثابت للـPilot",
    )
    missing = [value for value in required if value not in visible]
    assert not missing, f"missing approved public offer boundary: {missing}"


def test_public_pricing_has_no_checkout_or_retired_fixed_price_ladder() -> None:
    html = PRICING.read_text(encoding="utf-8")
    forbidden = (
        "/checkout.html",
        "tier=sprint",
        "tier=data_pack",
        "tier=growth",
        "tier=scale",
        "tier=partner",
        "Revenue Proof Sprint",
        "Data Pack",
        "Growth OS",
        "Scale OS",
        "Executive Command Center",
        "12,000",
        "7,999",
        "2,999",
        ">499<",
        ">1,500<",
    )
    leaked = [value for value in forbidden if value in html]
    assert not leaked, f"retired or internal offer leaked publicly: {leaked}"


def test_public_pricing_keeps_outbound_and_outcome_boundaries_visible() -> None:
    visible = _visible_text()
    required = (
        "لا نعد بعدد مبيعات أو إيراد أو نسبة نمو مضمونة",
        "الإرسال الحي غير مفعّل افتراضيًا",
        "يحتاج الموافقة المطلوبة",
        "تُقاس مقابل خط أساس",
        "ليست عروضًا عامة قابلة للشراء",
    )
    missing = [value for value in required if value not in visible]
    assert not missing, f"missing safety or evidence boundary: {missing}"


def test_public_pricing_uses_diagnostic_as_the_only_entry_cta() -> None:
    html = PRICING.read_text(encoding="utf-8")
    assert html.count('href="/diagnostic.html"') == 2
    assert "دون بطاقة أو دفع" in html
    assert "عرض موثق قبل البدء" in html
