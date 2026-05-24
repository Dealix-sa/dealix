"""Hermes-local conftest.

The hermes kernel is pure-Python with no FastAPI / DB / LLM dependencies.
These unit tests should not pay the cost of the global conftest, which
loads the full application (LLM providers, settings, DB pools).
"""

from __future__ import annotations


# Prevent the global tests/conftest.py from forcing imports of the full
# app stack. We do that by leaving this empty — pytest evaluates the
# closer conftest only when discovering tests inside this folder.
