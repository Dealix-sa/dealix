from scripts.launch.run_launch_now import SAFE_ENV, StepResult


def test_launch_command_center_safe_env_defaults():
    assert SAFE_ENV["APP_ENV"] == "test"
    assert SAFE_ENV["ENVIRONMENT"] == "test"
    assert SAFE_ENV["EXTERNAL_SEND_ENABLED"] == "false"
    assert SAFE_ENV["EMAIL_SEND_ENABLED"] == "false"
    assert SAFE_ENV["WHATSAPP_SEND_ENABLED"] == "false"
    assert SAFE_ENV["WHATSAPP_ALLOW_LIVE_SEND"] == "false"
    assert SAFE_ENV["SMS_SEND_ENABLED"] == "false"
    assert SAFE_ENV["OUTBOUND_MODE"] == "draft_only"


def test_step_result_contract():
    result = StepResult(
        name="Example",
        command=["python", "--version"],
        required=True,
        returncode=0,
        status="pass",
    )

    assert result.required is True
    assert result.status == "pass"
    assert result.returncode == 0
