# 100 — Site Manual QA Checklist

قائمة فحص يدوية للموقع قبل الإعلان الرسمي. نفّذها في المتصفح على جوال وحاسب.
Manual website QA before public announcement. Run in a browser on mobile and desktop.

## Pages
- [ ] Homepage loads, hero + CTA clear
- [ ] Commercial / services page(s)
- [ ] Verticals page(s)
- [ ] Pricing
- [ ] Trust / compliance
- [ ] Contact
- [ ] Status / health page

## Layout & language
- [ ] Mobile layout (no overflow, tap targets OK)
- [ ] Arabic text renders RTL correctly
- [ ] English text renders correctly
- [ ] Primary CTA visible above the fold

## SEO & metadata
- [ ] Title + meta description per page
- [ ] Sitemap reachable (`/sitemap.xml`)
- [ ] `robots.txt` present and sane
- [ ] OpenGraph tags (title/description/image)
- [ ] Structured data where relevant

## Safety / compliance
- [ ] **No exaggerated claims** (guaranteed ROI, 100%, replace your team, automate everything, no human needed)
- [ ] No broken links
- [ ] **No sensitive-data request** in any form (no national ID, financial, health) before agreement
- [ ] Forms do not auto-submit; consent is explicit

## Sign-off
- [ ] Founder reviewed on desktop
- [ ] Founder reviewed on mobile
- [ ] Static check (`site_launch_static_check.py`) PASS
- [ ] Approved for public announcement
