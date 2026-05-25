import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { CommandCenterContent } from "@/components/command-center/CommandCenterContent";

interface CommandCenterPageProps {
  params: Promise<{ locale: string }>;
}

export default async function CommandCenterPage({ params }: CommandCenterPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "commandCenter" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <CommandCenterContent />
    </AppLayout>
  );
}
