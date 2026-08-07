from app.leadership.x5 import build_payload, verify_payload


def test_x5_builds_action_registry():
    payload = build_payload()
    assert payload['summary']['actions'] == 7
    assert payload['summary']['approval_items'] == 7
    assert payload['summary']['audit_events'] == 7


def test_x5_is_review_first():
    payload = build_payload()
    assert payload['summary']['auto_execute'] == 0
    assert verify_payload(payload) == []


def test_x5_actions_are_ranked_and_owned():
    payload = build_payload()
    priorities = [item['priority'] for item in payload['actions']]
    assert priorities == sorted(priorities, reverse=True)
    for item in payload['actions']:
        assert item['owner']
        assert item['status'] == 'ready_for_review'
        assert item['approval_required'] is True
