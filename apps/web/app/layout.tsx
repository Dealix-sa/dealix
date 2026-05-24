import "./globals.css";
import type { ReactNode } from "react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: {
    default: "Dealix — Intelligent Deals. Real Growth.",
    template: "%s · Dealix",
  },
  description:
    "Dealix is a Saudi B2B Revenue Operating System for intelligent deal flow, founder-approved growth, and trust-gated AI execution.",
  icons: {
    icon: "/brand/favicon.svg",
  },
  openGraph: {
    title: "Dealix — Intelligent Deals. Real Growth.",
    description:
      "Saudi B2B Revenue Operating System. Trust-gated AI execution. Founder-approved growth.",
    images: ["/brand/dealix-og.svg"],
    type: "website",
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
