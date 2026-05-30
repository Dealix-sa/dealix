// Canonical Next.js config (CommonJS).
//
// Must stay a single config file: Next.js loads next.config.js before
// next.config.ts, so a second .ts config would be silently ignored and the
// next-intl plugin (wired below) would be dropped, breaking static prerender
// of localized routes. The Railway deploy contract (scripts/verify_railway_surfaces.py)
// also requires this file to enable `output: 'standalone'`.
const createNextIntlPlugin = require("next-intl/plugin");

const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  poweredByHeader: false,
  reactStrictMode: true,
  images: {
    domains: ["api.dealix.ai", "localhost"],
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        ],
      },
    ];
  },
};

module.exports = withNextIntl(nextConfig);
