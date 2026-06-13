from pathlib import Path
contracts=list(Path('prompts/contracts').glob('*.md'))
if len(contracts)<8:
    print('Expected at least 8 prompt contracts, found', len(contracts)); raise SystemExit(1)
for p in contracts:
    text=p.read_text(encoding='utf-8')
    if 'Output' not in text and 'Output JSON' not in text:
        print('Missing output spec:', p); raise SystemExit(1)
print('OK: prompt contracts look structured')
