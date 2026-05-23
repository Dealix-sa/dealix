"""Internal API routers — Founder Console v2 surface.

Routers in this package are intended for the internal Founder Console only.
They MUST never be exposed to public traffic without Trust Plane evaluation.
"""

from api.routers.internal import founder_console

__all__ = ["founder_console"]
