from pathlib import Path

src=Path('investor/INVESTOR_MEMO_AR.md').read_text(encoding='utf-8')
metrics=Path('out/board/board_metrics.md')
metrics_text=metrics.read_text(encoding='utf-8') if metrics.exists() else 'Metrics not generated yet.'
out=Path('out/investor/investor_memo_compiled.md'); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src+'\n\n---\n\n## آخر مؤشرات\n\n'+metrics_text, encoding='utf-8')
print(f'Wrote {out}')
