def test_commercial_launch_is_manual_only():
    text = open("docs/saas/COMMERCIAL_LAUNCH_PLAYBOOK_AR.md", encoding="utf-8").read()
    assert "لا إرسال تلقائي" in text
    assert "لا واتساب حي" in text
    assert "لا وعود ROI" in text
