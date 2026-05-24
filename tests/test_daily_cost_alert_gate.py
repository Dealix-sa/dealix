from auto_client_acquisition.observability.daily_cost_alert import evaluate_daily_cost_alert


def test_cost_alert_ok_under_threshold():
    out = evaluate_daily_cost_alert(daily_spend_usd=5.0)
    assert out["status"] == "ok"


def test_cost_alert_triggered():
    out = evaluate_daily_cost_alert(daily_spend_usd=50.0)
    assert out["status"] == "triggered"
