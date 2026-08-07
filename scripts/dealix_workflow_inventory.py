import re
from pathlib import Path

WORKFLOWS = Path('.github/workflows')

def main():
    if not WORKFLOWS.exists():
        print('NO-GO: .github/workflows missing')
        raise SystemExit(1)
    files = sorted(WORKFLOWS.glob('*.yml')) + sorted(WORKFLOWS.glob('*.yaml'))
    print('# Workflow Inventory')
    if not files:
        print('NO-GO: no workflows found')
        raise SystemExit(1)
    risky = []
    for f in files:
        text = f.read_text(encoding='utf-8', errors='ignore')
        has_permissions = 'permissions:' in text
        read_only = re.search(r'contents:\s*read', text) is not None
        print(f'- {f.as_posix()} | permissions={has_permissions} | contents_read={read_only}')
        if not has_permissions or not read_only:
            risky.append(f.as_posix())
    if risky:
        print('WARN: workflows needing permission review:')
        for f in risky: print(f'  - {f}')
    else:
        print('OK: workflows include explicit read-oriented permissions')

if __name__ == '__main__':
    main()
