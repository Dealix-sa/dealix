import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getSector, sectorSlugs } from "@/content/wave3/sectors";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";
import { Section } from "@/components/wave3/Section";
import { buildSectorMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string; sector: string }> };

export async function generateStaticParams() {
  const locales = ["ar", "en"];
  return locales.flatMap((locale) => sectorSlugs().map((sector) => ({ locale, sector })));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale, sector } = await params;
  const s = getSector(sector);
  if (!s) return { title: "Dealix" };
  return buildSectorMetadata(locale, sector, s.nameAr, s.nameEn, s.descAr, s.descEn);
}

export default async function SectorPage({ params }: PageProps) {
  const { locale, sector } = await params;
  const s = getSector(sector);
  if (!s) notFound();

  const isAr = locale === "ar";
  const pains = isAr ? s.painAr : s.painEn;
  const outcomes = isAr ? s.outcomesAr : s.outcomesEn;

  return (
    <MarketingShell locale={locale}>
      <Link href={`/${locale}/industries`} className="text-sm text-muted-foreground hover:text-foreground">
        {isAr ? "← القطاعات" : "← Industries"}
      </Link>
      <h1 className="mt-4 text-3xl font-bold font-display md:text-4xl">
        {isAr ? s.nameAr : s.nameEn}
      </h1>
      <p className="mt-3 text-lg text-muted-foreground">{isAr ? s.descAr : s.descEn}</p>

      <Section eyebrow={isAr ? "التحدي" : "The challenge"} title={isAr ? "أين يحدث التعطل" : "Where it stalls"}>
        <ul className="list-disc space-y-2 ps-5 text-muted-foreground">
          {pains.map((p, i) => <li key={i}>{p}</li>)}
        </ul>
      </Section>

      <Section eyebrow={isAr ? "المخرجات" : "Outcomes"} title={isAr ? "ما تحصل عليه" : "What you get"}>
        <ul className="list-disc space-y-2 ps-5 text-muted-foreground">
          {outcomes.map((o, i) => <li key={i}>{o}</li>)}
        </ul>
        <p className="mt-4 text-sm text-muted-foreground">
          {isAr ? `الطبقة المقترحة: ${s.recommendedOsAr}` : `Recommended: ${s.recommendedOsEn}`}
        </p>
      </Section>

      <div className="mt-8">
        <PrimaryCta
          locale={locale}
          href="/tools/business-os-score"
          labelAr="احصل على تقييم قطاعك"
          labelEn="Get Sector Score"
        />
      </div>
    </MarketingShell>
  );
}
