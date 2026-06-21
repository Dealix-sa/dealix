import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { ContactForm } from "@/components/gtm/ContactForm";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "تحدّث معنا · اطلب نظام AI مخصّص — Dealix"
      : "Talk to us · Request a custom AI build — Dealix",
    description: isAr
      ? "اطلب نظام ذكاء اصطناعي مخصّصاً أو تشغيل إيراد مُدار، أو ابدأ بتشخيص مجاني. خطة واضحة وأدلة — لا وعود. PDPL أصلاً، موافقة أولاً."
      : "Request a custom AI build or managed revenue ops, or start with a free diagnostic. Clear plan and evidence — no promises. PDPL-native, approval-first.",
    alternates: { canonical: `https://dealix.me/${locale}/contact` },
    openGraph: {
      title: isAr ? "تحدّث معنا — Dealix" : "Talk to us — Dealix",
      description: isAr
        ? "اطلب AI مخصّص · تشغيل إيراد مُدار · تشخيص مجاني — موافقة أولاً"
        : "Custom AI · Managed Revenue Ops · Free diagnostic — approval-first",
      url: `https://dealix.me/${locale}/contact`,
      images: [{ url: "https://dealix.me/brand/og-dealix.svg", width: 1200, height: 630, alt: "Dealix" }],
    },
  };
}

export default function ContactPage() {
  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-5xl px-6 py-12">
        <ContactForm />
      </div>
    </PublicGtmShell>
  );
}
