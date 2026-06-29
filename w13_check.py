import founder_command


def test_w13_builds_founder_command():
    payload = founder_command.build_payload()
    assert payload['summary']['target_companies'] == 30
    assert payload['summary']['service_steps'] == 7
    assert payload['summary']['inputs'] == 4
    assert payload['summary']['outputs'] == 4


def test_w13_is_real_service_flow():
    payload = founder_command.build_payload()
    assert payload['command']['sell_to']
    assert payload['command']['offer']
    assert payload['command']['kpi']
    assert payload['command']['proof']
    assert len(payload['service']['steps']) == 7
    assert len(payload['first_10']) == 10


def test_w13_is_review_first():
    payload = founder_command.build_payload()
    assert payload['summary']['live'] == 0
    assert payload['command']['live'] == 0
    assert payload['command']['review'] is True
    assert founder_command.verify(payload) == []
