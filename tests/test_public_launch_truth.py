"""Public launch copy must distinguish bounded demos from production proof."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_homepage_has_no_unproved_speed_or_customer_result() -> None:
    html = (ROOT / "landing" / "index.html").read_text(encoding="utf-8")
    assert "٤٠٪ من leads" not in html
    assert "يرد خلال ٤٥ ثانية" not in html
    assert "سيناريو حقيقي" not in html
    assert "محادثة حقيقية" not in html
    assert "موظف مبيعات AI حقيقي" not in html

    # The current authority surface labels the example directly instead of
    # relying on an older Arabic scenario marker.
    assert "DEMO · SYNTHETIC" in html
    assert "مثال صناعي يوضح شكل القرار" in html
    assert "DEMO only · no live send · no customer activity" in html


def test_homepage_explains_live_execution_boundary() -> None:
    html = (ROOT / "landing" / "index.html").read_text(encoding="utf-8")
    assert "خدمات Live" not in html
    assert "لا تنفيذ خارجي من دون المسار والموافقة المناسبين" in html
    assert "المتغيرات البيئية لا تمنح سلطة إرسال عام" in html
    assert "لا fake proof" in html


def test_status_console_uses_code_ready_public_label() -> None:
    html = (ROOT / "landing" / "status.html").read_text(encoding="utf-8")
    js = (ROOT / "landing" / "assets" / "js" / "service-console.js").read_text(
        encoding="utf-8"
    )
    assert "جاهز للكود" in html
    assert "Code-ready" in js
    assert "does not mean every provider" in html
