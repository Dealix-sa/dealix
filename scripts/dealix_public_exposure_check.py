#!/usr/bin/env python3
from pathlib import Path
import sys
bad=[]
public_roots=[Path('frontend/public'), Path('public')]
keywords=['DATABASE_URL','SECRET','API_KEY','TOKEN','PRIVATE KEY','password']
for root in public_roots:
    if not root.exists(): continue
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() not in {'.png','.jpg','.jpeg','.ico','.svg','.webp'}:
            txt=p.read_text(encoding='utf-8', errors='ignore')
            for k in keywords:
                if k.lower() in txt.lower(): bad.append((str(p), k))
if bad:
    print('Public exposure risk:')
    for p,k in bad: print('-',p,k)
    sys.exit(1)
print('OK: no obvious public exposure markers')
