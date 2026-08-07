"""Tests for company.intake.intake_engine module."""

from company.intake import intake_engine


class TestScore:
    """Test intake scoring — score() returns (int, tier_str, leakage_list)."""

    def test_score_base(self):
        """Empty row gets base score of 30 + default budget 3 = 33, tier D."""
        row = {}
        points, tier, leakage = intake_engine.score(row)
        assert points == 33
        assert tier == "D"
        assert leakage == []

    def test_score_with_weekly_leads(self):
        """100 leads adds 25 points on top of base."""
        row = {'weekly_leads': '100'}
        points, tier, _ = intake_engine.score(row)
        assert points >= 55  # 30 + 25 + 3(budget default)

    def test_score_with_problem(self):
        """main_problem adds 10 points."""
        row = {'main_problem': 'واتساب'}
        points, tier, _ = intake_engine.score(row)
        assert points >= 40  # 30 + 10 + 3(budget)

    def test_score_with_budget(self):
        """75k+ budget adds 15 points."""
        row = {'budget_range': '75k+'}
        points, tier, _ = intake_engine.score(row)
        assert points >= 45  # 30 + 15

    def test_score_invalid_weekly_leads(self):
        """Invalid weekly_leads don't crash; base score still returned."""
        row = {'weekly_leads': 'not_a_number'}
        points, tier, _ = intake_engine.score(row)
        assert points >= 30

    def test_score_max_cap(self):
        """Score never exceeds 100."""
        row = {
            'weekly_leads': '500',
            'main_problem': 'واتساب',
            'whatsapp': 'yes',
            'budget_range': '75k+',
        }
        points, tier, _ = intake_engine.score(row)
        assert points <= 100


class TestRecommend:
    """Test offer recommendation via recommend_offer()."""

    def test_recommend_whatsapp(self):
        """Test recommends WhatsApp OS."""
        row = {'main_problem': 'واتساب'}
        offer = intake_engine.recommend_offer(row)
        assert 'WhatsApp' in offer

    def test_recommend_review(self):
        """Test recommends Review Intelligence."""
        row = {'main_problem': 'تقييم'}
        offer = intake_engine.recommend_offer(row)
        assert 'Review' in offer

    def test_recommend_brand(self):
        """Test recommends Brand Intelligence."""
        row = {'main_problem': 'هوية'}
        offer = intake_engine.recommend_offer(row)
        assert 'Brand' in offer

    def test_recommend_training(self):
        """Test recommends Growth Engine for training."""
        row = {'sector': 'تدريب'}
        offer = intake_engine.recommend_offer(row)
        assert 'Growth' in offer

    def test_recommend_default(self):
        """Test default recommendation."""
        row = {}
        offer = intake_engine.recommend_offer(row)
        assert 'Diagnostic' in offer

    def test_recommend_case_insensitive(self):
        """Test recommendations are case insensitive."""
        row = {'main_problem': 'WHATSAPP'}
        offer = intake_engine.recommend_offer(row)
        assert 'WhatsApp' in offer or 'Diagnostic' in offer
