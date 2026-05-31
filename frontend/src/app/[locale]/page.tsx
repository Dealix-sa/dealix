import type { Metadata } from "next";
import { buildHomeMetadata } from "@/lib/gtmMetadata";
import { CommercialLaunchHome } from "@/components/gtm/CommercialLaunchHome";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildHomeMetadata(locale);
}

const ORG_JSON_LD = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  url: "https://dealix.me",
  logo: "https://dealix.me/icon",
  description: "Saudi B2B Revenue Operating System — ZATCA, PDPL, AI Governance",
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  serviceType: ["Revenue Operations", "AI Governance", "ZATCA Compliance", "PDPL Compliance"],
  contactPoint: { "@type": "ContactPoint", contactType: "customer service", availableLanguage: ["Arabic", "English"] },
};

const WEBSITE_JSON_LD = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Dealix",
  url: "https://dealix.me",
  potentialAction: {
    "@type": "SearchAction",
    target: "https://dealix.me/ar/learn?q={search_term_string}",
    "query-input": "required name=search_term_string",
  },
};

const SERVICE_JSON_LD = {
  "@context": "https://schema.org",
  "@type": "Service",
  name: "7-Day Revenue Sprint",
  provider: { "@type": "Organization", name: "Dealix" },
  description:
    "7-day diagnostic sprint covering revenue leakage, ZATCA readiness, AI governance, and CRM quality. Delivers a Proof Pack with documented evidence.",
  offers: {
    "@type": "Offer",
    price: "499",
    priceCurrency: "SAR",
    availability: "https://schema.org/InStock",
  },
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
};

export default function HomePage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify([ORG_JSON_LD, WEBSITE_JSON_LD, SERVICE_JSON_LD]),
        }}
      />
      <CommercialLaunchHome />
    </>
  );
}
