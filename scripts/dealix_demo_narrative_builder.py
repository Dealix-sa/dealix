from pathlib import Path
out=Path('out/demo/demo_narrative_v8.md'); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('# Demo Narrative V8\n\n1. Show lost lead problem.\n2. Capture lead.\n3. Score and next action.\n4. Draft offer.\n5. Show proof vault and trust center.\n6. Show KPI and board metrics.\n', encoding='utf-8')
print(f'Wrote {out}')
