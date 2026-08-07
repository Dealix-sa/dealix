from pathlib import Path

migrations=sorted(Path('db/migrations').glob('*.sql'))
print('# Migration Plan')
for i,m in enumerate(migrations,1):
    text=m.read_text(encoding='utf-8')
    creates=text.lower().count('create table')
    indexes=text.lower().count('create index')
    print(f'{i}. {m.name} — create_table={creates}, indexes={indexes}')
if not migrations:
    raise SystemExit('No migrations found')
print('OK: migration manifest ready')
