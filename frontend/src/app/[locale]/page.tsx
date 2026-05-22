import type { Metadata } from "next";
import { CommercialLaunchHome } from "@/components/gtm/CommercialLaunchHome";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  const title = isAr
    ? "Dealix — يثبت ماذا يحدث بعد الـ lead"
    : "Dealix — proves what happens after the lead";
  const description = isAr
    ? "Revenue OS للوكالات في السعودية — Risk Score، Proof Pack، تشخيص محكوم. لا واتساب بارد."
    : "Revenue OS for agencies in Saudi Arabia — Risk Score, Proof Pack, governed diagnostic. No cold WhatsApp.";
  return {
    title,
    description,
    openGraph: { title, description, locale: isAr ? "ar_SA" : "en_US", type: "website" },
  };
}

export default function HomePage() {
  return <CommercialLaunchHome />;
}
