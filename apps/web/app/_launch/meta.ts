import type { Metadata } from "next";

// Build consistent, SEO-complete metadata for a launch page.
export function makeMetadata(opts: {
  title: string;
  description: string;
  path: string;
}): Metadata {
  const { title, description, path } = opts;
  return {
    title,
    description,
    alternates: {
      canonical: path,
      languages: { "ar-SA": "/ar", "en-US": path },
    },
    openGraph: {
      type: "website",
      url: path,
      title,
      description,
      siteName: "Dealix",
      locale: "en_US",
      alternateLocale: ["ar_SA"],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
    },
  };
}
