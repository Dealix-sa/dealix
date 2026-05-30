import type { MetadataRoute } from "next";
import { LEARN_ARTICLES } from "@/content/learn/articles";

const BASE = process.env.NEXT_PUBLIC_SITE_URL || "https://dealix.me";

export default function sitemap(): MetadataRoute.Sitemap {
  const locales = ["ar", "en"] as const;
  const staticPaths = ["", "/risk-score", "/proof-pack", "/dealix-diagnostic", "/services", "/learn", "/partners"];
  const entries: MetadataRoute.Sitemap = [];

  for (const locale of locales) {
    for (const path of staticPaths) {
      entries.push({
        url: `${BASE}/${locale}${path}`,
        changeFrequency: path === "" ? "weekly" : "monthly",
        priority: path === "" ? 1 : 0.8,
      });
    }
    for (const article of LEARN_ARTICLES) {
      entries.push({
        url: `${BASE}/${locale}/learn/${article.slug}`,
        changeFrequency: "monthly",
        priority: 0.7,
      });
    }
  }
  return entries;
}
