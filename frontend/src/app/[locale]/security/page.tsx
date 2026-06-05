import type { Metadata } from "next";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { SecurityPage } from "@/components/wave3/SecurityPage";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/security",
    "الأمان والحوكمة — موافقة أولاً",
    "Security & Governance — approval-first",
    "موافقة بشرية لكل إجراء خارجي، لا إرسال تلقائي، لا scraping، واحترام الخصوصية.",
    "Human approval for every external action, no auto-send, no scraping, privacy respected.",
  );
}

export default async function Security({ params }: PageProps) {
  const { locale } = await params;
  return (
    <MarketingShell locale={locale}>
      <SecurityPage locale={locale} />
    </MarketingShell>
  );
}
