# Dealix Founder OS — Complete Dashboard Platform

## Overview
A comprehensive 13-page dashboard built for the Dealix founder to manage the entire business operation — from daily 90-minute cockpit to revenue battles, evidence tracking, and strategic planning.

## Deployment
- **URL**: https://myltgwgr5na3m.kimi.page
- **Stack**: React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui + Recharts
- **Features**: React Router, Framer Motion, 40+ UI components

## Pages (13 Total)

### Core Operations
1. **Cockpit** (`/`) — Daily 90-minute founder dashboard with KPIs, revenue chart, task list, quick actions
2. **Command Room** (`/command-room`) — Real-time system monitoring, service health, live alerts
3. **War Room** (`/war-room`) — Revenue battles with pipeline progress, team leaderboard, weekly analytics

### Business Operations
4. **Evidence Board** (`/evidence`) — Proof points and metrics demonstrating Dealix effectiveness
5. **Approvals Center** (`/approvals`) — Pending approvals with accept/reject actions
6. **Marketing Ops** (`/marketing`) — Campaign management, traffic analytics, lead generation
7. **Sales Ops** (`/sales`) — Full CRM with pipeline, deals, monthly performance

### Strategy & Finance
8. **Strategy** (`/strategy`) — OKRs with progress tracking, quarterly objectives
9. **Financial** (`/financial`) — Revenue vs expenses, transactions, profit margin
10. **Analytics** (`/analytics`) — User analytics, device breakdown, top pages

### System
11. **Settings** (`/settings`) — Profile, notifications, security, billing, language, appearance

## Design System
- **Colors**: Emerald `#1B5E3B` + Gold `#C9A94C` + Charcoal `#1A1A1A`
- **Sidebar**: Dark theme with gold active indicator
- **RTL**: Full Arabic RTL support
- **Responsive**: Works on all screen sizes

## How to Run Locally
```bash
cd frontend/founder-dashboard
npm install
npm run dev
```

## Build for Production
```bash
npm run build
cd dist && python3 -m http.server 8080
```

## Source Files
All source code in: `frontend/founder-dashboard/src/`

## Complete Package
All marketing assets, presentations, and dashboard source are included in:
- `brand/` — Visual identity assets
- `presentations/` — Company profile + sector pitches (PPTD format)
- `frontend/founder-dashboard/` — Full dashboard source code
