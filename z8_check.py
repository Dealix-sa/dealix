import dealix_daily_os


def test_z8_builds_daily_console():
    payload = dealix_daily_os.build_console()
    assert payload['summary']['memory_decisions'] == 7
    assert payload['summary']['routes'] == 42
    assert payload['summary']['channels'] == 6
    assert payload['summary']['offers'] == 3
    assert payload['summary']['target_sectors'] == 4


def test_z8_is_sales_ready_but_review_first():
    payload = dealix_daily_os.build_console()
    assert payload['summary']['live'] == 0
    assert payload['summary']['approvals_pending'] == 42
    assert dealix_daily_os.verify(payload) == []


def test_z8_has_commercial_motion():
    payload = dealix_daily_os.build_console()
    assert len(payload['commercial_offers']) == 3
    assert len(payload['target_sectors']) == 4
    assert len(payload['next_sales_actions']) >= 5
    assert payload['route_counts']['crm_task'] == 7
    assert payload['route_counts']['whatsapp_draft'] == 7
