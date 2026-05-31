import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Dealix — Saudi B2B Revenue Engine",
    short_name: "Dealix",
    description:
      "Saudi-first B2B revenue, growth, and compliance engine with approval-first AI execution.",
    start_url: "/",
    scope: "/",
    display: "standalone",
    background_color: "#06111f",
    theme_color: "#06111f",
    lang: "ar-SA",
    dir: "rtl",
    categories: ["business", "productivity"],
    screenshots: [
      {
        src: `${siteUrl}/screenshot-wide.png`,
        sizes: "1280x720",
        type: "image/png"
      }
    ]
  };
}
