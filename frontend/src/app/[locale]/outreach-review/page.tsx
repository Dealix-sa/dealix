import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OutreachReviewQueue } from "@/components/approvals/OutreachReviewQueue";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "مراجعة التواصل — Dealix" : "Outreach Review — Dealix",
    description: isAr
      ? "طابور مراجعة المسودات — مسودة/مراجعة/موافق/مرفوض. لا إرسال بدون موافقة وبوابات أمان."
      : "Draft review queue — draft/review/approved/rejected. No send without approval and safety gates.",
    alternates: { canonical: `https://dealix.me/${locale}/outreach-review` },
  };
}

export default async function OutreachReviewPage({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "approvals" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <OutreachReviewQueue />
    </AppLayout>
  );
}