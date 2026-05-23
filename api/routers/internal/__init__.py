"""Internal (founder-facing) API routers.

Everything mounted from this package is gated by the
``X-Dealix-Internal-Token`` header in production. See
``api/internal/auth.py``.
"""
