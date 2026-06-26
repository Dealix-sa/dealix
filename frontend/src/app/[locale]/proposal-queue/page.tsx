import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ProposalQueueContent } from "@/components/pipeline/ProposalQueueContent";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "طابور العروض — Dealix" : "Proposal Queue — Dealix",
    description: isAr
      ? "العروض بالحالة والقيمة والمرحلة — بدون بيانات وهمية."
      : "Proposals with status, value, and stage — no fake data.",
    alternates: { canonical: `https://dealix.me/${locale}/proposal-queue` },
  };
}

export default async function ProposalQueuePage({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "pipeline" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <ProposalQueueContent />
    </AppLayout>
  );
}