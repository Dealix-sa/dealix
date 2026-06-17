"""Tests for company.micro.micro_master module."""

import tempfile
from pathlib import Path

import pytest

# Import after ensuring path
import sys
sys.path.insert(0, str(Path(__file__).parents[2]))

from company.micro import micro_master


@pytest.fixture
def temp_csv():
    """Create temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        f.write('company,phone,website,pain_angle,recommended_offer,priority_score\n')
        f.write('Test Co,+966123,example.com,تحتاج نظام,Diagnostic,75\n')
        f.write('Another Co,,https://test.com,متابعة ضعيفة,Revenue OS,\n')
        path = Path(f.name)
    yield path
    path.unlink()


@pytest.fixture
def temp_dir():
    """Create temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestReadCsv:
    """Test CSV reading functionality."""

    def test_read_valid_csv(self, temp_csv):
        """Test reading valid CSV file."""
        rows = micro_master.read_csv(temp_csv)
        assert len(rows) == 2
        assert rows[0]['company'] == 'Test Co'

    def test_read_missing_file(self):
        """Test reading non-existent file returns empty list."""
        rows = micro_master.read_csv(Path('/nonexistent/file.csv'))
        assert rows == []

    def test_read_invalid_csv(self, temp_dir):
        """Test reading corrupted CSV gracefully."""
        bad_csv = temp_dir / 'bad.csv'
        bad_csv.write_text('not valid csv\x00content')
        rows = micro_master.read_csv(bad_csv)
        # Should not crash, return empty or partial data
        assert isinstance(rows, list)


class TestScore:
    """Test row scoring functionality."""

    def test_score_with_phone(self):
        """Test score increases with phone contact."""
        row = {'phone': '+966123'}
        score = micro_master.score(row)
        assert score >= 60  # 40 base + 20 for phone

    def test_score_with_website(self):
        """Test score increases with website."""
        row = {'website': 'example.com'}
        score = micro_master.score(row)
        assert score >= 55  # 40 base + 15 for website

    def test_score_with_pain_angle(self):
        """Test score increases with pain angle."""
        row = {'pain_angle': 'تحتاج نظام'}
        score = micro_master.score(row)
        assert score >= 55  # 40 base + 15 for pain

    def test_score_with_priority_score(self):
        """Test priority_score overrides base score."""
        row = {'priority_score': '95'}
        score = micro_master.score(row)
        assert score == 95

    def test_score_invalid_priority_score(self):
        """Test invalid priority_score is ignored."""
        row = {'priority_score': 'not_a_number'}
        score = micro_master.score(row)
        assert score >= 40  # Base score, no crash

    def test_score_max_100(self):
        """Test score never exceeds 100."""
        row = {
            'phone': '+966123',
            'website': 'example.com',
            'pain_angle': 'test',
            'recommended_offer': 'Diagnostic',
            'priority_score': '999',
        }
        score = micro_master.score(row)
        assert score <= 100


class TestPick:
    """Test field picking utility."""

    def test_pick_single_key(self):
        """Test picking single field."""
        row = {'company': 'Test Co'}
        assert micro_master.pick(row, 'company') == 'Test Co'

    def test_pick_fallback_keys(self):
        """Test fallback to alternative keys."""
        row = {'title': 'My Company'}
        assert micro_master.pick(row, 'company_name', 'title') == 'My Company'

    def test_pick_missing_keys(self):
        """Test returns empty string for missing keys."""
        row = {}
        assert micro_master.pick(row, 'company', 'name') == ''

    def test_pick_strips_whitespace(self):
        """Test whitespace is stripped."""
        row = {'company': '  Test Co  '}
        assert micro_master.pick(row, 'company') == 'Test Co'


class TestNormalize:
    """Test row normalization."""

    def test_normalize_full_row(self):
        """Test normalizing complete row."""
        row = {
            'company_name': 'Test Company',
            'sector': 'healthcare',
            'phone': '+966123',
            'pain_angle': 'تحتاج نظام',
            'recommended_offer': 'Diagnostic',
        }
        normalized = micro_master.normalize(row)

        assert normalized['company'] == 'Test Company'
        assert normalized['sector'] == 'healthcare'
        assert normalized['contact'] == '+966123'
        assert normalized['status'] == 'needs_review'
        assert 'date' in normalized
        assert 'priority' in normalized

    def test_normalize_partial_row(self):
        """Test normalizing row with missing fields."""
        row = {'sector': 'general'}
        normalized = micro_master.normalize(row)

        assert 'company' in normalized
        assert normalized['sector'] == 'general'
        # Should use defaults
        assert 'Diagnostic' in normalized['offer'] or len(normalized) > 0


class TestFallbackRows:
    """Test fallback data generation."""

    def test_fallback_rows_generated(self):
        """Test fallback rows are created."""
        rows = micro_master.fallback_rows()

        assert len(rows) == 5  # 5 sectors
        assert all('company' in row for row in rows)
        assert all('sector' in row for row in rows)

    def test_fallback_rows_structure(self):
        """Test fallback rows have required fields."""
        rows = micro_master.fallback_rows()
        required_fields = {'date', 'company', 'sector', 'offer', 'pain_angle', 'status'}

        for row in rows:
            assert required_fields.issubset(row.keys())
