import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OutboundSafetyContent } from "@/components/settings/OutboundSafetyContent";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "أمان الاتصال الخارجي — Dealix" : "Outbound Safety — Dealix",
    description: isAr
      ? "حالة كل علم بيئة، بوابات جاهزية القنوات، وتوثيق — بدون تفعيل إرسال حي."
      : "Status of every env flag, channel readiness gates, and documentation — no live send toggle.",
    alternates: { canonical: `https://dealix.me/${locale}/settings/outbound-safety` },
  };
}

export default async function OutboundSafetyPage({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "settings" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <OutboundSafetyContent />
    </AppLayout>
  );
}