from pathlib import Path


def test_commercial_launch_is_manual_only():
    text = Path("docs/saas/COMMERCIAL_LAUNCH_PLAYBOOK_AR.md").read_text(encoding="utf-8")
    assert "لا إرسال تلقائي" in text
    assert "لا واتساب حي" in text
    assert "لا وعود ROI" in text
