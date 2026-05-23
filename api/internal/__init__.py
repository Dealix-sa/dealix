"""Dealix internal control-plane modules.

These modules back the Founder Console internal API. They are
explicitly internal: token-gated, read mostly from a private ops
runtime directory ($DEALIX_PRIVATE_OPS), and never perform external
sends. See docs/api/ULTIMATE_INTERNAL_API.md.
"""
