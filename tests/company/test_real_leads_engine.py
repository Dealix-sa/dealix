"""Tests for company.leads.real_leads_engine module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from company.leads import real_leads_engine


class TestScore:
    """Test real leads scoring."""

    def test_score_base(self):
        """Test base score for real leads."""
        row = {}
        score = real_leads_engine.score(row)
        assert score == 45  # Base score for real leads is 45

    def test_score_with_phone(self):
        """Test score with phone number."""
        row = {'phone': '+966501234567'}
        score = real_leads_engine.score(row)
        assert score >= 65  # 45 + 20

    def test_score_with_website(self):
        """Test score with website."""
        row = {'website': 'example.com'}
        score = real_leads_engine.score(row)
        assert score >= 55  # 45 + 10

    def test_score_with_rating(self):
        """Test score with good rating."""
        row = {'rating': '4.5'}
        score = real_leads_engine.score(row)
        assert score >= 50  # 45 + 5

    def test_score_with_rating_count(self):
        """Test score with many reviews."""
        row = {'user_rating_count': '100'}
        score = real_leads_engine.score(row)
        assert score >= 60  # 45 + 15

    def test_score_invalid_rating(self):
        """Test invalid rating doesn't crash."""
        row = {'rating': 'not_a_number'}
        score = real_leads_engine.score(row)
        assert score >= 45  # Base score

    def test_score_invalid_count(self):
        """Test invalid count doesn't crash."""
        row = {'user_rating_count': 'many'}
        score = real_leads_engine.score(row)
        assert score >= 45  # Base score

    def test_score_poor_rating(self):
        """Test score with poor rating."""
        row = {'rating': '2.5'}
        score = real_leads_engine.score(row)
        assert score >= 55  # 45 + 10 for 0 < rating < 4.0

    def test_score_max_cap(self):
        """Test score never exceeds 100."""
        row = {
            'phone': '+966501234567',
            'website': 'example.com',
            'user_rating_count': '500',
            'rating': '4.8',
        }
        score = real_leads_engine.score(row)
        assert score <= 100


class TestText:
    """Test text extraction utility."""

    def test_text_from_string(self):
        """Test extracting text from string."""
        result = real_leads_engine.text('Hello')
        assert result == 'Hello'

    def test_text_from_dict_with_text(self):
        """Test extracting text from dict."""
        result = real_leads_engine.text({'text': 'Company Name'})
        assert result == 'Company Name'

    def test_text_from_none(self):
        """Test None returns empty string."""
        result = real_leads_engine.text(None)
        assert result == ''

    def test_text_from_number(self):
        """Test number conversion to string."""
        result = real_leads_engine.text(123)
        assert result == '123'
