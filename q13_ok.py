import founder_daily_command


def test_q13():
    payload = founder_daily_command.build_payload()
    assert payload['summary']['target_companies'] == 30
    assert founder_daily_command.verify(payload) == []
