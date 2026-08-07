import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: [
          "/",
          "/pricing",
          "/offers",
          "/services",
          "/cases",
          "/book",
          "/products",
          "/status",
          "/revenue-os",
          "/go-to-market",
          "/product-network",
          "/safety",
          "/value-engine",
        ],
        // Block internal ops surfaces from indexing. /ar/* is no longer
        // listed here or in allow -- it 301s to the canonical pages
        // above (next.config.js), so crawlers land on the redirect
        // target and never need to index the old path directly.
        disallow: [
          "/control-plane",
          "/agents",
          "/approvals",
          "/sandbox",
          "/self-evolving",
          "/_next/",
          "/api/",
          "/healthz",
        ],
      },
      // Block AI training crawlers
      {
        userAgent: "GPTBot",
        disallow: ["/"],
      },
      {
        userAgent: "CCBot",
        disallow: ["/"],
      },
      {
        userAgent: "anthropic-ai",
        disallow: ["/"],
      },
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
    host: siteUrl,
  };
}
