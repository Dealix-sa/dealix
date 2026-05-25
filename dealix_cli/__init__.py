"""Dealix CEO CLI.

A small command-line layer that wraps the Execution Assurance System scripts.
The CLI is intentionally thin: every command shells out to a script under
``scripts/`` so the same behaviour is reproducible from CI, the Makefile,
or a direct Python invocation. Today it ships a single command, ``assurance``,
which reads real evidence from a private ops repository (passed via
``--private-ops``) and writes ``evidence/execution_assurance_report.md``
under that root.
"""
