#!/usr/bin/env python3
# Scans public-facing directories for actual credential patterns (not generic words).
# Uses the same regex approach as dealix_secret_smoke_check.py to avoid false positives
# on landing pages that legitimately use words like TOKEN/SECRET in their content.
import re, sys
from pathlib import Path

patterns = [
    ('openai_key',    re.compile(r'(?<![A-Za-z])sk-[A-Za-z0-9_\-]{20,}')),
    ('github_pat',    re.compile(r'github_pat_[A-Za-z0-9_]{20,}')),
    ('ghp_token',     re.compile(r'ghp_[A-Za-z0-9]{20,}')),
    ('jwt',           re.compile(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+')),
    ('stripe_live',   re.compile(r'sk_live_[A-Za-z0-9]{20,}')),
    ('aws_key',       re.compile(r'AKIA[0-9A-Z]{16}')),
]

public_roots = [Path('frontend/public'), Path('public'), Path('landing')]
skip_ext = {'.png', '.jpg', '.jpeg', '.ico', '.svg', '.webp', '.woff', '.woff2', '.ttf'}
bad = []

for root in public_roots:
    if not root.exists():
        continue
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix.lower() in skip_ext:
            continue
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for name, rx in patterns:
            if rx.search(txt):
                bad.append((str(p), name))

if bad:
    print('Public exposure risk (real credential patterns found in public assets):')
    for p, k in bad:
        print('-', p, k)
    sys.exit(1)
print('OK: no credential patterns found in public assets')
