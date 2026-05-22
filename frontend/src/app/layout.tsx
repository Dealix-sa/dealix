import type { Metadata } from "next";
import { Noto_Sans_Arabic } from "next/font/google";
import "./globals.css";

const notoArabic = Noto_Sans_Arabic({
  subsets: ["arabic"],
  variable: "--font-arabic",
  weight: ["300", "400", "500", "600", "700", "800"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Dealix — Post-Lead Revenue OS",
    template: "%s | Dealix",
  },
  description:
    "Saudi B2B Post-Lead Revenue Operations OS — proves owner, approval, evidence, and next action after every lead. PDPL-aligned. No cold WhatsApp or LinkedIn automation.",
  keywords: [
    "RevOps", "Post-Lead Revenue Ops", "Proof Pack", "Risk Score",
    "Saudi Arabia", "PDPL", "AI Governance", "Dealix",
  ],
  icons: {
    icon: [
      { url: "/brand/favicon.svg", type: "image/svg+xml" },
      { url: "/favicon.ico", sizes: "any" },
    ],
    shortcut: "/brand/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html suppressHydrationWarning>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700;800&family=IBM+Plex+Arabic:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className={`${notoArabic.variable} antialiased`}>{children}</body>
    </html>
  );
}
