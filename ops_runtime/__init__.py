"""Dealix Ops Runtime.

Read-only calculators that derive operating metrics from the private
ops tree (pipeline tracker, revenue action log, finance ledger).

All functions take a string path to the private-ops root and never
mutate state — they only read CSV/Markdown evidence and return dicts.
"""
