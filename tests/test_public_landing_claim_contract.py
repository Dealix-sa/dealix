"""Contract for evidence-safe copy on the canonical static landing page."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing" / "index.html"


def _visible_text() -> str:
    html = LANDING.read_text(encoding="utf-8")
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    return re.sub(r"<[^>]+>", " ", html)


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
