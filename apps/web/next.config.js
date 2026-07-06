const path = require("path");
const { withSentryConfig } = require("@sentry/nextjs");

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  outputFileTracingRoot: path.join(__dirname, "../../"),
  poweredByHeader: false,
  reactStrictMode: true,
  compress: true,

  // Security & performance headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-DNS-Prefetch-Control',  value: 'on' },
          { key: 'X-Frame-Options',          value: 'SAMEORIGIN' },
          { key: 'X-Content-Type-Options',   value: 'nosniff' },
          { key: 'Referrer-Policy',          value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy',       value: 'camera=(), microphone=(), geolocation=()' },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com",
              "font-src 'self' https://fonts.gstatic.com",
              "img-src 'self' data: https:",
              "connect-src 'self' https://api.dealix.me https://us.i.posthog.com",
              "frame-ancestors 'none'",
            ].join('; '),
          },
        ],
      },
      // Cache static assets aggressively
      {
        source: '/_next/static/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ];
  },

  // Redirects
  //
  // 2026-07-06: founder decision resolved a multi-system brand/pricing
  // conflict in favor of the PREMIUM_OFFERS ladder (see docs/ops/
  // TASTE_SKILL_DESIGN_AUTOMATION_PLAN.md, "Finding 0"). /pricing used to
  // permanently redirect to /ar/pricing (a separate P1/P2/P3 system) --
  // that redirect is removed so /pricing serves its own real page. The
  // /ar/* subtree, /landing, and /signup represented the losing systems
  // (the P1/P2/P3 ladder and a self-serve ERP-SaaS pivot); they now 301
  // to their closest equivalent canonical page. Underlying page files
  // are intentionally left in place for now (a redirect takes effect
  // before the page renders either way) -- deleting them is a separate,
  // lower-stakes cleanup, not required to fix the user-facing conflict.
  async redirects() {
    return [
      { source: '/landing',              destination: '/',          permanent: true },
      { source: '/signup',               destination: '/book',      permanent: true },
      { source: '/ar',                   destination: '/',          permanent: true },
      { source: '/ar/pricing',           destination: '/pricing',   permanent: true },
      { source: '/ar/offers',            destination: '/offers',    permanent: true },
      { source: '/ar/p1',                destination: '/offers',    permanent: true },
      { source: '/ar/p2',                destination: '/offers',    permanent: true },
      { source: '/ar/p3',                destination: '/offers',    permanent: true },
      { source: '/ar/diagnostic-sprint', destination: '/offers',    permanent: true },
      { source: '/ar/demo',              destination: '/book',      permanent: true },
      { source: '/ar/intake',            destination: '/book',      permanent: true },
      { source: '/ar/case-studies',      destination: '/cases',    permanent: true },
      { source: '/ar/company-os',        destination: '/brain',    permanent: true },
      { source: '/ar/control-room',      destination: '/command-center', permanent: true },
      { source: '/ar/transformation',    destination: '/services', permanent: true },
      { source: '/ar/trust',             destination: '/safety',   permanent: true },
      { source: '/ar/zatca-readiness',   destination: '/services', permanent: true },
    ];
  },

  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 86400,
    remotePatterns: [
      { protocol: 'https', hostname: 'dealix.me' },
      { protocol: 'https', hostname: 'api.dealix.me' },
    ],
  },

  // Bundle optimization
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['react', 'react-dom'],
  },
};

module.exports = withSentryConfig(
  nextConfig,
  {
    // Only print logs in production builds (not in dev)
    silent: true,
    // Disable Sentry webpack plugin in dev/local builds
    org: process.env.SENTRY_ORG,
    project: process.env.SENTRY_PROJECT,
    // Only upload source maps when SENTRY_AUTH_TOKEN is set
    authToken: process.env.SENTRY_AUTH_TOKEN,
    // Don't upload source maps if no DSN is configured
    disableServerWebpackPlugin: !process.env.SENTRY_DSN && !process.env.NEXT_PUBLIC_SENTRY_DSN,
    disableClientWebpackPlugin: !process.env.SENTRY_DSN && !process.env.NEXT_PUBLIC_SENTRY_DSN,
  },
);
