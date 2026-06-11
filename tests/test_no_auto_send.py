#!/usr/bin/env python3
"""
Test: No Auto-Send Enforcement
Scans repo for suspicious auto-send patterns in executable code.
Allows docs to discuss these terms; fails on executable automation.
"""

import ast
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Patterns that indicate possible auto-send in executable code
FORBIDDEN_CALLS = {"send_whatsapp", "send_email", "send_sms"}
FORBIDDEN_ASSIGNMENTS = {"auto_send=True", "auto_send = True", "without_review=True", "without_review = True"}
FORBIDDEN_STRINGS = {"review_status=\"approved\"", "review_status='approved'", "review_status= \"approved\"", "review_status = 'approved'"}

def is_doc_or_test(path: Path) -> bool:
    parts = path.parts
    if "test" in path.name:
        return True
    for p in parts:
        if p in {"docs", "doc", "reports", "README.md", "README.ar.md"}:
            return True
    return False

def scan_python_file(path: Path) -> list:
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    # Skip if clearly a doc/test (we still parse to be safe)
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                findings.append((path, node.lineno, f"Forbidden call: {node.func.id}()"))
            elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_CALLS:
                findings.append((path, node.lineno, f"Forbidden call: *.{node.func.attr}()"))

    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for assign in FORBIDDEN_ASSIGNMENTS:
            if assign in stripped:
                findings.append((path, line_no, f"Forbidden assignment: {assign}"))
        for s in FORBIDDEN_STRINGS:
            if s in stripped:
                findings.append((path, line_no, f"Forbidden hardcoded approval: {s}"))

    return findings

def test_no_auto_send():
    findings = []
    skip_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", ".ruff_cache", ".pytest_cache"}
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f.endswith(".py"):
                path = Path(root) / f
                # Allow discussion in docs/tests
                if is_doc_or_test(path):
                    continue
                findings.extend(scan_python_file(path))

    if findings:
        msg = "Auto-send patterns found in executable code:\n"
        for path, line, reason in findings:
            msg += f"  {path}:{line} {reason}\n"
        raise AssertionError(msg)
