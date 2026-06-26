import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { DeliveryTrackingContent } from "@/components/clients/DeliveryTrackingContent";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "تتبع التسليم — Dealix" : "Delivery Tracking — Dealix",
    description: isAr
      ? "مشاريع العميل عبر مراحل: استيعاب، تشخيص، مخطط، بناء، QA، UAT، إطلاق، تدريب، إثبات."
      : "Client projects across stages: intake, diagnosis, blueprint, build, QA, UAT, launch, training, proof.",
    alternates: { canonical: `https://dealix.me/${locale}/delivery` },
  };
}

export default async function DeliveryPage({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "clients" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <DeliveryTrackingContent />
    </AppLayout>
  );
}