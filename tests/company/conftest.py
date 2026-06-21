"""Shared test fixtures and configuration for company module tests."""

import csv
import tempfile
from pathlib import Path
from typing import Iterator

import pytest


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    """Create and cleanup temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_csv_file(temp_dir: Path) -> Path:
    """Create a valid test CSV file."""
    csv_path = temp_dir / "test_data.csv"
    with csv_path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'company', 'sector', 'phone', 'website', 'pain_angle',
            'recommended_offer', 'priority_score', 'notes'
        ])
        writer.writeheader()
        writer.writerows([
            {
                'company': 'Test Company 1',
                'sector': 'healthcare',
                'phone': '+966501234567',
                'website': 'example.com',
                'pain_angle': 'تحتاج نظام متابعة',
                'recommended_offer': 'WhatsApp Revenue OS',
                'priority_score': '75',
                'notes': 'High potential',
            },
            {
                'company': 'Test Company 2',
                'sector': 'restaurant',
                'phone': '',
                'website': 'test.com',
                'pain_angle': 'التقييمات',
                'recommended_offer': 'Review Intelligence OS',
                'priority_score': '',
                'notes': '',
            },
        ])
    return csv_path


@pytest.fixture
def temp_broken_csv(temp_dir: Path) -> Path:
    """Create a malformed CSV file for error handling tests."""
    csv_path = temp_dir / "broken.csv"
    csv_path.write_text('not,valid,csv\x00file', encoding='utf-8')
    return csv_path


@pytest.fixture
def sample_row() -> dict:
    """Sample lead row for testing."""
    return {
        'company': 'Sample Corp',
        'sector': 'healthcare',
        'phone': '+966501234567',
        'website': 'sample.com',
        'contact': '+966501234567',
        'pain_angle': 'تحتاج نظام متابعة واضح',
        'recommended_offer': 'Transformation Diagnostic Sprint',
        'priority_score': '50',
        'notes': 'Strong prospect',
        'company_name': 'Sample Corp',
        'title': 'Sample Corp',
        'segment': 'healthcare',
        'link': 'sample.com',
        'snippet': 'Sample company',
        'core_offer': 'Diagnostic',
        'main_problem': 'واتساب',
        'budget_range': '25k - 75k',
        'whatsapp': 'yes',
        'weekly_leads': '50',
    }


@pytest.fixture
def sample_row_missing() -> dict:
    """Row with missing fields for fallback testing."""
    return {
        'company': 'Minimal Corp',
        'sector': 'general',
    }


@pytest.fixture
def sample_row_invalid_score() -> dict:
    """Row with invalid score field."""
    return {
        'company': 'Invalid Corp',
        'priority_score': 'not_a_number',
    }


@pytest.fixture
def sample_lead_from_places() -> dict:
    """Sample lead from Google Places API."""
    return {
        'company_name': 'Test Clinic',
        'phone': '+966501234567',
        'website': 'clinic.com',
        'rating': '4.5',
        'user_rating_count': '120',
        'pain_angle': 'استفسارات لا تُجاب',
    }


# Test data constants
VALID_SCORE_ROW = {
    'phone': '+966501234567',
    'website': 'example.com',
    'pain_angle': 'test',
    'recommended_offer': 'Diagnostic',
}

HIGH_SCORE_ROW = {
    'phone': '+966501234567',
    'website': 'example.com',
    'pain_angle': 'تحتاج نظام',
    'recommended_offer': 'Diagnostic',
    'priority_score': '95',
}

NO_CONTACT_ROW = {
    'company': 'Test',
    'pain_angle': 'تحتاج نظام',
}

SECTORS = [
    'healthcare',
    'restaurant',
    'real_estate',
    'training',
    'agency',
]

PAIN_ANGLES_AR = [
    'تحتاج نظام متابعة',
    'الاستفسارات تضيع في واتساب',
    'التقييمات لا تُستغل',
    'الإدارة لا ترى الحقيقة',
    'العملاء متفرقون',
]

OFFERS = [
    'WhatsApp Revenue OS',
    'Review Intelligence OS',
    'AI Business Command Center',
    'Brand Intelligence OS',
    'Growth Engine OS',
    'Transformation Diagnostic Sprint',
]


# Assertion helpers
class AssertScore:
    """Helper for score assertions."""

    @staticmethod
    def is_valid(score: int) -> bool:
        """Check if score is valid (0-100)."""
        return 0 <= score <= 100

    @staticmethod
    def is_minimum(score: int, minimum: int) -> bool:
        """Check if score meets minimum."""
        return score >= minimum

    @staticmethod
    def is_maxed(score: int) -> bool:
        """Check if score is at maximum (100)."""
        return score == 100

    @staticmethod
    def equals(score: int, expected: int) -> bool:
        """Check if score equals expected."""
        return score == expected


# Markers for selective test running
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "csv: marks tests that use CSV files"
    )
    config.addinivalue_line(
        "markers", "score: marks tests for scoring functions"
    )
