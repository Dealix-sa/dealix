from pathlib import Path
routes=list(Path('frontend/src/app/api').glob('**/route.ts')) if Path('frontend/src/app/api').exists() else []
print('# API Route Contract')
for r in routes:
    text=r.read_text(encoding='utf-8', errors='ignore')
    methods=[m for m in ['GET','POST','PUT','PATCH','DELETE'] if f'function {m}' in text or f'async function {m}' in text]
    print(f'- {r}: {",".join(methods) or "no explicit method found"}')
print(f'Total routes: {len(routes)}')
