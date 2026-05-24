"""Dealix internal API package.

All endpoints under api/routers/internal/* are mounted at /api/v1/internal
and require DEALIX_INTERNAL_TOKEN in production. They are NEVER exposed
to the public surface and never accept user-supplied auth tokens.
"""
