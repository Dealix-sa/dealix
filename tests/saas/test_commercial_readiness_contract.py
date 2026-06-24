from app.commercial.readiness import build_founder_led_readiness_report


def test_founder_led_readiness_report_is_ready():
    report = build_founder_led_readiness_report()
    assert report.is_ready is True
    assert report.verdict == "READY_FOR_FOUNDER_LED_COMMERCIAL_LAUNCH"


def test_founder_led_readiness_report_mentions_review_first_safety():
    report = build_founder_led_readiness_report()
    notes = " ".join(gate.note for gate in report.gates)
    assert "review-first" in notes
