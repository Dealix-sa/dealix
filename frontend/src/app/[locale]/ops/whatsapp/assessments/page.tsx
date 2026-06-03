import { AppLayout } from "@/components/layout/AppLayout";
import { WhatsAppClientOsPanel } from "@/components/whatsapp/WhatsAppClientOsPanel";
import { WhatsAppOpsTabs } from "@/components/whatsapp/WhatsAppOpsTabs";

interface Props {
  params: Promise<{ locale: string }>;
}

export default async function OpsWhatsAppAssessmentsPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "فحوصات الجاهزية" : "Readiness assessments"}
      subtitle={isAr ? "Dealix Company Readiness Scan" : "Dealix Company Readiness Scan"}
    >
      <WhatsAppOpsTabs locale={locale} active="/assessments" />
      <WhatsAppClientOsPanel view="assessments" locale={locale} />
    </AppLayout>
  );
}
