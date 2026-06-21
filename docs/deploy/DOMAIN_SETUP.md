# Domain Setup

## Recommended
- Primary: `dealix.sa` or `dealix.com`
- WWW redirect to apex or vice versa
- `www` CNAME to Vercel
- Apex A/ANAME to Vercel IPs or use Cloudflare

## DNS Records
| Type | Name | Value |
|------|------|-------|
| CNAME | www | cname.vercel-dns.com |
| A | @ | Vercel IP |

## SSL
- Enable automatic SSL on Vercel
- Force HTTPS redirect

## Backend
- Railway provides `*.up.railway.app`
- Custom domain via Railway settings
- CNAME `api` to Railway domain
