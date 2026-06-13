import type { Metadata } from "next";
import { ContactPage } from "@/components/gtm/ContactPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "تواصل مع Dealix" : "Contact Dealix",
    description: isAr
      ? "احجز مكالمة، أو راسلنا، أو ابدأ بتشخيص Risk Score مجاني. نرد خلال 48 ساعة عمل."
      : "Book a call, email us, or start with a free Risk Score. We reply within 48 business hours.",
    alternates: { canonical: `https://dealix.me/${locale}/contact` },
  };
}

export default function ContactRoute() {
  return <ContactPage />;
}
