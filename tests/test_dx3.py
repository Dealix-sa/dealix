from app.leadership.dx3 import LANES, build_payload, verify_payload


def test_dx3_covers_all_leadership_lanes():
    payload = build_payload()
    assert payload['summary']['lanes'] == len(LANES)
    for lane in LANES:
        assert payload['lane_counts'][lane] > 0


def test_dx3_has_ranked_priorities():
    payload = build_payload()
    assert payload['summary']['items'] >= 15
    assert payload['summary']['top_items'] == 7
    scores = [item['score'] for item in payload['top_items']]
    assert scores == sorted(scores, reverse=True)


def test_dx3_is_review_first():
    payload = build_payload()
    assert payload['summary']['auto_execute'] == 0
    assert payload['summary']['review_required'] == payload['summary']['items']
    assert verify_payload(payload) == []


def test_dx3_items_have_operating_fields():
    payload = build_payload()
    for item in payload['items']:
        assert item['owner']
        assert item['why_now']
        assert item['next_step']
        assert item['metric']
        assert 0 <= item['score'] <= 100
