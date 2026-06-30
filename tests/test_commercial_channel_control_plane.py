from app.commercial.channel_control_plane import run_channel_control_plane


def test_channel_control_smoke():
    payload = run_channel_control_plane()
    assert payload['summary']['actions'] == 3
    assert payload['summary']['approval_cards'] == 3
    assert payload['summary']['live_sends'] == 0
