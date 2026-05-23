"""Dealix Internal API package.

This subpackage holds the **internal** (founder-facing) plumbing used by
the Founder Console: auth gate, private runtime reader, and policy
adapter. All endpoints under `api/routers/internal/` use these primitives.

Nothing in this package is allowed to perform external sending or
otherwise breach the trust boundary defined in `CLAUDE.md`.
"""
