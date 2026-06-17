"""Tests for company.intake.intake_engine module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from company.intake import intake_engine


class TestScore:
    """Test intake scoring."""

    def test_score_base(self):
        """Test base score."""
        row = {}
        score = intake_engine.score(row)
        assert score == 40

    def test_score_with_weekly_leads(self):
        """Test score with weekly leads."""
        row = {'weekly_leads': '100'}
        score = intake_engine.score(row)
        assert score >= 65  # 40 + 25

    def test_score_with_problem(self):
        """Test score with main problem."""
        row = {'main_problem': 'واتساب'}
        score = intake_engine.score(row)
        assert score >= 55  # 40 + 15

    def test_score_with_budget(self):
        """Test score with sufficient budget."""
        row = {'budget_range': '75k+'}
        score = intake_engine.score(row)
        assert score >= 50  # 40 + 10

    def test_score_invalid_weekly_leads(self):
        """Test invalid weekly leads don't crash."""
        row = {'weekly_leads': 'not_a_number'}
        score = intake_engine.score(row)
        assert score >= 40  # Base score

    def test_score_max_cap(self):
        """Test score never exceeds 100."""
        row = {
            'weekly_leads': '500',
            'main_problem': 'واتساب',
            'whatsapp': 'yes',
            'budget_range': '75k+',
        }
        score = intake_engine.score(row)
        assert score <= 100


class TestRecommend:
    """Test offer recommendation."""

    def test_recommend_whatsapp(self):
        """Test recommends WhatsApp OS."""
        row = {'main_problem': 'واتساب'}
        offer = intake_engine.recommend(row)
        assert 'WhatsApp' in offer

    def test_recommend_review(self):
        """Test recommends Review Intelligence."""
        row = {'main_problem': 'تقييم'}
        offer = intake_engine.recommend(row)
        assert 'Review' in offer

    def test_recommend_brand(self):
        """Test recommends Brand Intelligence."""
        row = {'main_problem': 'هوية'}
        offer = intake_engine.recommend(row)
        assert 'Brand' in offer

    def test_recommend_training(self):
        """Test recommends Growth Engine for training."""
        row = {'sector': 'تدريب'}
        offer = intake_engine.recommend(row)
        assert 'Growth' in offer

    def test_recommend_default(self):
        """Test default recommendation."""
        row = {}
        offer = intake_engine.recommend(row)
        assert 'Diagnostic' in offer

    def test_recommend_case_insensitive(self):
        """Test recommendations are case insensitive."""
        row = {'main_problem': 'WHATSAPP'}
        offer = intake_engine.recommend(row)
        assert 'WhatsApp' in offer or 'Diagnostic' in offer
