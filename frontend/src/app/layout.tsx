import type { Metadata } from "next";
import { Noto_Sans_Arabic } from "next/font/google";
import "./globals.css";
import "@/styles/dealix-system.css";

const notoArabic = Noto_Sans_Arabic({
  subsets: ["arabic"],
  variable: "--font-arabic",
  weight: ["300", "400", "500", "600", "700", "800"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Dealix — نظام تشغيل الإيرادات B2B السعودي",
    template: "%s | Dealix",
  },
  description:
    "منصة Revenue Operations مبنية للسوق السعودي — PDPL أصيل، ZATCA جاهز، حوكمة AI واضحة، موافقة قبل أي إرسال.",
  keywords: [
    "RevOps",
    "Revenue Ops",
    "AI Governance",
    "Saudi Arabia",
    "B2B",
    "PDPL",
    "ZATCA",
    "Dealix",
    "نظام الإيرادات",
    "حوكمة الذكاء الاصطناعي",
  ],
  metadataBase: new URL("https://dealix.me"),
  openGraph: {
    type: "website",
    siteName: "Dealix",
    images: [{ url: "/brand/og-dealix.svg", width: 1200, height: 630, alt: "Dealix — Saudi B2B Revenue OS" }],
  },
  twitter: { card: "summary_large_image", site: "@dealix_sa" },
  icons: {
    icon: [{ url: "/brand/logo-mark.svg", type: "image/svg+xml" }],
    apple: "/brand/logo-mark.svg",
  },
};

const ORG_JSON_LD = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  alternateName: "ديلكس",
  url: "https://dealix.me",
  logo: "https://dealix.me/brand/logo.svg",
  description:
    "Saudi B2B Revenue Operating System — AI-governed Revenue Ops with PDPL-native compliance and ZATCA readiness.",
  foundingDate: "2024",
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  contactPoint: {
    "@type": "ContactPoint",
    contactType: "customer support",
    email: "support@dealix.me",
    availableLanguage: ["Arabic", "English"],
  },
  sameAs: ["https://www.linkedin.com/company/dealix-sa"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html suppressHydrationWarning>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500&family=Cairo:wght@600;700;900&family=Tajawal:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400&family=Noto+Sans+Arabic:wght@300;400;500;600;700;800&family=IBM+Plex+Arabic:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(ORG_JSON_LD) }}
        />
      </head>
      <body className={`${notoArabic.variable} antialiased`}>{children}</body>
    </html>
  );
}
