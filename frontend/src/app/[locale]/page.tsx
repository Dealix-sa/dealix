import type { Metadata } from "next";
import { buildHomeMetadata } from "@/lib/gtmMetadata";
import { CommercialLaunchHome } from "@/components/gtm/CommercialLaunchHome";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildHomeMetadata(locale);
}

export default async function HomePage({ params }: PageProps) {
  const { locale } = await params;
  
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": locale === "ar" ? "ما هو نظام ديلكس (Dealix)؟" : "What is Dealix?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": locale === "ar" ? "ديلكس هو أول نظام تشغيل إيرادات (Revenue OS) مدعوم بوكلاء الذكاء الاصطناعي في السعودية متوافق مع لوائح سدايا." : "Dealix is the first AI-powered Revenue OS in Saudi Arabia, compliant with SDAIA regulations."
        }
      },
      {
        "@type": "Question",
        "name": locale === "ar" ? "هل يدعم ديلكس لوائح حماية البيانات الشخصية (PDPL)؟" : "Does Dealix support PDPL?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": locale === "ar" ? "نعم، ديلكس مصمم ليتوافق تمامًا مع نظام حماية البيانات الشخصية (PDPL) المطبق في المملكة العربية السعودية." : "Yes, Dealix is fully compliant with the Personal Data Protection Law (PDPL) in Saudi Arabia."
        }
      }
    ]
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      <CommercialLaunchHome />
    </>
  );
}
