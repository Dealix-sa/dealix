"""Follow-up Engine produces D1/D3/D7 tasks and respects opt-out."""

from __future__ import annotations

from app.commercial import followup_engine


def test_three_tasks_d1_d3_d7():
    tasks = followup_engine.build_followup_tasks("c1", "email")
    days = sorted(t.due_in_days for t in tasks)
    assert days == [1, 3, 7]
    assert all(t.status == "open" for t in tasks)
    assert all(t.draft_note for t in tasks)


def test_opted_out_produces_no_tasks():
    tasks = followup_engine.build_followup_tasks("c1", "email", opted_out=True)
    assert tasks == []


def test_build_for_cards_skips_opted_out_accounts():
    cards = [
        type("C", (), {"card_id": "c1", "recommended_channel": "email", "account_id": "a1"})(),
        type("C", (), {"card_id": "c2", "recommended_channel": "email", "account_id": "a2"})(),
    ]
    accounts = {
        "a1": {"contactability_status": "contactable", "owner": "sami", "email_opt_out": False},
        "a2": {"contactability_status": "opted_out", "owner": "sami", "email_opt_out": True},
    }
    tasks = followup_engine.build_followups_for_cards(cards, accounts)
    card_ids = {t.card_id for t in tasks}
    assert "c1" in card_ids
    assert "c2" not in card_ids
