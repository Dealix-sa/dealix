import z7_router


def test_z7_builds_routes_for_all_channels():
    payload = z7_router.build_payload()
    assert payload['summary']['channels'] == 6
    assert payload['summary']['routes'] == 42
    assert payload['summary']['prepared'] == 42


def test_z7_routes_are_review_only():
    payload = z7_router.build_payload()
    assert payload['summary']['live'] == 0
    assert payload['summary']['needs_review'] == payload['summary']['routes']
    assert z7_router.verify(payload) == []


def test_z7_route_fields_exist():
    payload = z7_router.build_payload()
    for route in payload['routes']:
        assert route['route_id']
        assert route['action_id']
        assert route['owner']
        assert route['channel'] in z7_router.CHANNELS
        assert route['mode'] == 'draft'
