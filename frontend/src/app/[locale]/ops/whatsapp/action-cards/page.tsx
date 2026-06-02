import { AppLayout } from "@/components/layout/AppLayout";
import { WhatsAppClientOsPanel } from "@/components/whatsapp/WhatsAppClientOsPanel";
import { WhatsAppOpsTabs } from "@/components/whatsapp/WhatsAppOpsTabs";

interface Props {
  params: Promise<{ locale: string }>;
}

export default async function OpsWhatsAppActionCardsPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "كروت الإجراءات والموافقات" : "Action & approval cards"}
      subtitle={isAr ? "كل إجراء خارجي يحتاج موافقة بشرية" : "Every external action needs human approval"}
    >
      <WhatsAppOpsTabs locale={locale} active="/action-cards" />
      <WhatsAppClientOsPanel view="action-cards" locale={locale} />
    </AppLayout>
  );
}
