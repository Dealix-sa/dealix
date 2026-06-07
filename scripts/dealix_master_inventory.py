from pathlib import Path
from collections import Counter

EXCLUDE = {'.git', 'node_modules', '.next', '__pycache__'}

def main():
    files = []
    for p in Path('.').rglob('*'):
        if p.is_file() and not any(part in EXCLUDE for part in p.parts):
            files.append(p)
    counts = Counter(p.parts[0] for p in files if p.parts)
    out = Path('out/consolidation')
    out.mkdir(parents=True, exist_ok=True)
    report = ['# Dealix Master Inventory', '', f'Total files: {len(files)}', '', '## By top-level directory']
    for k, v in sorted(counts.items()):
        report.append(f'- {k}: {v}')
    report.append('\n## File list')
    for p in sorted(files):
        report.append(f'- {p.as_posix()}')
    (out/'master_inventory.md').write_text('\n'.join(report)+'\n', encoding='utf-8')
    print(f'Wrote {out}/master_inventory.md')
    print(f'Total files: {len(files)}')

if __name__ == '__main__':
    main()
