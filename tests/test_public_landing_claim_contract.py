"""Contract for evidence-safe copy on the canonical static landing page."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing" / "index.html"


class _VisibleTextParser(HTMLParser):
    """Collect browser-visible text without regex-parsing HTML."""

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
    parser.feed(LANDING.read_text(encoding="utf-8"))
    parser.close()
    return " ".join(parser.parts)


def test_public_landing_does_not_publish_unverified_benchmark_claims() -> None:
    visible = _visible_text()
    forbidden = (
        "خصومات بلا توثيق تُسرّب 5–15% من الهامش",
        "تجديدات مفوّتة بقيمة مئات الآلاف",
        "المندوب يُعطي 20–35% خصماً",
        "كل proposal تستغرق 2–4 ساعات",
        "كل مراجعة SAMA = أسابيع",
        "15 فريق يُرسل موافقاتهم",
        "20+ شريك استراتيجي",
        "الموزع الجديد يحتاج 2–3 أشهر",
        "6–10 مستويات موافقة",
        "3–5 مطورين × 12 شهراً = 1.5–3M",
        "سنتواصل خلال ٤ ساعات عمل",
        "نتائج حقيقية من محرك ذكاء اصطناعي",
        "طلب تجربة",
    )
    assert not [claim for claim in forbidden if claim in visible]


def test_public_landing_labels_measurement_and_approval_boundaries() -> None:
    visible = _visible_text()
    required = (
        "دون وعد مسبق بنتيجة زمنية",
        "تُقاس النسبة من بيانات الشركة",
        "نثبّت baseline في البايلوت",
        "لا إرسال أو التزام أو شحن بدون الموافقة المطلوبة",
        "الإرسال الحي غير مفعّل افتراضيًا",
        "ليس نتيجة متحققة أو وعد أداء",
        "لا نعطي وعدًا زمنيًا قبل هذا الفحص",
    )
    missing = [boundary for boundary in required if boundary not in visible]
    assert not missing, f"missing public claim boundary: {missing}"


def test_public_landing_makes_free_diagnostic_the_primary_entry() -> None:
    html = LANDING.read_text(encoding="utf-8")
    assert html.count('href="/diagnostic.html"') >= 9
    assert "ابدأ الفحص المجاني المبدئي" in html
    assert "بدون بطاقة أو دفع" in html
    assert "مراجعة بشرية قبل أي عرض مدفوع" in html


def test_public_landing_has_no_live_prospect_or_paid_shortcut() -> None:
    html = LANDING.read_text(encoding="utf-8")
    forbidden = (
        'id="demoForm"',
        'id="prospector-form"',
        'href="/start.html"',
        'href="/checkout',
    )
    assert not [fragment for fragment in forbidden if fragment in html]
