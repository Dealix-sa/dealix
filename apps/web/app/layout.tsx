import "./globals.css";
import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Dealix — Saudi B2B Revenue Engine",
    template: "%s | Dealix"
  },
  description:
    "Dealix is a Saudi-first B2B revenue, growth, and compliance engine with approval-first AI execution.",
  applicationName: "Dealix",
  keywords: [
    "Dealix",
    "Saudi B2B",
    "AI revenue engine",
    "PDPL",
    "ZATCA",
    "sales automation",
    "Saudi Arabia"
  ],
  authors: [{ name: "Dealix" }],
  creator: "Dealix",
  publisher: "Dealix",
  alternates: {
    canonical: "/"
  },
  openGraph: {
    type: "website",
    locale: "ar_SA",
    alternateLocale: ["en_US"],
    url: siteUrl,
    siteName: "Dealix",
    title: "Dealix — Saudi B2B Revenue Engine",
    description:
      "Saudi-first B2B revenue, growth, and compliance engine with approval-first AI execution."
  },
  twitter: {
    card: "summary_large_image",
    title: "Dealix — Saudi B2B Revenue Engine",
    description:
      "Saudi-first B2B revenue, growth, and compliance engine with approval-first AI execution."
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-snippet": -1,
      "max-image-preview": "large",
      "max-video-preview": -1
    }
  }
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  themeColor: "#06111f"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
