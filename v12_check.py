import dealix_gtm_launch_kit


def test_v12_builds_launch_kit():
    payload = dealix_gtm_launch_kit.build_payload()
    assert payload['summary']['checklist_items'] == 8
    assert payload['summary']['target_companies'] == 30
    assert payload['summary']['calendar_days'] == 7
    assert payload['summary']['proposal_folders'] == 10


def test_v12_has_onboarding_and_close_plan():
    payload = dealix_gtm_launch_kit.build_payload()
    assert payload['summary']['onboarding_steps'] == 7
    assert payload['summary']['close_plan_weeks'] == 4
    assert len(payload['weekly_close_plan']) == 4
    assert payload['kpi_dashboard']['live'] == 0


def test_v12_is_review_first_and_commercial_ready():
    payload = dealix_gtm_launch_kit.build_payload()
    assert payload['summary']['live'] == 0
    assert payload['summary']['sales_material_sectors'] == 4
    assert dealix_gtm_launch_kit.verify(payload) == []


def test_v12_company_plan_fields():
    payload = dealix_gtm_launch_kit.build_payload()
    for company in payload['company_plan']:
        assert company['company_id']
        assert company['sector']
        assert company['owner']
        assert company['review_required'] is True
