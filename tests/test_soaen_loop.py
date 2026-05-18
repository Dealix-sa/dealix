from dealix.commercial_ops.soaen_loop import WEEKLY_BOARD_QUESTIONS_AR, analyze_soaen_loop


def test_soaen_loop_schema() -> None:
    blob = analyze_soaen_loop()
    assert blob["schema_version"] == "1.0"
    assert len(WEEKLY_BOARD_QUESTIONS_AR) == 3
