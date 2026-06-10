import type { Metadata } from "next";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { CommandSprintPage } from "@/components/wave3/CommandSprintPage";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/command-sprint",
    "Dealix Command Sprint — 7 أيام",
    "Dealix Command Sprint — 7 days",
    "7 أيام ثابتة النطاق تنتج Proof Pack: خريطة فرص، سجل إثبات، وملخص تنفيذي. الوعد وضوح لا ضمان.",
    "A 7-day fixed scope that produces a Proof Pack: revenue map, proof register, executive brief. The promise is clarity, not a guarantee.",
  );
}

export default async function CommandSprint({ params }: PageProps) {
  const { locale } = await params;
  return (
    <MarketingShell locale={locale}>
      <CommandSprintPage locale={locale} />
    </MarketingShell>
  );
}
