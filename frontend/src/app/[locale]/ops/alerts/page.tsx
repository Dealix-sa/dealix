import { AppLayout } from "@/components/layout/AppLayout";
import { FounderAlertCenter } from "@/components/ops/FounderAlertCenter";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsAlertsPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "مركز التنبيهات" : "Alert Center"}
      subtitle={isAr ? "مراجعة التنبيهات والموافقة عليها — APPROVAL_FIRST" : "Review and approve alerts — APPROVAL_FIRST"}
    >
      <FounderAlertCenter />
    </AppLayout>
  );
}
