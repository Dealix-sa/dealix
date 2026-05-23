"""Dealix internal-only API surface for the Founder Console.

These endpoints serve internal runtime data and dispatch trust-gated
intent (approve / reject / request-edit / escalate). No external sending,
no proof publication, no automatic destructive operations are performed
through these endpoints.
"""
