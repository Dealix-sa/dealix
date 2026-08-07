import dealix_revenue_machine


def test_s9_builds_ranked_accounts():
    payload = dealix_revenue_machine.build_payload()
    assert payload['summary']['accounts'] == 5
    assert payload['summary']['top_accounts'] == 3
    scores = [row['score'] for row in payload['ranked_accounts']]
    assert scores == sorted(scores, reverse=True)


def test_s9_has_sales_assets():
    payload = dealix_revenue_machine.build_payload()
    assert payload['summary']['offers'] == 3
    assert payload['summary']['followups'] == 15
    for row in payload['ranked_accounts']:
        assert len(row['discovery_script']) == 5
        assert len(row['followups']) == 3
        assert row['offer']['name']


def test_s9_is_review_first():
    payload = dealix_revenue_machine.build_payload()
    assert payload['summary']['live'] == 0
    assert payload['summary']['review_required'] == payload['summary']['accounts']
    assert dealix_revenue_machine.verify(payload) == []


def test_s9_uses_daily_console_context():
    payload = dealix_revenue_machine.build_payload()
    assert payload['summary']['daily_routes'] == 42
    assert payload['summary']['daily_approvals'] == 42
