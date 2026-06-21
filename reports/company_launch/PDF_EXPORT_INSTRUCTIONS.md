# PDF Export Instructions

## Current status

HTML presentations are ready:

- `presentations/dealix_company_profile_ar.html`
- `presentations/dealix_company_profile_en.html`
- `presentations/dealix_one_page_offer_ar.html`

No PDF export tool (Chrome, LibreOffice, wkhtmltopdf) was found in this
Codespace, so PDFs were not auto-generated.

## How to export PDFs

### Option 1: Browser print to PDF

1. Open the HTML file in a browser.
2. Press `Ctrl+P` (or `Cmd+P` on macOS).
3. Choose "Save as PDF".
4. Set margins to "None" for full-bleed slides.

### Option 2: Use a headless browser

If Chrome or Chromium is available elsewhere, run:

```bash
chrome --headless --disable-gpu --print-to-pdf=output.pdf file:///path/to/presentation.html
```

### Option 3: Install wkhtmltopdf

```bash
# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

wkhtmltopdf --enable-local-file-access presentations/dealix_company_profile_ar.html presentations/dealix_company_profile_ar.pdf
```

## Target output files

- `presentations/dealix_company_profile_ar.pdf`
- `presentations/dealix_company_profile_en.pdf`
- `presentations/dealix_one_page_offer_ar.pdf`
