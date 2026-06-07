from pathlib import Path
import re

def main():
    mdir = Path('db/migrations')
    files = sorted(mdir.glob('*.sql')) if mdir.exists() else []
    if not files:
        print('NO-GO: no migrations found')
        raise SystemExit(1)
    nums=[]
    print('# Migration Order')
    for f in files:
        m=re.match(r'(\d+)_', f.name)
        num=int(m.group(1)) if m else None
        nums.append(num)
        print(f'- {f.name}')
    expected=list(range(min(nums), max(nums)+1)) if all(n is not None for n in nums) else []
    if nums != expected:
        print(f'WARN: migration numbering not contiguous: {nums}')
    else:
        print('OK: migration order is contiguous')

if __name__ == '__main__':
    main()
