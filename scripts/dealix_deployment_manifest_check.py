from pathlib import Path
checks=['deployment/ENVIRONMENT_CONTRACT.md','frontend/public/robots.txt','frontend/public/sitemap.xml','frontend/src/app/[locale]/contact/page.tsx','frontend/src/app/[locale]/diagnostic/page.tsx']
missing=[c for c in checks if not Path(c).exists()]
if missing:
 print('Deployment manifest incomplete:'); [print('-',m) for m in missing]; raise SystemExit(1)
print('OK: deployment manifest looks complete')
