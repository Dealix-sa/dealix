import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const routes = [
  "",
  "/status",
  "/control-plane",
  "/agents",
  "/approvals",
  "/safety",
  "/sandbox",
  "/value-engine",
  "/self-evolving"
];

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  return routes.map((route) => ({
    url: `${siteUrl}${route}`,
    lastModified: now,
    changeFrequency: route === "" || route === "/status" ? "daily" : "weekly",
    priority: route === "" ? 1 : route === "/status" ? 0.8 : 0.7
  }));
}
