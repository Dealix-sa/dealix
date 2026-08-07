from pathlib import Path

bad=[]
for p in Path('.github/workflows').glob('*.yml'):
    txt=p.read_text(encoding='utf-8')
    if 'permissions:' not in txt:
        bad.append(str(p))
print('# Workflow Permission Audit')
if bad:
    print('Needs permission review:')
    for p in bad: print(f'- {p}')
    raise SystemExit(2)
print('OK: all workflows declare permissions')
