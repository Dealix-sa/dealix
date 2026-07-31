// Lighthouse CI config — current Tier-1 public and customer surfaces.
// Runs against the highest-impact indexable, trust, and customer pages.
// Checkout is intentionally excluded: the current commercial path is
// Free Mini Diagnostic → quote-only 30-Day Revenue Command Pilot.

module.exports = {
  ci: {
    collect: {
      // Built by GitHub Actions: python3 -m http.server 8765 inside landing/
      url: [
        "http://localhost:8765/",
        "http://localhost:8765/pricing.html",
        "http://localhost:8765/diagnostic.html",
        "http://localhost:8765/customer-portal.html",
        "http://localhost:8765/proof.html",
        "http://localhost:8765/trust-center.html",
        "http://localhost:8765/agency-partner.html",
        "http://localhost:8765/privacy.html",
        "http://localhost:8765/customer-decisions.html",
        "http://localhost:8765/login.html",
      ],
      numberOfRuns: 1,
      settings: {
        preset: "desktop",
        chromeFlags: "--no-sandbox --headless",
      },
    },
    assert: {
      preset: "lighthouse:no-pwa",
      assertions: {
        "categories:performance": ["warn", { minScore: 0.75 }],
        "categories:accessibility": ["error", { minScore: 0.85 }],
        "categories:best-practices": ["warn", { minScore: 0.80 }],
        "categories:seo": ["error", { minScore: 0.85 }],
        "color-contrast": ["error", { minScore: 1 }],
        "image-alt": ["error", { minScore: 1 }],
        "link-name": ["error", { minScore: 1 }],
        "html-has-lang": ["error", { minScore: 1 }],
        "html-lang-valid": ["error", { minScore: 1 }],
        "first-contentful-paint": ["warn", { maxNumericValue: 2500 }],
        "largest-contentful-paint": ["warn", { maxNumericValue: 4000 }],
        "cumulative-layout-shift": ["warn", { maxNumericValue: 0.1 }],
      },
    },
    upload: {
      target: "temporary-public-storage",
    },
  },
};
