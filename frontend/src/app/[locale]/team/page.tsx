import type { Metadata } from "next";
import { AppLayout } from "@/components/layout/AppLayout";
import { TeamPage } from "@/components/gtm/TeamPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الفريق — Dealix" : "Team — Dealix",
    description: isAr
      ? "تعرّف على فريق Dealix — منصة تشغيل الإيرادات السعودية المبنية على الحوكمة"
      : "Meet the Dealix team — Saudi revenue operations platform built on governance-first principles",
  };
}

export default async function TeamPageRoute({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "الفريق" : "The Team"}
      subtitle={isAr ? "من نحن وكيف نبني Dealix" : "Who we are and how we build Dealix"}
    >
      <TeamPage />
    </AppLayout>
  );
}
