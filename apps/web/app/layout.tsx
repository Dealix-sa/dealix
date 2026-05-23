import "./globals.css";
import "../styles/brand.css";
import type { ReactNode } from "react";
import { dealixBrand } from "../lib/brand-tokens";

export const metadata = {
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.local"
  ),
  title: `${dealixBrand.wordmark} — Founder Console`,
  description: dealixBrand.positioning,
  icons: { icon: "/brand/favicon.svg" },
  openGraph: {
    title: `${dealixBrand.wordmark} — ${dealixBrand.taglineEn}`,
    description: dealixBrand.positioning,
    images: ["/brand/og.svg"],
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar">
      <body className="dlx-app">
        <div style={{ maxWidth: 1280, margin: "0 auto", padding: "24px 28px" }}>
          {children}
        </div>
      </body>
    </html>
  );
}
