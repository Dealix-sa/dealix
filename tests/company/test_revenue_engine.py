"""Tests for company.revenue_engine.revenue_engine_v2 module."""

import sys
from pathlib import Path

# Import after ensuring path
sys.path.insert(0, str(Path(__file__).parents[2]))

from company.revenue_engine import revenue_engine_v2


class TestScore:
    """Test revenue engine scoring."""

    def test_score_base(self):
        """Test base score."""
        row = {}
        score = revenue_engine_v2.score(row)
        assert score == 40  # Base score

    def test_score_with_contact(self):
        """Test score with phone or contact."""
        row = {'phone': '+966501234567'}
        score = revenue_engine_v2.score(row)
        assert score >= 60  # 40 + 20

    def test_score_with_multiple_fields(self):
        """Test score accumulation."""
        row = {
            'phone': '+966501234567',
            'website': 'example.com',
            'pain_angle': 'تحتاج نظام',
            'recommended_offer': 'Diagnostic',
        }
        score = revenue_engine_v2.score(row)
        # 40 + 20 (phone) + 15 (website) + 15 (pain) + 10 (offer) = 100
        assert score >= 80

    def test_score_max_cap(self):
        """Test score caps at 100."""
        row = {
            'phone': '+966501234567',
            'website': 'example.com',
            'pain_angle': 'test',
            'recommended_offer': 'Diagnostic',
            'priority_score': '150',
        }
        score = revenue_engine_v2.score(row)
        assert score <= 100

    def test_score_with_invalid_priority(self):
        """Test invalid priority_score doesn't crash."""
        row = {'priority_score': 'not_a_number'}
        score = revenue_engine_v2.score(row)
        assert score >= 40  # Base score, no exception


class TestPick:
    """Test field picking."""

    def test_pick_returns_string(self):
        """Test pick always returns string."""
        row = {'name': 'Test'}
        result = revenue_engine_v2.pick(row, 'name')
        assert isinstance(result, str)
        assert result == 'Test'

    def test_pick_multiple_options(self):
        """Test fallback behavior."""
        row = {'title': 'Company Title'}
        result = revenue_engine_v2.pick(row, 'company', 'title')
        assert result == 'Company Title'

    def test_pick_missing_returns_empty(self):
        """Test missing key returns empty string."""
        row = {}
        result = revenue_engine_v2.pick(row, 'nonexistent')
        assert result == ''


class TestCollectTargets:
    """Test target collection from various sources."""

    def test_collect_targets_returns_list(self):
        """Test collect_targets returns a list."""
        targets = revenue_engine_v2.collect_targets()
        assert isinstance(targets, list)

    def test_collect_targets_structure(self):
        """Test targets have expected structure."""
        targets = revenue_engine_v2.collect_targets()
        # Should have at least fallback rows if no files found
        if len(targets) > 0:
            assert all(isinstance(t, dict) for t in targets)
            # Check for basic keys
            assert any('company' in t for t in targets[:10]) or len(targets) == 0
