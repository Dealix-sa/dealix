"""Local conftest for the CEO OS tests.

These tests only invoke CEO OS CLIs via subprocess and never touch the
app. We declare collect_ignore at this level so that the parent
tests/conftest.py is the only conftest active here — but we deliberately
avoid importing the parent's heavy app fixtures, since this directory
needs no httpx / LLM mocking. Pytest auto-discovers the parent conftest
regardless, so users who want to run *only* this directory can do so
with `pytest tests/ceo_os --no-header --confcutdir=tests/ceo_os`.
"""
