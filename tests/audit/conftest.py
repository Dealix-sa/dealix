"""Local conftest for the Audit-First Remediation tests.

Intentionally minimal — these tests must be runnable in CI without the
heavy backend test dependencies (httpx, pytest-asyncio, etc.) used by
the rest of the suite. Having this file shadows tests/conftest.py for
this directory.
"""
