import type { Metadata } from "next";
import Link from "next/link";
import { ServicesSprintPanelDynamic } from "@/components/services/ServicesSprintPanelDynamic";
import { buildServicesMetadata } from "@/lib/gtmMetadata";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: ServicesHubProps): Promise<Metadata> {
  const { locale } = await params;
  return buildServicesMetadata(locale);
}

export default async function ServicesHubPage({ params }: ServicesHubProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "خدمات Dealix — سلم العروض الخمسة"
      : "Dealix Services — Five-Tier Offer Ladder",
    description: isAr
      ? "من التشخيص المجاني إلى مشاريع AI المخصصة — كل مستوى يبني على الإثبات قبل التوسع."
      : "From free diagnostic to custom AI projects — every tier builds on proof before expansion.",
    alternates: { canonical: `https://dealix.me/${locale}/services` },
  };
}

export default function ServicesHubPage() {
  return <ServicesPage />;
}
