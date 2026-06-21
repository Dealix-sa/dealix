# Dealix Website Implementation

## Location

The public bilingual website lives in:

apps/website

## Routes

- /ar Arabic landing page
- /en English landing page

## Commands

Install:

cd apps/website
npm install

Build:

npm run build

Run locally:

npm run dev

## Deployment

Recommended deployment options:

1. Railway service dedicated to website
   - Root Directory: apps/website
   - Build Command: npm install && npm run build
   - Start Command: npm run preview -- --host 0.0.0.0 --port $PORT

2. Vercel
   - Root Directory: apps/website
   - Framework: Vite

## Notes

The API service should remain separate from the public website unless the production architecture intentionally combines them.
