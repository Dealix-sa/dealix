import dealix_acquisition_pack


def test_t10_builds_sector_packs():
    payload = dealix_acquisition_pack.build_payload()
    assert payload['summary']['sector_packs'] == 4
    assert payload['summary']['proposal_templates'] == 4
    assert payload['summary']['discovery_scripts'] == 4


def test_t10_assets_are_complete():
    payload = dealix_acquisition_pack.build_payload()
    for pack in payload['packs']:
        assert pack['one_page_offer']['headline']
        assert pack['proposal_template']['scope']
        assert pack['proposal_template']['not_in_scope']
        assert len(pack['discovery_script']) == 5
        assert pack['drafts']['mode'] == 'draft_only'


def test_t10_is_review_first_and_commercial():
    payload = dealix_acquisition_pack.build_payload()
    assert payload['summary']['live'] == 0
    assert payload['founder_command']['review_required'] is True
    assert payload['founder_command']['live'] == 0
    assert payload['summary']['revenue_accounts'] == 5
    assert dealix_acquisition_pack.verify(payload) == []
