from app.billing.moyasar_stub import create_payment, is_live_payment_enabled


def test_live_payment_disabled():
    assert is_live_payment_enabled() is False


def test_payment_capture_raises():
    try:
        create_payment()
    except RuntimeError as exc:
        assert "disabled" in str(exc)
    else:
        raise AssertionError("payment capture must remain disabled")
