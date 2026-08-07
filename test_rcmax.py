import rcmax


def test_rcmax_builds_practical_command():
    payload = rcmax.build_payload()
    assert payload['summary']['target_companies'] == 30
    assert payload['summary']['first_10_companies'] == 10
    assert payload['summary']['materials_sectors'] == 4
    assert payload['summary']['service_stages'] >= 7
    assert payload['command']['account']
    assert payload['command']['offer']
    assert rcmax.verify(payload) == []


def test_rcmax_client_service_is_complete():
    payload = rcmax.build_payload()
    assert len(payload['service_blueprint']['inputs_needed']) == 6
    assert len(payload['service_blueprint']['client_outputs']) == 6
    assert len(payload['proposal_folder']['discovery_script']) == 5
    assert payload['proposal_folder']['mode'] == 'draft_only'


def test_rcmax_is_review_first():
    payload = rcmax.build_payload()
    assert payload['summary']['live'] == 0
    assert payload['command']['live'] == 0
    assert payload['command']['review_required'] is True
    assert len(payload['pricing_guidance']['do_not_commit']) == 4
