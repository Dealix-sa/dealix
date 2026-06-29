import dealix_sales_materials_factory


def test_u11_builds_all_sector_materials():
    payload = dealix_sales_materials_factory.build_payload()
    assert payload['summary']['sectors'] == 4
    assert payload['summary']['one_page_offers'] == 4
    assert payload['summary']['proposals'] == 4
    assert payload['summary']['landing_pages'] == 4
    assert payload['summary']['proof_templates'] == 4


def test_u11_sequences_and_battlecards_exist():
    payload = dealix_sales_materials_factory.build_payload()
    assert payload['summary']['battlecards'] == 4
    assert payload['summary']['pricing_items'] == 3
    for material in payload['materials']:
        assert len(material['email_sequence']) == 3
        assert len(material['whatsapp_sequence']) == 3
        assert len(material['linkedin_posts']) == 2
        assert material['mode'] == 'draft_only'


def test_u11_is_review_first():
    payload = dealix_sales_materials_factory.build_payload()
    assert payload['summary']['live'] == 0
    assert dealix_sales_materials_factory.verify(payload) == []
