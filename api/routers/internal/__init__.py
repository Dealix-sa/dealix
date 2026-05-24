"""Internal (read-only) routers for the Dealix Founder Console.

Modules in this package MUST NOT perform external action (no send_email,
no send_whatsapp, no httpx.post to third-party APIs). Outbound actions
are reserved for governed routers behind approval_center.
"""
