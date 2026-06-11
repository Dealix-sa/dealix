# Vercel Frontend Deployment

## Prerequisites
- Vercel account
- GitHub repo connected
- `apps/web` is the Next.js app

## Steps
1. Import project in Vercel dashboard
2. Root directory: `apps/web`
3. Build command: `npm run build`
4. Output directory: `.next`
5. Environment variables:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` (optional, for local ops UI)

## Checks
- `npm run typecheck` passes
- `npm run build` passes
- No secrets in `apps/web/.env*` (use Vercel dashboard instead)

## Post-Deploy
- Run `scripts/post_deploy_smoke.py --base-url https://your-domain.com`
