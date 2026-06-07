#!/usr/bin/env python3
import re, sys
from pathlib import Path
patterns=[
    # Negative lookbehind prevents matching substrings like "risk-management-framework"
    ('openai', re.compile(r'(?<![A-Za-z])sk-[A-Za-z0-9_\-]{20,}')),
    ('github_pat', re.compile(r'github_pat_[A-Za-z0-9_]{20,}')),
    ('ghp', re.compile(r'ghp_[A-Za-z0-9]{20,}')),
    ('jwt', re.compile(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+')),
]
# tests/ and docs/ are excluded: test files intentionally contain fake credential
# patterns, and docs contain illustrative examples (e.g. sk-ant-xxxx placeholders).
exclude={'.git','node_modules','.next','venv','env','__pycache__','tests','docs'}
hits=[]
for path in Path('.').rglob('*'):
    if any(part in exclude for part in path.parts) or not path.is_file(): continue
    if path.suffix.lower() in {'.png','.jpg','.jpeg','.zip','.pdf','.ico'}: continue
    try: text=path.read_text(encoding='utf-8', errors='ignore')
    except Exception: continue
    for name, rx in patterns:
        if rx.search(text): hits.append((str(path), name))
if hits:
    print('Potential secret exposure:')
    for h in hits: print('-', h[0], h[1])
    sys.exit(1)
print('OK: no obvious secret patterns found')
