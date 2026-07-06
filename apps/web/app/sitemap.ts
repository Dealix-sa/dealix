import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";
const now = new Date();

export default function sitemap(): MetadataRoute.Sitemap {
  const pages: Array<{
    path: string;
    priority: number;
    changeFrequency: "always" | "hourly" | "daily" | "weekly" | "monthly" | "yearly" | "never";
  }> = [
    // ── Canonical (System B / PREMIUM_OFFERS, per Finding 0 resolution
    //    2026-07-06 -- see docs/ops/TASTE_SKILL_DESIGN_AUTOMATION_PLAN.md).
    //    The old /ar/* subtree is no longer listed here: it now 301s to
    //    these pages (next.config.js), so it shouldn't compete with them
    //    for search-engine priority. ──────────────────────────────────
    { path: "",                priority: 1.0,  changeFrequency: "daily"   },
    { path: "/pricing",        priority: 0.95, changeFrequency: "weekly"  },
    { path: "/offers",         priority: 0.90, changeFrequency: "weekly"  },
    { path: "/services",       priority: 0.85, changeFrequency: "weekly"  },
    { path: "/cases",          priority: 0.75, changeFrequency: "weekly"  },
    { path: "/book",           priority: 0.85, changeFrequency: "weekly"  },
    { path: "/products",       priority: 0.75, changeFrequency: "weekly"  },
    { path: "/status",         priority: 0.8,  changeFrequency: "daily"   },
    { path: "/control-plane",  priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/agents",         priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/approvals",      priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/safety",         priority: 0.7,  changeFrequency: "weekly"  },
    { path: "/sandbox",        priority: 0.5,  changeFrequency: "weekly"  },
    { path: "/value-engine",   priority: 0.7,  changeFrequency: "weekly"  },
    { path: "/self-evolving",  priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/revenue-os",     priority: 0.7,  changeFrequency: "weekly"  },
    { path: "/go-to-market",   priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/product-network",priority: 0.6,  changeFrequency: "weekly"  },
  ];

  return pages.map(({ path, priority, changeFrequency }) => ({
    url: `${siteUrl}${path}`,
    lastModified: now,
    changeFrequency,
    priority,
    alternates: { languages: { "ar-SA": `${siteUrl}${path}` } },
  }));
}
